# -*- coding: utf-8 -*-
import sys

sys.path.append('../common/')
from cl import *

g_state = []
g_ops = []
g_deb = False
g_depth = 0

# operatorの定義
class operator:
    def __init__(self, action, preconds, add_list, del_list = ()):
        self.action = action
        self.preconds = preconds
        self.add_list = add_list
        self.del_list = del_list
        
    def info(self):
        print self.action
        print self.preconds
        print self.add_list
        print self.del_list

# The General Problem Solver
# Version 2
def gps2(state, goals, ops, deb = False):
    global g_state
    global g_ops
    global g_deb
    g_state = state
    g_deb = deb
    # g_ops = ops
    use(ops)
    first_state = ('start',) + state
    result = achieve_all(first_state, goals, [])
    return remove_if(is_atom, result)

def is_atom(x):
    return type(x) == str

def currying(f, x):
    """引数を2つ取る関数fから、一つ目の引数をxに固定した関数を作る"""
    return lambda y: f(x, y)

def achieve_all(state, goals, goal_stack):
    current_state = state
    for goal in goals:
        current_state = achieve(current_state, goal, goal_stack)
        if not current_state:
            return []
    # 全てのgoalを達成
    if subset_p(goals, current_state):
        # achieve呼び出し後のstateも、achieve呼び出し前のgoalを満たしている。
        return current_state
    else:
        # 状態が変わって、goalの条件を満たさなくなった。
        return []

def achieve(state, goal, goal_stack):
    global g_depth
    if goal in state:
        return state
    if goal in goal_stack:
        return []

    ops = find_all(goal, g_ops, appropriate_p)
    for op in ops:
        new_s = apply_op(state, goal, op, goal_stack)
        if new_s:
            return new_s

    return []

def find_all(item, seq, test_func):
    find = currying(test_func, item)
    return filter(find, seq)

def is_executing(l):
    """引数lの先頭が'executing'の判定"""
    return start_with(l, 'executing')

def start_with(l, x):
    """list の先頭がxであるかの判定"""
    if len(l) == 0:
        return False
    return l[0] == x;
                 
def apply_op(state, goal, op, goal_stack):
    print "Consider:%s " % op.action
    state2 = achieve_all(state, op.preconds, [goal,] + goal_stack)
    if state2 != []:
        print "Action:%s " % op.action
        new_state = remove_if(lambda x : x in op.del_list, state2) + list(op.add_list) 
        return new_state
    else:
        return None

def appropriate_p(goal, op):
    """opのadd-listにgoalがあるかどうかの判定"""
    return goal in op.add_list

def use(oplist):
    global g_ops
    g_ops = []
    for op in oplist:
        g_ops.append(convert_op(op))
    return len(g_ops)

def convert_op(op):
    if not(some(is_executing, op.add_list)):
        op.add_list = (('executing', op.action),) + op.add_list
    return op

def print_ops(ops):
    for op in ops:
        print op.action,
        print " ",
    print

def dbg(s):
    if g_deb:
        print s

def main():
    """教科書に出てくる例"""
    # opratorを追加するためにListへ
    school_ops = (
        operator('drive-son-to-school', 
                 ('son-at-home', 'car-works'),
                 ('son-at-school',),
                 ('son-at-home',)),
        operator('shop-installs-battery',
                 ('car-needs-battery', 'shop-knows-problem', 'shop-has-money'),
                 ('car-works',)),
        operator('tell-shop-problem',
                 ('in-communication-with-shop',),
                 ('shop-knows-problem',),),
        operator('telephon-shop',
                 ('know-phone-number',),
                 ('in-communication-with-shop',)),
        operator('look-up-number',
                 ('have-phone-book',),
                 ('know-phone-number',)),
        operator('give-shop-money',
                 ('have-money',),
                 ('shop-has-money',),
                 ('have-money',))
        )

    use(school_ops)

    # print gps2(('son-at-home',), ('son-at-school',), g_ops)
    # print gps2(('son-at-home','car-needs-battery', 'have-money'), ('son-at-school',), g_ops)

    # solved
    # print gps2(('son-at-home','car-works'), ('son-at-school',), g_ops)
    print gps2(('car-needs-battery','have-phone-book', 'have-money', 'son-at-home'), ('son-at-school',), g_ops)
        

if __name__ == "__main__":
     main()

