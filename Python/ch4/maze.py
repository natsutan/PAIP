# -*- coding: utf-8 -*- 
# PAIP 4.13 The Maze Searching Domain

import gps2
import re

def make_maze_op_pair(first, second):
    f = str(first)
    s = str(second)
    op1 = make_maze_operator(f, s)
    op2 = make_maze_operator(s, f)
    return [op1, op2]

def make_maze_operator(here, there):
    op = gps2.operator('move from %s to %s' % (here, there),
                       (('at %s' % here),),
                       (('at %s' % there),),
                       (('at %s' % here),))
    return op

def make_maze_ops():
    maze_data = [(1,2),(2,3),(3,4),(4,9),(9,14),(9,8),(8,7),(7,12),(12,13),(12,11),(11,6),(11,16),(16,17),(17,22),(21,22),(22,23),(23,18),(23,24),(24,19),(19,20),(20,15),(15,10),(10,5),(20,25)]
    maze_ops = []
    for f, s in maze_data:
        op1, op2 = make_maze_op_pair(f,s)
        maze_ops.append(op1)
    maze_ops.append(op2)
    return maze_ops

def find_path(start, goal):
    maze_ops = make_maze_ops() 
    gps2.use(maze_ops)
    start_state = ('at '+str(start),)
    goal_state = ('at '+str(goal),)
    path =  gps2.gps2(start_state, goal_state, maze_ops)

    print_path(path, start)

def print_path(path, start):
    num = re.compile('%d+')

    for p in path:
        if p == 'start':
            print  "(%d" % start ,
        elif p[0] == 'executing':
            # 実行
            # 'move from 1 to 2'
            bufs = p[1].split()
            print bufs[4],
    print ")"

find_path(1,25)

