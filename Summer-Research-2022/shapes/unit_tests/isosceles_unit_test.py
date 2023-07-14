import unittest
import sys
import numpy as np
import math

sys.path.insert(0, './Summer-Research-2022/')

from shapes.triangles.isosceles import Isosceles
from pygeom import Axes3D, Point
from lattice import Lattice

class TestIsoscelesTriangle(unittest.TestCase):
    #right iso, obtuse iso, acute iso, too many coords, too few coords, not iso (prob 2)
    def test_verify_isosceles_right_iso(self):
        coords = [(0,0), (1,0), (0,1)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_obtuse_iso(self):
        coords = [(0,0), (1, 10), (1, -10)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_acute_iso(self):
        coords = [(0,0), (2, 1), (2, -1)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_too_many_coords(self):
        coords = [(0,0), (1,0), (0,1), (3,3), (4,4), (87, -1)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_too_few_coords(self):
        coords = [(1,0), (0,1)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_not_iso(self):
        coords = [(0,0), (-2, 1), (3, 2)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_not_iso_2(self):
        coords = [(2, 4), (0, 5), (5, 6)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

if __name__ == "__main__":
    unittest.main()