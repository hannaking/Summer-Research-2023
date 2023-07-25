import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.dart import Dart
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice
class TestDart(unittest.TestCase):  

    '''
    
    Helper Methods
    
    '''
    @staticmethod
    def show_failed(scenarios):
        for scenario in scenarios:
                if not Dart.are_darts([scenario]):
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

    Tests for coordinatize()

    '''

    #
    # one point tests
    #

    def test_coordinatize_1_point(self):
        points = [Point(0, 0), None, None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 160)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    #
    # two point tests
    #

    def test_coordinatize_2_point_right(self):
        points = [Point(0, 0), Point(1, 0), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_up_right(self):
        points = [Point(0, 0), Point(1, 1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_up(self):
        points = [Point(0, 0), Point(0, 1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_up_left(self):
        points = [Point(0, 0), Point(-1, 1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_left(self):
        points = [Point(0, 0), Point(-1, 0), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_down_left(self):
        points = [Point(0, 0), Point(-1, -1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_down(self):
        points = [Point(0, 0), Point(0, -1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point_down_right(self):
        points = [Point(0, 0), Point(1, -1), None, None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 16)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    #
    # three point tests
    #

    # both sides same side length
    #

    #acute

    def test_coordinatize_3_point_same_acute_right(self):
        points = [Point(0, 0), Point(1, 0.5), Point(0, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_right_flipped(self):
        points = [Point(0, 1), Point(1, 0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up_right(self):
        points = [Point(0, 0), Point(1, 2), Point(-1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up_right_flipped(self):
        points = [Point(-1, 1), Point(1, 2), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up(self):
        points = [Point(0, 0), Point(-0.5, 1), Point(-1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up_flipped(self):
        points = [Point(-1, 0), Point(-0.5, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up_left(self):
        points = [Point(0, 0), Point(-2, 1), Point(-1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_up_left_flipped(self):
        points = [Point(-1, -1), Point(-2, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_left(self):
        points = [Point(0, 0), Point(-1, -0.5), Point(0, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_left_flipped(self):
        points = [Point(0, -1), Point(-1, -0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_down_left(self):
        points = [Point(0, 0), Point(-1, -2), Point(1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_down_left_flipped(self):
        points = [Point(1, -1), Point(-1, -2), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_acute_down(self):
        points = [Point(0, 0), Point(0.5, -1), Point(1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_acute_down_flipped(self):
        points = [Point(1, 0), Point(0.5, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_down_right(self):
        points = [Point(0, 0), Point(2, -1), Point(1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_acute_down_right_flipped(self):
        points = [Point(1, 1), Point(2, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    # right

    def test_coordinatize_3_point_same_right_right(self):
        points = [Point(0, 0), Point(1, 1), Point(0, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_right_flipped(self):
        points = [Point(0, 2), Point(1, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_up_right(self):
        points = [Point(0, 0), Point(0, 1), Point(-1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_up_right_flipped(self):
        points = [Point(-1, 1), Point(0, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_up(self):
        points = [Point(0, 0), Point(-1, 1), Point(-2, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_up_flipped(self):
        points = [Point(-2, 0), Point(-1, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_right_up_left(self):
        points = [Point(0, 0), Point(-1, 0), Point(-1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_right_up_left_flipped(self):
        points = [Point(-1, -1), Point(-1, 0), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_right_left(self):
        points = [Point(0, 0), Point(-1, -1), Point(0, -2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_left_flipped(self):
        points = [Point(0, -2), Point(-1, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down_left(self):
        points = [Point(0, 0), Point(0, -1), Point(1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down_left_flipped(self):
        points = [Point(1, -1), Point(0, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down(self):
        points = [Point(0, 0), Point(1, -1), Point(2, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down_flipped(self):
        points = [Point(2, 0), Point(1, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down_right(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_right_down_right_flipped(self):
        points = [Point(1, 1), Point(1, 0), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    # obtuse

    def test_coordinatize_3_point_same_obtuse_right(self):
        points = [Point(0, 0), Point(0.5, 1), Point(0, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_right_flipped(self):
        points = [Point(0, 2), Point(0.5, 1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up_right(self):
        points = [Point(0, 0), Point(-0.5, 1.5), Point(-2, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up_right_flipped(self):
        points = [Point(-2, 2), Point(-0.5, 1.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up(self):
        points = [Point(0, 0), Point(-1, 0.5), Point(-2, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up_flipped(self):
        points = [Point(-2, 0), Point(-1, 0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up_left(self):
        points = [Point(0, 0), Point(-1.5, -0.5), Point(-2, -2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_up_left_flipped(self):
        points = [Point(-2, -2), Point(-1.5, -0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_obtuse_left(self):
        points = [Point(0, 0), Point(-0.5, -1), Point(0, -2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_left_flipped(self):
        points = [Point(0, -2), Point(-0.5, -1), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_down_left(self):
        points = [Point(0, 0), Point(0.5, -1.5), Point(2, -2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_down_left_flipped(self):
        points = [Point(2, -2), Point(0.5, -1.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_down(self):
        points = [Point(0, 0), Point(1, -0.5), Point(2, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_down_flipped(self):
        points = [Point(2, 0), Point(1, -0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_same_obtuse_down_right(self):
        points = [Point(0, 0), Point(1.5, 0.5), Point(2, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_same_obtuse_down_right_flipped(self):
        points = [Point(2, 2), Point(1.5, 0.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    # first side greater side length
    #

    def test_coordinatize_3_point_greater_right(self):
        points = [Point(0, 0), Point(1, 2), Point(0, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_up_right(self):
        points = [Point(0, 0), Point(-1, 2), Point(-1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_up(self):
        points = [Point(0, 0), Point(-2, 1), Point(-1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_up_left(self):
        points = [Point(0, 0), Point(-2, -1), Point(-1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_left(self):
        points = [Point(0, 0), Point(-1, -2), Point(0, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_down_left(self):
        points = [Point(0, 0), Point(1, -2), Point(1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_down(self):
        points = [Point(0, 0), Point(2, -1), Point(1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_greater_down_right(self):
        points = [Point(0, 0), Point(2, 1), Point(1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    # first side lesser side length
    #

    def test_coordinatize_3_point_lesser_right(self):
        points = [Point(0, 0), Point(1, -1), Point(0, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_up_right(self):
        points = [Point(0, 0), Point(1, 0), Point(-1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_up(self):
        points = [Point(0, 0), Point(1, 1), Point(-1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_up_left(self):
        points = [Point(0, 0), Point(0, 1), Point(-1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_left(self):
        points = [Point(0, 0), Point(-1, 1), Point(0, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_down_left(self):
        points = [Point(0, 0), Point(-1, 0), Point(1, -1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_down(self):
        points = [Point(0, 0), Point(-1, -1), Point(1, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_lesser_down_right(self):
        points = [Point(0, 0), Point(0, -1), Point(1, 1), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    # impossible

    def test_coordinatize_3_point_non_midpoint(self):
        points = [Point(0, 0), Point(1, 1.5), Point(0, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_point_non_midpoint_flipped(self):
        points = [Point(0, 2), Point(1, 1.5), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_point_right_uneven(self):
        points = [Point(0, 0), Point(0, 2), Point(1, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_point_right_uneven_flipped(self):
        points = [Point(1, 2), Point(0, 2), Point(0, 0), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)
    #
    # four point tests
    #

    def test_coordinatize_4_point_up(self):
        points = [Point(0, 0), Point(1, 2), Point(2, 0), Point(1, 0.5)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_4_point_right(self):
        points = [Point(0, 0), Point(-0.5, 1), Point(1.5, 0), Point(-0.5, -1)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        TestDart.show_failed(scenarios)
        self.assertTrue(Dart.are_darts(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_4_point_both_out(self):
        points = [Point(0, 1), Point(2, 0), Point(0, 2), Point(1, 0)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_both_midpoint(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_different_loc(self):
        points = [Point(0, 3), Point(1, 0), Point(2, 5), Point(3, 2)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_different_loc_alt(self):
        points = [Point(0, 3), Point(3, 2), Point(2, 5), Point(1, 0)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)
    
    def test_coordinatize_4_point_not_midpoint_up(self):
        points = [Point(0, 0), Point(1.5, 2), Point(2, 0), Point(1, 0.5)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)
    
    def test_coordinatize_4_point_not_midpoint_right(self):
        points = [Point(0, 0), Point(0.5, 1), Point(0, 2), Point(2, 1.5)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_not_outside_up(self):
        points = [Point(0, 0), Point(-1, 1.5), Point(0, 2), Point(1, 1.5)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_not_outside_right(self):
        points = [Point(0, 0), Point(-1.5, 1), Point(0, 2), Point(0.5, 1)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_irregular(self):
        points = [Point(0, 0), Point(-1, 1), Point(-2, 0), Point(-2, -0.5)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    #
    # wrong size tests
    #

    def test_coordinatize_5_input(self):
        points = [Point(0, 0), Point(1, 0.5), Point(2, 0), Point(1, 2), None]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_3_input(self):
        points = [Point(0, 0), Point(1, 0.5), Point(2, 0)]
        shape = Dart(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    '''
    
    Tests for _verify_dart()
    
    '''

    def test_verify_dart_right_upper(self):
        coords = [Point(0,0), Point(0,3), Point(3,3), Point(1,2)]
        shape = Dart(coords)
        self.assertTrue(shape._verify_dart())

    def test_verify_dart_right_lower(self):
        coords = [Point(0,2), Point(2,1), Point(1,1), Point(1,0)]
        shape = Dart(coords)
        self.assertTrue(shape._verify_dart())

    def test_verify_dart_obtuse_upper(self):
        coords = [Point(2,3), Point(5, 5), Point(1,4), Point(0,0)]
        shape = Dart(coords)
        self.assertTrue(shape._verify_dart())

    def test_verify_dart_obtuse_lower(self):
        coords = [Point(4,3), Point(0,4), Point(1,0), Point(2,2)]
        shape = Dart(coords)
        self.assertTrue(shape._verify_dart())

    def test_verify_dart_acute_upper(self):
        coords = [Point(3,1), Point(1,2), Point(2,0), Point(0,3)]
        shape = Dart(coords)
        self.assertTrue(shape._verify_dart())

    def test_verify_dart_too_many_coords(self):
        coords = [Point(0,0), Point(1,0), Point(0,1), Point(3,3), Point(4,4), Point(87, -1)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())

    def test_verify_dart_too_few_coords(self):
        coords = [Point(1,0), Point(0,1)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())

    def test_verify_dart_inner_not_symm(self):
        coords = [Point(0,3), Point(1,0), Point(1,1), Point(3,2)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())

    def test_verify_dart_no_symm(self):
        coords = [Point(1,0), Point(1,1), Point(2,2), Point(0,3)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())
    
    def test_verify_dart_overlap(self):
        coords = [Point(0,0), Point(0,1), Point(1,1), Point(0,1)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())
    
    def test_verify_dart_kite(self):
        coords = [Point(0,1), Point(0,2), Point(1,2), Point(2,0)]
        shape = Dart(coords)
        self.assertFalse(shape._verify_dart())

if __name__ == "__main__":
    unittest.main()