import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.parallelogram import Parallelogram
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice
class TestParallelogram(unittest.TestCase):  
    '''
    
    Helper Methods
    
    '''
    @staticmethod
    def show_failed(scenarios):
        for scenario in scenarios:
                if not Parallelogram.are_parallelograms([scenario]):
                    gen = ShapeGenerator()
                    lattice = Lattice(4)
                    gen.generate_by_lattice_traversal(lattice)
                    gen.show([scenario], lattice)

    @staticmethod
    def show(scenarios):
        gen = ShapeGenerator()
        lattice = Lattice(4)
        gen.generate_by_lattice_traversal(lattice)
        gen.show(scenarios, lattice)

    '''

    coordinatize() tests

    '''

    def test_coordinatize_1_point(self):
        points = [Point(0, 0), None, None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 240)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_right(self):
        points = [Point(0, 0), Point(1, 0), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_up_right(self):
        points = [Point(0, 0), Point(1, 1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_up(self):
        points = [Point(0, 0), Point(0, 1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_up_left(self):
        points = [Point(0, 0), Point(-1, 1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_left(self):
        points = [Point(0, 0), Point(-1, 0), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_2_points_down_left(self):
        points = [Point(0, 0), Point(-1, -1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_down(self):
        points = [Point(0, 0), Point(0, -1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_down_right(self):
        points = [Point(0, 0), Point(1, -1), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 24)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points_same(self):
        points = [Point(0, 0), Point(0, 0), None, None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_points(self):
        points = [Point(0, 0), Point(1, math.pi), Point(math.cos(0.124), math.e), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_points_zero_degrees(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 0.5), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_points_180_degrees(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 2), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_points_2_points_same(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 2), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_points_all_points_same(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 0), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_points_parallelogram(self):
        points = [Point(0, 0), Point(2, 0), Point(3, 1), Point(1, 1)]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        TestParallelogram.show_failed(scenarios)
        self.assertTrue(Parallelogram.are_parallelograms(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_4_points_trapezoid(self):
        points = [Point(0, 0), Point(3, 0), Point(2, 1), Point(1, 1)]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_points_irregular(self):
        points = [Point(0, 0), Point(1, -1), Point(2, 2), Point(0, 1)]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_points_psudo_triangle(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 1)]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_points_overlapping(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 0), Point(1, 1)]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    '''

    get_second_point_scenarios() tests

    '''

    def test_get_second_point_scenarios(self):
        point1_a = Point(0, 0)
        point1_b = Point(1, 1)
        
        scenarios = [[point1_a, None, None, None], [point1_b, None, None, None]]
        
        shape = Parallelogram([point1_a])
        new_scenarios = shape.get_second_point_scenarios(scenarios)

        self.assertEqual(type(new_scenarios), list)
        self.assertEqual(len(new_scenarios), 2)
        for new_scenario in new_scenarios:
            self.assertEqual(type(new_scenario), list)
            self.assertEqual(len(new_scenario), 4)
            for i, point in enumerate(new_scenario):
                if i <= 1:
                    self.assertEqual(type(point), Point)
                else:
                    self.assertEqual(point, None)
        
        self.assertEqual(new_scenarios[0][1].x, 1)
        self.assertEqual(new_scenarios[1][1].x, 2)

    '''

    get_third_point_scenarios() tests

    '''

    def test_get_third_point_scenarios(self):
        point1_a = Point(0, 0)
        point1_b = Point(1, 1)
        point2_a = Point(1, 1)
        point2_b = Point(2, 2)
        
        scenarios = [[point1_a, point2_a, None, None], [point1_b, point2_b, None, None]]
        
        shape = Parallelogram([point1_a])
        new_scenarios = shape.get_third_point_scenarios(scenarios)
        
        self.assertEqual(type(new_scenarios), list)
        self.assertEqual(len(new_scenarios), 48)
        for new_scenario in new_scenarios:
            self.assertEqual(type(new_scenario), list)
            self.assertEqual(len(new_scenario), 4)
            for i, point in enumerate(new_scenario):
                if i <= 2:
                    self.assertEqual(type(point), Point)
                else:
                    self.assertEqual(point, None)

    '''

    get_fourth_point_scenarios() tests

    '''

    def test_get_fourth_point_scenarios(self):
        point1_a = Point(0, 0)
        point1_b = Point(1, 1)
        point2_a = Point(1, 1)
        point2_b = Point(2, 2)
        point3_a = Point(2, 3)
        point3_b = Point(3, 4)
        
        scenarios = [[point1_a, point2_a, point3_a, None], [point1_b, point2_b, point3_b, None]]
        
        shape = Parallelogram([point1_a])
        new_scenarios = shape.get_fourth_point_scenarios(scenarios)
        
        self.assertEqual(type(new_scenarios), list)
        self.assertEqual(len(new_scenarios), 2)
        for new_scenario in new_scenarios:
            self.assertEqual(type(new_scenario), list)
            self.assertEqual(len(new_scenario), 4)
            for i, point in enumerate(new_scenario):
                    self.assertEqual(type(point), Point)

        self.assertAlmostEqual(new_scenarios[0][3].x, 1)
        self.assertAlmostEqual(new_scenarios[0][3].y, 2)

        self.assertAlmostEqual(new_scenarios[1][3].x, 2)
        self.assertAlmostEqual(new_scenarios[1][3].y, 3)

    def test_verify_parallelogram_parallelogram(self):
        points = [Point(0, 0), Point(2, 0), Point(3, 1), Point(1, 1)]
        shape = Parallelogram(points)
        
        self.assertTrue(shape._verify_parallelogram())

    '''

    _verify_parallelogram() tests

    '''

    def test_verify_parallelogram_trapezoid(self):
        points = [Point(0, 0), Point(3, 0), Point(2, 1), Point(1, 1)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    def test_verify_parallelogram_irregular(self):
        points = [Point(0, 0), Point(1, -1), Point(2, 2), Point(0, 1)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    def test_verify_parallelogram_psudo_triangle(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 1)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    def test_verify_parallelogram_overlapping(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 0), Point(1, 1)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    def test_verify_parallelogram_3_overlap(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 0), Point(1, 1)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    def test_verify_parallelogram_all_overlap(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram())

    '''

    _verify_parallelogram_3_points() tests

    '''

    def test_verify_parallelogram_3_points_parallelogram(self):
        points = [Point(0, 0), Point(2, 0), Point(3, 1), None]
        shape = Parallelogram(points)
        
        self.assertTrue(shape._verify_parallelogram_3_points())

    def test_verify_parallelogram_3_points_zero_degrees(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 0.5), None]
        shape = Parallelogram(points)
        
        self.assertFalse(shape._verify_parallelogram_3_points())

    def test_verify_parallelogram_3_points__180_degrees(self):
        points = [Point(0, 0), Point(0, 1), Point(0, 2), None]
        shape = Parallelogram(points)
       
        self.assertFalse(shape._verify_parallelogram_3_points())

    def test_coordinatize_3_points_2_points_same(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 2), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_points_all_points_same(self):
        points = [Point(0, 0), Point(0, 0), Point(0, 0), None]
        shape = Parallelogram(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

if __name__ == "__main__":
    unittest.main()