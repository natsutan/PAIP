# -*- coding: utf-8 -*-
import unittest
from cl import *

def even(x):
    return x % 2 == 1


class testRemoveIf(unittest.TestCase):
    def testNormal(self):
        l = (1,2,3,4,5)
        ret = remove_if(lambda x:x < 3, l)
        self.assertEqual(ret, [3, 4, 5])

        ret = remove_if(even, l)
        self.assertEqual(ret, [2, 4])
        

class testSubsetP(unittest.TestCase):
    def testSubsetP(self):
        l1 = (1,2,3)
        l2 = (1,2,3,4)
        l3 = (3,4)

        self.assert_(subset_p(l1,l2))
        self.assert_(not subset_p(l2,l1))
        self.assert_(not subset_p(l1,l3))
        self.assert_(subset_p(l3,l2))

if __name__ == '__main__':
    unittest.main()

