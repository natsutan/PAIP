# -*- coding: utf-8 -*-
import unittest
from gps2 import *


class testAtom(unittest.TestCase):
    def testAtom(self):
        self.assertEqual(is_atom('str'), True)
        self.assertEqual(is_atom(('str',)), False)

class testIsExecutin(unittest.TestCase):
    def testIsExecuting(self):
        l1 = ['executing', 'aaa']
        l2 = []
        l3 = ['abc', 'executing']
        self.assert_(is_executing(l1))
        self.assert_(not is_executing(l2))
        self.assert_(not is_executing(l3))
        pass

class testStartWith(unittest.TestCase):
    def testStartWith(self):
        l = [1,2,3]
        self.assert_(not start_with([], 1))
        self.assert_(start_with(l, 1))
        self.assert_(not start_with(l, 4))
        self.assert_(not start_with(l, 2))

class testUse(unittest.TestCase):
    def testUse(self):
        l = [1,2,3]
        self.assertEqual(use(l), len(l))

class testAppropriateP(unittest.TestCase):
    def testAppropriateP(self):
        op1 = operator('action', ('preconds',), ('add1', 'add2', 'add3'), ('dellist',))
        self.assert_(appropriate_p('add1', op1))
        self.assert_(appropriate_p('add2', op1))
        self.assert_(appropriate_p('add3', op1))
        self.assert_(not appropriate_p('add4', op1))


#def achieve_all(state, goals, goal_stack):
#def achieve(state, goal, goal_stack):
#def apply_op(state, goal, op, goal_stack):

        
if __name__ == '__main__':
    unittest.main()



