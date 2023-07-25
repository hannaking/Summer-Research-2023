import unittest
import sys
import numpy as np

sys.path.insert(0, './Summer-Research-2022/')

from shapely.geometry import *
from shapes.triangles.non_isosceles_right import NonIsoscelesRight
from lattice import Lattice

class TestRightTriangle(unittest.TestCase):
    #---------------------------verify right triangle-----------------------#
    # *
    # | \
    # *--*
    def test_verify_right_triangle_true(self):
        coords = [Point(0,0), Point(1,0), Point(0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    # *--*
    # | /
    # *
    def test_verify_right_triangle_true_angle_top(self):
        coords = [Point(0,0), Point(1,2), Point(0, 2)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    #    *
    #  / |
    # *--*
    def test_verify_right_triangle_isosceles(self):
        coords = [Point(0,0), Point(1,0), Point(2,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    # *--*
    #  \ |
    #    *
    def test_verify_right_triangle_not_on_origin(self):
        coords = [Point(0, 1), Point(1, 0), Point(1, 1)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    #    *       but closed
    #   /
    #  /
    # *             obtuse angle
    #  \
    #   *
    def test_verify_right_triangle_obtuse(self):
        coords = [Point(0,0), Point(-2, 1), Point(3, 2)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    def test_verify_right_triangle_too_many_coords(self):
        coords = [Point(0,0), Point(1,0), Point(1,1), Point(0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    def test_verify_right_triangle_too_few_coords(self):
        coords = [Point(0,0), Point(0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

if __name__ == "__main__":
    unittest.main()