# -*- coding: utf-8 -*-
g_state = []
g_ops = []

# operatorの定義
class operator:
    def __init__(self, action, preconds, add_list, del_list = ()):
        self.action = action
        self.preconds = preconds
        self.add_list = add_list
        self.del_list = del_list

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

# The General Problem Solver
def gps(state, goals, ops):
    global g_state
    global g_ops
    g_state = state
    g_ops = ops
    return every(achieve, goals) and goals in g_state

def achieve(goal):
    if goal in g_state: # g_stateにgoalが含まれていれば、goalまでに必要な全てのoperationを実行している。
        return True
    # goalを含むoperationを探す。全てのoperationのadd_listがgoalを含まない場合はFalseを返す。
    return some(apply_op, (find_all(goal, g_ops, appropriate)))

def appropriate(goal, op):
    """ opration opのadd_listにgoalがあるか（goalを実現するために必要なactionがあるか）を調べる"""
    try:
        index = op.add_list.index(goal)
        return op.add_list[index:]
    except ValueError:
        return ()

def apply_op(op):
    global g_state
    ret = False
    if every(achieve, op.preconds):
        # operation opの前提条件を全て達成しているなら、acitonを実行する。
        print "Execute ",
        print op.action.encode('utf-8')
        g_state = difference(g_state, op.del_list) # del_listに含まれる状態を削除
        g_state = union(g_state, op.add_list)      # add_listに含まれる状態を追加
        ret = True
    return ret

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

    # solved
    print gps(('son-at-home','car-works'),
              ('son-at-school',),
              school_ops)
    #solved
    print gps(('son-at-home', 'car-needs-battery', 'have-money', 'have-phone-book'),
              ('son-at-school',),
              school_ops)

    # solved
    print gps(('son-at-home', 'car-needs-battery', 'shop-knows-problem', 'shop-has-money'),          
              ('son-at-school',),
              school_ops)

    # nil
    print gps(('son-at-home', 'car-needs-battery', 'have-money'),
              ('son-at-school',),
              school_ops)

    # 4.7 The Globbered Sibling Goal Problem
    print gps(('son-at-home', 'car-needs-battery', 'have-money', 'have-phone-book'),
              ('have-money', 'son-at-school'),
              school_ops)

    # 4.9 The Recursive Subgoal Problem
    new_school_ops = school_ops + (operator('ask-phone-number', 
                                           ('in-communication-with-shop',),
                                           ('know-phone-number',),
                                           ),)
    print gps(('son-at-home', 'car-needs-battery', 'have-money'),
              ('son-at-school',),
              new_school_ops)

if __name__ == "__main__":
     main()
     
