import unittest
import sys
import numpy as np

sys.path.insert(0, './Summer-Research-2022/')

from shapes.triangles.non_isosceles_right import NonIsoscelesRight
from pygeom import Axes3D, Point
from lattice import Lattice

class TestRightTriangle(unittest.TestCase):
    #---------------------------verify right triangle-----------------------#
    # *
    # | \
    # *--*
    def test_verify_right_triangle_true(self):
        coords = [(0,0), (1,0), (0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    # *--*
    # | /
    # *
    def test_verify_right_triangle_true_angle_top(self):
        coords = [(0,0), (1,2), (0, 2)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    #    *
    #  / |
    # *--*
    def test_verify_right_triangle_isosceles(self):
        coords = [(0,0), (1,0), (2,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    # *--*
    #  \ |
    #    *
    def test_verify_right_triangle_not_on_origin(self):
        coords = [(0, 1), (1, 0), (1, 1)]
        shape = NonIsoscelesRight(coords)
        self.assertTrue(shape._verify_right_triangle())

    #    *       but closed
    #   /
    #  /
    # *             obtuse angle
    #  \
    #   *
    def test_verify_right_triangle_obtuse(self):
        coords = [(0,0), (-2, 1), (3, 2)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    def test_verify_right_triangle_too_many_coords(self):
        coords = [(0,0), (1,0), (1,1), (0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

    def test_verify_right_triangle_too_few_coords(self):
        coords = [(0,0), (0,1)]
        shape = NonIsoscelesRight(coords)
        self.assertFalse(shape._verify_right_triangle())

if __name__ == "__main__":
    unittest.main()