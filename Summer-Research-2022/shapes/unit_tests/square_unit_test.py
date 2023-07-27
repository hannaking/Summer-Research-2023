import unittest
import sys
import numpy as np
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.square import Square
from shape_generator import ShapeGenerator

sys.path.append('Summer-Research-2022')

from lattice import Lattice

class TestSquare(unittest.TestCase):

    '''
    
    Helper Methods
    
    '''
    
    @staticmethod
    def show_failed(scenarios):
        for scenario in scenarios:
                if not Square.are_squares([scenario]):
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

    #-----------------------------------------init---------------------------------
    def test_square(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        shape = Square(coords)
        self.assertEqual(shape._points, coords)

    #-------------------------------------coordinatize-----------------------------
    # 1 in
    # 2 in
    # # 3 in - can make a square
    # # 3 in - can't make a square
    # 4 in - a square
    # 4 in - not a square

    def test_coordinatize_1_point(self):
        points = [Point(0, 0), None, None, None]
        shape = Square(points)
        scenarios = shape.coordinatize()
        TestSquare.show_failed(scenarios)
        self.assertTrue(Square.are_squares(scenarios))
        self.assertEqual(len(scenarios), 20)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_point(self):
        points = [Point(0, 0), Point(1, 0), None, None]
        shape = Square(points)
        scenarios = shape.coordinatize()
        TestSquare.show_failed(scenarios)
        self.assertTrue(Square.are_squares(scenarios))
        self.assertEqual(len(scenarios), 2)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_3_point_squareable(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), None]
        shape = Square(points)
        scenarios = shape.coordinatize()
        TestSquare.show_failed(scenarios)
        self.assertTrue(Square.are_squares(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_squareable(self):
        points = [Point(0, 0), Point(1, 0), Point(0, 1), None]
        shape = Square(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)

    def test_coordinatize_4_point_square(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        shape = Square(points)
        scenarios = shape.coordinatize()
        TestSquare.show_failed(scenarios)
        self.assertTrue(Square.are_squares(scenarios))
        self.assertEqual(len(scenarios), 1)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))
    
    def test_coordinatize_3_point_squareable(self):
        points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
        shape = Square(points)
        scenarios = shape.coordinatize()
        self.assertEqual(len(scenarios), 0)


    #-------------------------------------get second point-------------------------
    # normal

    def test_get_second_point(self):
        point1 = Point(0,0)
        sq = Square([point1, None, None, None])
        point2 = sq.get_second_point(point1)
        self.assertEqual(point2, Point(1,0))

    #----------------------------------verify square 3 points----------------------
    # not 4 points - too many, too few
    # point is None - 1, 2, 3
    # point 4 is None
    # sides not the same
    # existing angle not 90 or -90
    # can be a square

    def test_verify_square_3_points_can_square(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1)]
        shape = Square(coords)
        rots = shape.get_rotated_scenarios([coords])
        for points in rots:
            points.append(None)
            shape = Square(points)
            self.assertTrue(shape._verify_square_3_points())

    def test_verify_square_3_points_too_many(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), None, None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_too_few(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_1_is_none(self):
        coords = [None, Point(1, 0), Point(1, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_2_is_none(self):
        coords = [Point(0, 0), None, Point(1, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_3_is_none(self):
        coords = [Point(0, 0), Point(1, 0), None, None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_not_same_length(self):
        coords = [Point(0, 0), Point(1, 0), Point(3, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_obtuse(self):
        coords = [Point(0, 0), Point(1, 0), Point(2, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    def test_verify_square_3_points_acute(self):
        coords = [Point(0, 0), Point(1, 0), Point(0, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square_3_points())

    #--------------------------------------verify square---------------------------
    # not 4 points - too many, too few
    # any point is None
    # side 1 and 3 don't match
    # side 2 and 4 don't match
    # angle not 90 or -90
    # correct

    def test_verify_square_is_square(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        shape = Square(coords)
        rots = shape.get_rotated_scenarios([coords])
        for points in rots:
            shape = Square(points)
            self.assertTrue(shape._verify_square())

    def test_verify_square_too_many(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), None]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

    def test_verify_square_too_few(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 1)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

    def test_verify_square_long(self):
        coords = [Point(0, 0), Point(2, 0), Point(2, 1), Point(0, 1)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

    def test_verify_square_tall(self):
        coords = [Point(0, 0), Point(1, 0), Point(1, 2), Point(0, 2)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

    def test_verify_square_non_90(self):
        coords = [Point(0, 0), Point(1, 0), Point(2, 1), Point(1, 1)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

    def test_verify_square_different_sizes(self):
        coords = [Point(0, 0), Point(0, 2), Point(2, 2), Point(2, 1)]
        shape = Square(coords)
        self.assertFalse(shape._verify_square())

if __name__ == "__main__":
    unittest.main()
