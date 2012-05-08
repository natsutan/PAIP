#python3
# -*- coding: utf-8 -*-
import copy
import const
import tools
import sys

const.fail = None
const.no_binding = {True:True,}
debug = False
depth = 0

def debout(s):
    if debug:
        print("  " * depth + s)


eliza_rule = [['?*?x hello ?*?y', ['How do you do Please store your problem',]],
              ['?*?x I want ?*?y',['What would it mean if you got it ?y',
                                   'Why do you want ?y',
                                   'Suppose you got ?y soon']]]

def rule_pattern(rule):
    return rule[0]

def rule_responses (rule):
    return rule[1]


def use_eliza_rules(input):
    for rule in eliza_rule:
        result = pattern_match(rule_pattern(rule), input)
        if result != const.fail:
            response = to_list(tools.ramdom_elt(rule_responses(rule)))
            message = tools.sublis(result, response)
            return to_string(message)
    const.fail



def is_list(val):
    """
    引数がリストの時True、文字列（単語）の時Falseを返す。
    """
    ret= not isinstance(val, str)
    debout("in consp val = %s, return %s" % (val, ret))
    return ret


def is_variable(pattern):
    """petternが変数かどうかを、先頭の文字で判断する"""
    ret = isinstance(pattern, str) and pattern[0] == '?'
    debout("is_variable %s return %s" % (pattern, ret))
    return ret

def get_binding(var, bindings):
    """varが束縛している変数を返す。見つからなかった時は、const.failを返す"""
    if isinstance(var[0], str):
        key = var
    else:
        key = tuple(var[0])

    return bindings.get(key, const.fail)

def extend_bindings(var, val, bindings):
    """valにvarを束縛する"""
    if isinstance(var, str):
        key = var
    else:
        key = tuple(var)

    bindings[key] = val
    return bindings


def match_variable(var, input, bindings):
    """
    変数をマッチさせる。
    varが変数を束縛しているときはbindingsを返す。何も束縛していない時は、新しく束縛したbindingを返す。
    """
    binding = get_binding(var, bindings)
    debout("in match_variable binding = %s" % binding)

    if binding == const.fail:
        return extend_bindings(var, input, bindings)
    if input == binding:
        return bindings
    return const.fail

def first(li):
    """ car """
    if isinstance(li, str):
        return li
    else:
        return li[0]

def rest(li):
    """ cdr """
    if isinstance(li, str):
        return []
    else:
        return li[1:]

def to_list(s):
    """文字列をword単位のListに変更する"""
    if is_list(s):
        return s
    else:
        return s.split()

def to_string(l):
    result = ""
    if len(l) == 0:
        return l
    for s in l:
        result = result + s + " "
    return result


def pat_match(pattern, input, bindings = 'no binding'):
    """マッチングのメインルーチン"""
    if debug : print("in pat_match pattern = %s, input = %s, binidng=%s" % (pattern, input, bindings))
    if bindings == 'no binding':
        bindings = copy.copy(const.no_binding)

    if bindings == const.fail:
        debout(" *fail(binding)")
        return const.fail
    if is_variable(pattern):
        debout(" *variable %s %s" % (pattern, input))
        return match_variable(pattern, input, bindings)
    if pattern == input:
        debout(" *matched %s %s" % (pattern, input))
        return bindings
    if is_segment_pattern(pattern):
        debout(" *matched %s %s" % (pattern, input))
        return segment_match(pattern, input, bindings)
    if input == [] or pattern == []:
        return bindings
    if is_list(pattern) and  is_list(input):
        pat_f  = first(pattern)
        pat_r   = rest(pattern)
        input_f  = first(input)
        input_r   = rest(input)

        result1 = pat_match(pat_f, input_f, bindings)
        debout("result1 = %s pattern %s input = %s bindings = %s" % (result1, pat_f, input_f, bindings))
        result2 = pat_match(pat_r ,input_r, result1)
        debout("result2 = %s pattern %s input = %s bindings = %s" % (result1, pat_r, input_r, result1))

        return result2

    debout(" *fail %s %s" % (pattern, input))
    return const.fail


def pattern_match(pattern, input):
    """
    引数が文字列なら、Listに分解してパターンマッチを行う。
    パターンマッチの結果から、const.no_binding を取りのぞく
    """

    pattern_s = to_list(pattern)
    input_s = to_list(input)

    bindings =  pat_match(pattern_s, input_s)

    if bindings == const.fail:
        return const.fail

    if bindings.get(True):
        del bindings[True]
    return bindings


def segment_match(pattern, input, bindings, start = 0):
    """複数の単語へのマッチングを行う"""
    var = first(pattern)
    rest_pattern = rest(pattern)
    binding_save = copy.copy(bindings)
    debout('in segment_match pattern = %s input = %s bindings = %s var = %s pat = %s start = %s' %
        (pattern, input, bindings, var, rest_pattern, start))

    if rest_pattern == []:
        r = match_variable(var, input, bindings)
        debout('segment_match return %s' % r)
        return r

    next_pattern = first(rest_pattern)
    if not next_pattern in input[start:]:
        debout('segmant_match return %s' % const.fail)
        return const.fail

    # start分ずらした文字列から、次にマッチングする場所を検索する。
    pos = input[start:].index(next_pattern) + start

    # マッチングに成功した部分の、後ろに対して再帰的にマッチングを行う。
    b2 = pat_match(rest_pattern, input[pos:], match_variable(var, input[0:pos], bindings))
    if b2 == const.fail:
        # 後半部分のマッチングに失敗したとき、bindingを元に戻し、開始位置をずらして再度セグメントマッチングを行う
        # 例:パターン'?*?x a b ?*?x' 入力 '1 2 a b a b 1 2 a b' の時は、パターンの非変数部分a を検索する。
        # 最初は、入力の3文字目のaを入力のaにbindするが、後半のマッチングに失敗したときは、5文字のaまでをbind
        # して、再度マッチングを行う。
        start_pos = pos + 1
        r = segment_match(pattern, input, binding_save, start = start_pos)
        debout('segmant_match return %s' % r)
        return r

    debout('segmant_match return B2 = %s' % b2)
    return b2

def is_segment_pattern(pattern):
    """petternがsegmentパターンかどうかの判定"""
    pat = first(pattern)
    if len(pat) < 2:
        debout ('in is_segment_pattern pattern = %s' % (pattern, ))
        return False

    r = (pat[0:2] == "?*")
    debout ('in is_segment_pattern pattern = %s pat = %s return %s' % (pattern, pat, r))
    return r

def do_test(pattern, input):
    print("> patten match(%s , %s)" % (pattern, input))
    print(pattern_match(pattern, input))
    print('')

def main():
    do_test('?*?x a b ?*?x', '1 2 a b a b 1 2 a b')
    do_test('?*?x a  ?*?x', '1 a b a 1 a b')
    do_test('?x is ?x', [['2', '+', '2'], 'is',['2', '+', '2']])
    do_test('?*?p need ?*?x', 'Mr Hulot and I need a vacation')

def eliza_prompt():
    print('> ')
    for line in sys.stdin:
        result = use_eliza_rules(line.rstrip())
        print ('%s' % result)


if __name__ == "__main__":
    tools.interactive_interpreter("YUKI.N>",  use_eliza_rules)
