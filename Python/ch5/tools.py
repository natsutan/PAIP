#-*- coding: utf-8 -*-
__author__ = 'Natsutani'
import sys
import random

# lispの関数
def some(f, l):
    """list l の要素に対してfを呼び出し、論理和を取って結果を返す"""
    return reduce(lambda x, y: x or y, map(f, l), False)

def every(f, l):
    """list l の要素に対してfを呼び出し、論理積を取って結果を返す"""
    return reduce(lambda x, y: x and y, map(f, l))

def currying(f, x):
    """引数を2つ取る関数fから、一つ目の引数をxに固定した関数を作る"""
    return lambda y: f(x, y)

def union(x, y):
    """引数の和集合を取る"""
    return list(set(x).union(set(y)))

def difference(x, y):
    """引数の差集合を取る"""
    return list(set(x).difference(set(y)))

def find_all(item, seq, test_func):
    find = currying(test_func, item)
    return filter(find, seq)

def sublis(dic, l):
    result = []
    for e in l:
        et = '?*'+e
        if et in dic:
            result.append(dic[et][0])
        else:
            result.append(e)
    return result


def ramdom_elt(l):
    length = len(l)
    i = random.randrange(length)
    return l[i]

# interactive 環境
def prompt(prompt_str = '> '):
    print (prompt_str, end='')
    sys.stdout.flush()

def pyloop():
    interactive_iinterpreter('> ', eval)

def interactive_interpreter (prompt_str, transformer):
    prompt(prompt_str)
    for line in sys.stdin:
        if line.rstrip() == "exit":
            return
        print("%s" % transformer(line))
        prompt(prompt_str)

