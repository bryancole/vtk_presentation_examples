#!/usr/bin/env python

import pyximport
pyximport.install()

from biot_savart import calc_wire_B_field
import unittest
import numpy as np

class TestBField(unittest.TestCase):
    def test_small_array(self):
        nodes = np.array([[-1,-1,0],
                        [-1,1,0],
                        [1,1,0],
                        [1,-1,0]], 'd')
        points = np.array([[0.1,0.2,0.3]], 'd')
        
        ret = calc_wire_B_field(nodes, points, 0.1)
        print ret
        self.assertEquals(ret[0][2],4.0)
        
if __name__=="__main__":
    unittest.main()
