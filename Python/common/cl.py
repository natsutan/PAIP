# -*- coding: utf-8 -*-


# lispの関数
def some(f, l):
    """list l の要素に対してfを呼び出し、論理和を取って結果を返す"""
    return reduce(lambda x, y: x or y, map(f, l), False)

def every(f, l):
    """list l の要素に対してfを呼び出し、論理積を取って結果を返す"""
    return reduce(lambda x, y: x and y, map(f, l))

def union(x, y):
    """引数の和集合を取る"""
    return list(set(x).union(set(y)))

def difference(x, y):
    """引数の差集合を取る"""
    return list(set(x).difference(set(y)))

def remove_if(p, l):
    """lからpの条件に合ったものを削除"""
    return [x for x in l if not p(x)]

def subset_p(l1, l2):
    """l1の要素がl2に全て含まれていればTrue"""
    return set(l1).issubset(set(l2))
