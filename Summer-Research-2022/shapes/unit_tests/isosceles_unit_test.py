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

    # 1 point integer, 1 point irrational, 2 points integers, 2 points irrational, 3 points isosceles, 3 points non isosceles,
    # four points
    def test_coordinatize_simple_1_point(self):
        points = [Point(math.pi, math.cos(34)), None, None]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        self.assertEqual(len(scenarios), 180)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_simple_1_point(self):
        points = [Point(0, 0), None, None]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))
        
        gen = ShapeGenerator()
        lattice = Lattice(3)
        gen.generate_by_lattice_traversal(lattice)
        #gen.show(scenarios, lattice)

        self.assertEqual(len(scenarios), 180)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_simple_2_points(self):
        points = [Point(0, 0), Point(1, 0), None]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        self.assertEqual(len(scenarios), 18)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_irrational_2_points(self):
        points = [Point(math.pi, math.cos(34)), Point(math.e, math.log2(14)), None]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertEqual(len(scenarios), 18)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_isosceles_3_points(self):
        points = [Point(0, 0), Point(2, 0), Point(1, 1)]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_non_isosceles_3_points(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 2)]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_overlapping_4_points(self):
        points = [Point(0, 0), Point(0, 1), Point(1, 1), Point(0, 0)]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_distict_4_points(self):
        points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
        shape = Isosceles(points)
        scenarios = shape.coordinatize()

        self.assertEqual(len(scenarios), 0)

    #integer, irrational
    def test_get_second_point_integer(self):
        point = Point(0, 0)
        shape = Isosceles(point)
        second_point = shape.get_second_point(point)
        
        self.assertEqual(second_point, Point(1, 0))

    def test_get_second_point_irrational(self):
        point = Point(math.pi, math.cos(34))
        shape = Isosceles([point, None, None])
        second_point = shape.get_second_point(point)

        self.assertEqual(second_point, Point(math.pi+1, math.cos(34)))

    #integers, irrational
    def test_get_third_points_integers(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        shape = Isosceles([point1, point2, None])
        third_points = shape.get_third_points(point1, point2)
        
        scenarios = []
        for third_point in third_points:
            scenarios.append([point1, point2, third_point])

        self.assertEqual(len(scenarios), 18)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
        
    def test_get_third_points_irrational(self):
        point1 = Point(math.pi, math.cos(34))
        point2 = Point(math.e, math.log2(14))
        shape = Isosceles([point1, point2, None])
        third_points = shape.get_third_points(point1, point2)
        
        scenarios = []
        for third_point in third_points:
            scenarios.append([point1, point2, third_point])

        self.assertEqual(len(scenarios), 18)
        self.assertTrue(Isosceles.are_isosceles_triangles(scenarios))

        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
        

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

    

if __name__ == "__main__":
    unittest.main()