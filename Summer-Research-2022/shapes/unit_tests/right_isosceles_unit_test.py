import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *
from triangles.isosceles_right import IsoscelesRight

sys.path.append("Summer-Research-2022")

from lattice import Lattice

class TestIsoscelesTriangle(unittest.TestCase):
    #right iso, obtuse iso, acute iso, too many coords, too few coords, not iso (prob 2)
    def test_verify_right_isosceles_triangle_right_iso(self):
        coords = [Point(0,0), Point(1,0), Point(0,1)]
        shape = IsoscelesRight(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_obtuse_iso(self):
        coords = [Point(0,0), Point(1, 10), Point(1, -10)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_acute_iso(self):
        coords = [Point(0,0), Point(2, 1), Point(2, -1)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_too_many_coords(self):
        coords = [Point(0,0), Point(1,0), Point(0,1), Point(3,3), Point(4,4), Point(87, -1)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_too_few_coords(self):
        coords = [Point(1,0), Point(0,1)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_not_iso(self):
        coords = [Point(0,0), Point(-2, 1), Point(3, 2)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_right_isosceles_triangle_not_iso_2(self):
        coords = [Point(2, 4), Point(0, 5), Point(5, 6)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    # *
    # | \
    # *--*
    def test_verify_right_isosceles_triangle_true(self):
        coords = [Point(0,0), Point(1,0), Point(0,1)]
        shape = IsoscelesRight(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    # *--*
    # | /
    # *
    def test_verify_right_isosceles_triangle_right_not_iso(self):
        coords = [Point(0,0), Point(1,2), Point(0, 2)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    #    *
    #  / |
    # *--*
    def test_verify_right_isosceles_triangle_right_not_iso2(self):
        coords = [Point(0,0), Point(1,0), Point(2,1)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    # *--*
    #  \ |
    #    *
    def test_verify_right_isosceles_triangle_not_on_origin(self):
        coords = [Point(0, 1), Point(1, 0), Point(1, 1)]
        shape = IsoscelesRight(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    #    *       but closed
    #   /
    #  /
    # *             obtuse angle
    #  \
    #   *
    def test_verify_right_isosceles_triangle_obtuse(self):
        coords = [Point(0,0), Point(-2, 1), Point(3, 2)]
        shape = IsoscelesRight(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

if __name__ == "__main__":
    unittest.main()