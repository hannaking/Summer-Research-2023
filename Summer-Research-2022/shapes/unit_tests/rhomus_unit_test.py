import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.Rhombus import Rhombus
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice

class TestRhombus(unittest.TestCase):

    def test_verify_rectangle(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        shape = Rhombus(coords)
        #self.assertTrue(shape._verify_rectangle())

    def test_verify_rectangle2(self):
        coords = [Point(1, 1), Point(6, 1), Point(6, 6), Point(1, 6)]
        shape = Rhombus(coords)
       # self.assertTrue(shape._verify_rectangle())

    def test_verify_rectangle3(self):
        coords = [Point(1, 1), Point(6, 1), Point(6, 6), Point(1, 6)]
        shape = Rhombus(coords)
       # self.assertTrue(shape._verify_rectangle())
    
    def test_verify_rectangle4(self):
        coords = [Point(-2, -3), Point(1, -3), Point(1, 4), Point(-2, 4)]
        shape = Rhombus(coords)
       # self.assertTrue(shape._verify_rectangle())

    def test_verify_rectangle_too_many_coords(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), Point(2, 2)]
        shape = Rhombus(coords)
       # self.assertFalse(shape._verify_rectangle())

    def test_verify_rectangle_too_few_coords(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1)]
        shape = Rhombus(coords)
       # self.assertFalse(shape._verify_rectangle())

    def test_verify_rectangle_not_rectangle(self):
        coords = [Point(0, 0), Point(1, 0), Point(0, 1)]
        shape = Rhombus(coords)
       # self.assertFalse(shape._verify_rectangle())

    def test_verify_rectangle_not_rectangle_2(self):
        coords = [Point(2, 4), Point(0, 5), Point(5, 6), Point(3, 3)]
        shape = Rhombus(coords)
       # self.assertFalse(shape._verify_rectangle())

    
    def test_(self):
        points = [Point(0, 0), None, None, None]
        shape = Rhombus(points)
        scenarios = shape.coordinatize()
        #self.assertTrue(Rhombus.are_rhombi(scenarios))

        print(scenarios)
        
        gen = ShapeGenerator()
        lattice = Lattice(4)
        #gen.generate_by_lattice_traversal(lattice)
        #gen.show(scenarios, lattice)

if __name__ == "__main__":
    unittest.main()
