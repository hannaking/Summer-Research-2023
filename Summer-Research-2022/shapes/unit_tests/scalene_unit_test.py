import unittest
import sys
import numpy as np
import math

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from shapes.triangles.scalene import Scalene
from pygeom import Axes, Point
from lattice import Lattice

class TestScaleneTriangle(unittest.TestCase):
    #    *       but closed
    #   /
    #  /
    # *             obtuse angle
    #  \
    #   *
    def test_verify_scalene_triangle_true(self):
        coords = [(0,0), (-2,11), (32, 2)]
        shape = Scalene(coords)
        self.assertTrue(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_true_2(self):
        coords = [(8,6), (-5,15), (27,-5)]
        shape = Scalene(coords)
        self.assertTrue(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_true_3(self):
        coords = [(0,10), (20,0), (30,30)]
        shape = Scalene(coords)
        self.assertTrue(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_equilateral(self):
        coords = [(1,0), (3, (2*math.sqrt(3))), (5,0)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_equilateral_2(self):
        coords = [(3,0), (0, (3*math.sqrt(3))), (-3,0)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_too_large(self):
        coords = [(0,0), (1,0), (0,1), (1,1)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    def test_verify_scalene_triangle_too_small(self):
        coords = [(0,0), (1,0)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    # pictures NOT to scale

    # *
    # | \
    # *--*
    def test_verify_scalene_triangle_right(self):
        coords = [(0,0), (1,0), (0,1)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    # *--*
    # | /
    # *
    def test_verify_scalene_triangle_right_true_angle_top(self): # it is scalene
        coords = [(0,0), (1,2), (0, 2)]
        shape = Scalene(coords)
        self.assertTrue(shape._verify_scalene_triangle())

    #    *
    #  / |
    # *--*
    def test_verify_scalene_triangle_isosceles(self):
        coords = [(0,0), (1,0), (1,1)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

    # *--*
    #  \ |
    #    *
    def test_verify_scalene_triangle_right_not_on_origin(self):
        coords = [(0, 1), (1, 0), (1, 1)]
        shape = Scalene(coords)
        self.assertFalse(shape._verify_scalene_triangle())

if __name__ == "__main__":
    unittest.main()