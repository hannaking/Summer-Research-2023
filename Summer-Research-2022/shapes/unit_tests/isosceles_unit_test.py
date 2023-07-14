import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from triangles.isosceles import Isosceles
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice

class TestIsoscelesTriangle(unittest.TestCase):

    #right iso, obtuse iso, acute iso, too many coords, too few coords, not iso (prob 2)
    def test_verify_isosceles_right_iso(self):
        coords = [Point(0,0), Point(1,0), Point(0,1)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_obtuse_iso(self):
        coords = [Point(0,0), Point(1, 10), Point(1, -10)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_acute_iso(self):
        coords = [Point(0,0), Point(2, 1), Point(2, -1)]
        shape = Isosceles(coords)
        self.assertTrue(shape._verify_isosceles_triangle())

    def test_verify_isosceles_too_many_coords(self):
        coords = [Point(0,0), Point(1,0), Point(0,1), Point(3,3), Point(4,4), Point(87, -1)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_too_few_coords(self):
        coords = [Point(1,0), Point(0,1)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_not_iso(self):
        coords = [Point(0,0), Point(-2, 1), Point(3, 2)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    def test_verify_isosceles_not_iso_2(self):
        coords = [Point(2, 4), Point(0, 5), Point(5, 6)]
        shape = Isosceles(coords)
        self.assertFalse(shape._verify_isosceles_triangle())

    #
    def test_(self):
        points = [Point(0, 0), Point(1, 0), None]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))
        
        gen = ShapeGenerator()
        lattice = Lattice(3)
        gen.generate_by_lattice_traversal(lattice)
        gen.show(scenarios, lattice)

if __name__ == "__main__":
    unittest.main()