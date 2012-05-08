# -*- coding: utf-8 -*-
import gps2

def move_op(obj, dst, src):
    action = "move " + obj + " from " + dst + " to " + src
    preconds = [ on('space', obj), on('space', src), on(obj, dst)]
    add_list = move_ons(obj, dst, src)
    del_list = move_ons(obj, src, dst)
    return gps2.operator(action, preconds, add_list, del_list)

def is_table(src):
    return src == 'table'

def move_ons(obj, src, dst):
    if is_table(src):
        return (on(obj, dst),)
    else:
        return (on(obj, dst), on('space', src))

def on(top, bottom):
    assert bottom != 'space'
    assert top != bottom
    return top + " on " + bottom

def make_block_ops(blocks):
    ops = []
    for (a, b, c) in comb3(blocks):
        ops.append(move_op(a, b, c))
    return ops
           

def comb3(l):
    for a in l:
        for b in l:
            if a != b:
                yield (a, 'table', b)
                yield (a, b, 'table')
                for c in l:
                    if a != c and b != c:
                        yield (a, b, c)


def all_object_on_table(l):
    r = []
    for item in l:
        r.append(on(item, 'table'))
    return r

def all_top_is_space(l):
    r = []
    for item in l:
        r.append(on('space', item))
    return r


# The simplest possible problem
print "----- 1 -----"
blocks = ['a','b']
ops = make_block_ops(blocks)
gps2.use(ops)
start1 = tuple(all_object_on_table(blocks) + all_top_is_space(blocks) + [on('space', 'table'),])
print start1
goal1 = [on('a', 'b'), on('b', 'table')]
print gps2.gps2(start1, goal1, ops)
print ""

# 3 blocks
print "----- 2 -----"
blocks = ['a','b','c']
ops = make_block_ops(blocks)

gps2.use(ops)
start2 = tuple([on('a', 'b'), on('b', 'c'), on('c', 'table'),  on('space', 'a'), on('space', 'table')])
print start2
goal2 = [on('a', 'table'), on('b', 'a')]
print gps2.gps2(start2, goal2, ops)
print ""

# Clobbered Sibling Problem
print "----- 3 -----"
blocks = ['a','b','c']
ops = make_block_ops(blocks)

gps2.use(ops)
start2 = tuple([on('a', 'b'), on('b', 'c'), on('c', 'table'),  on('space', 'a'), on('space', 'table')])
goal2 = [on('a', 'table'), on('b', 'a'), on('c', 'b')]
print gps2.gps2(start2, goal2, ops)

