import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.righttrapezoid import RightTrapezoid
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice

class TestRightTrapezoid(unittest.TestCase):
    #-----------------------------------------------Init--------------------------------------------
    def test_init(self):
        pass

    #--------------------------------------------Coordinatize--------------------------------------------
    # 4 in - can make a rt
    # 4 in - can't make a rt
    # 3 in - can make an rt
    # 3 in - can't make a rt
    # 2 in
    # 1 in

    #--------------------------------------------get second point--------------------------------------------
    # normal

    #--------------------------------------------get third points--------------------------------------------
    # check len and values
    # normal

    #------------------------------------------are right trapezoids--------------------------------------------
    
    #-----------------------------------------are right trapezoidable--------------------------------------------
    
    #-----------------------------------------------get other angle--------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def test_verify_righttrapezoid(self):
        coords = [Point(0, 0), Point(0.5, 0.866), Point(0.933, 0.616), Point(0.683, 0.183)]
        shape = RightTrapezoid(coords)
        self.assertTrue(shape._verify_righttrapezoid())


    #
    def test_(self):
        points = [Point(0, 0), Point(1, 0), None, None]
        shape = RightTrapezoid(points)
        scenarios = shape.coordinatize()
        #self.assertTrue(Square.(scenarios))
        
        gen = ShapeGenerator()
        lattice = Lattice(4)
        gen.generate_by_lattice_traversal(lattice)
        gen.show(scenarios, lattice)

if __name__ == "__main__":
    unittest.main()
