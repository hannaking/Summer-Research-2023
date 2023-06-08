from email.mime import base
import unittest
import sys
import numpy as np
import math

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from shapes.triangles.equilateral import Equilateral
from shapely.geometry import *
from lattice import Lattice
from shapes.geometry import Geometry

class TestEquilateralTriangle(unittest.TestCase):
 # ----------------------------- get second points --------------------------#
    # origin
    def test_get_second_points_0_0(self):
        points = [Point(0,0), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(1,0),                              # 0
            Point(math.sqrt(3)/2, 1/2),              # 30
            Point(math.sqrt(2)/2, math.sqrt(2)/2),   # 45
            Point(1/2, math.sqrt(3)/2),              # 60
            Point(0,1),                              # 90
            Point (-1,0),                            # 180
            Point (math.sqrt(3)/2, -1/2),            # -30
            Point (math.sqrt(2)/2, -math.sqrt(2)/2), # -45
            Point (1/2, -math.sqrt(3)/2),            # -60
            Point (0,-1)                             # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # right x-axis
    def test_get_second_points_1_0(self):
        points = [Point(1,0), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(2,0),                                  # 0
            Point(math.sqrt(3)/2 + 1, 1/2),              # 30
            Point(math.sqrt(2)/2 + 1, math.sqrt(2)/2),   # 45
            Point(3/2, math.sqrt(3)/2),                  # 60
            Point(1,1),                                  # 90
            Point (0,0),                                 # 180
            Point (math.sqrt(3)/2 + 1, -1/2),            # -30
            Point (math.sqrt(2)/2 + 1, -math.sqrt(2)/2), # -45
            Point (3/2, -math.sqrt(3)/2),                # -60
            Point (1,-1)                                 # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # quadrant 1
    def test_get_second_points_1_1(self):
        points = [Point(1,1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(2,1),                                      # 0
            Point(math.sqrt(3)/2 + 1, 3/2),                  # 30
            Point(math.sqrt(2)/2 + 1, math.sqrt(2)/2 + 1),   # 45
            Point(3/2, math.sqrt(3)/2 + 1),                  # 60
            Point(1,2),                                      # 90
            Point (0,1),                                     # 180
            Point (math.sqrt(3)/2 + 1, 1/2),                 # -30
            Point (math.sqrt(2)/2 + 1, -math.sqrt(2)/2 + 1), # -45
            Point (3/2, -math.sqrt(3)/2 + 1),                # -60
            Point (1,0)                                      # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            print(i)
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)
    
    # up y-axis
    def test_get_second_points_0_1(self):
        points = [Point(0,1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(1,1),                                  # 0
            Point(math.sqrt(3)/2, 3/2),                  # 30
            Point(math.sqrt(2)/2, math.sqrt(2)/2 + 1),   # 45
            Point(1/2, math.sqrt(3)/2 + 1),              # 60
            Point(0,2),                                  # 90
            Point (-1,1),                                # 180
            Point (math.sqrt(3)/2, 1/2),                 # -30
            Point (math.sqrt(2)/2, -math.sqrt(2)/2 + 1), # -45
            Point (1/2, -math.sqrt(3)/2 + 1),            # -60
            Point (0,0)                                  # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # quadrant 2
    def test_get_second_points_neg_1_pos_1(self):
        points = [Point(-1,1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(0,1),                                      # 0
            Point(math.sqrt(3)/2 - 1, 3/2),                  # 30
            Point(math.sqrt(2)/2 - 1, math.sqrt(2)/2 + 1),   # 45
            Point(-1/2, math.sqrt(3)/2 + 1),                 # 60
            Point(-1,2),                                     # 90
            Point (-2,1),                                    # 180
            Point (math.sqrt(3)/2 - 1, 1/2),                 # -30
            Point (math.sqrt(2)/2 - 1, -math.sqrt(2)/2 + 1), # -45
            Point (-1/2, -math.sqrt(3)/2 + 1),               # -60
            Point (-1,0)                                     # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # left x-axis
    def test_get_second_points_neg_1_0(self):
        points = [Point(-1,0), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(0,0),                                  # 0
            Point(math.sqrt(3)/2 - 1, 1/2),              # 30
            Point(math.sqrt(2)/2 - 1, math.sqrt(2)/2),   # 45
            Point(-1/2, math.sqrt(3)/2),                 # 60
            Point(-1,1),                                 # 90
            Point (-2,0),                                # 180
            Point (math.sqrt(3)/2 - 1, -1/2),            # -30
            Point (math.sqrt(2)/2 - 1, -math.sqrt(2)/2), # -45
            Point (-1/2, -math.sqrt(3)/2),               # -60
            Point (-1,-1)                                # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # quadrant 3
    def test_get_second_points_neg_1_neg_1(self):
        points = [Point(-1,-1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(0,-1),                                     # 0
            Point(math.sqrt(3)/2 - 1, -1/2),                 # 30
            Point(math.sqrt(2)/2 - 1, math.sqrt(2)/2 -1),    # 45
            Point(-1/2, math.sqrt(3)/2 - 1),                 # 60
            Point(-1,0),                                     # 90
            Point (-2,-1),                                   # 180
            Point (math.sqrt(3)/2 - 1, -3/2),                # -30
            Point (math.sqrt(2)/2 - 1, -math.sqrt(2)/2 - 1), # -45
            Point (-1/2, -math.sqrt(3)/2 - 1),               # -60
            Point (-1,-2)                                    # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # down y-axis
    def test_get_second_points_0_neg_1(self):
        points = [Point(0,-1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(1,-1),                                 # 0
            Point(math.sqrt(3)/2, -1/2),                 # 30
            Point(math.sqrt(2)/2, math.sqrt(2)/2 -1),    # 45
            Point(1/2, math.sqrt(3)/2 - 1),              # 60
            Point(0,0),                                  # 90
            Point (-1,-1),                               # 180
            Point (math.sqrt(3)/2, -3/2),                # -30
            Point (math.sqrt(2)/2, -math.sqrt(2)/2 - 1), # -45
            Point (1/2, -math.sqrt(3)/2 - 1),            # -60
            Point (0,-2)                                 # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y)

    # quadrant 4
    def test_get_second_points_pos_1_neg_1(self):
        points = [Point(1,-1), None, None]
        equilateral = Equilateral(points)
        second_points = equilateral.get_second_points(points[0])

        expected = [
            Point(2,-1),                                     # 0
            Point(math.sqrt(3)/2 + 1, -1/2),                 # 30
            Point(math.sqrt(2)/2 + 1, math.sqrt(2)/2 -1),    # 45
            Point(3/2, math.sqrt(3)/2 - 1),                  # 60
            Point(1,0),                                      # 90
            Point (0,-1),                                    # 180
            Point (math.sqrt(3)/2 + 1, -3/2),                # -30
            Point (math.sqrt(2)/2 + 1, -math.sqrt(2)/2 - 1), # -45
            Point (3/2, -math.sqrt(3)/2 - 1),                # -60
            Point (1,-2)                                     # -90
        ]   

        self.assertEqual(len(second_points), len(expected))
        for i in range(len(second_points)):
            self.assertAlmostEqual(second_points[i].x, expected[i].x)
            self.assertAlmostEqual(second_points[i].y, expected[i].y) 

  # --------------------- coordinatize ------------------------ #
  # what is tested here:
  # - from one point: origin, (1,1), (-1,1), (-1,-1), (1,-1)
  #   - for each point, all positions of points list: e.g. [(0,0), None, None], [None, (0,0), None], [None, None, (0,0)]
  # - from two points (starting point -> all directions):
  #   - (origin)     -  from (0,0) to (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) 
  #   - (non-origin) -  from (1,1) to (2,1), (2,2), (1,2), (0,2), (0,1), (0,0), (1,0), (2,0)
  # - from three points:
  #   - (0,0), (1,0), (sqrt(3)/2, 1/2)
    def test_coordinatize_one_point_origin_first_position(self):
        lattice = Lattice(3)
        points = [Point(0,0), None, None]
        equilateral = Equilateral(points)
        coordinatized = equilateral.coordinatize(lattice)

        expected = [

        ]

        self.assertEqual(len(coordinatized), len(expected))
        for i in range(len(coordinatized)):
            self.assertAlmostEqual(coordinatized[i].x, expected[i].x)
            self.assertAlmostEqual(coordinatized[i].y, expected[i].y)
    



#* from old code, not sure if we still need them ----------------------------------------------
    # def test_verify_equilateral_triangle_true(self):
    #     coords = [(1,0), (3, (2*math.sqrt(3))), (5,0)]
    #     shape = Equilateral(coords)
    #     self.assertTrue(shape._verify_equilateral_triangle())

    # def test_verify_equilateral_triangle_true_2(self):
    #     coords = [(3,0), (0, (3*math.sqrt(3))), (-3,0)]
    #     shape = Equilateral(coords)
    #     self.assertTrue(shape._verify_equilateral_triangle())

    # def test_verify_equilateral_triangle_too_large(self):
    #     coords = [(0,0), (1,0), (0,1), (1,1)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # def test_verify_equilateral_triangle_too_small(self):
    #     coords = [(0,0), (1,0)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # def test_verify_equilateral_triangle_too_small(self):
    #     coords = [(0,0), (1,0)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())
    # # *
    # # | \
    # # *--*
    # def test_verify_equilateral_triangle_right(self):
    #     coords = [(0,0), (1,0), (0,1)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # # *--*
    # # | /
    # # *
    # def test_verify_equilateral_triangle_right_true_angle_top(self):
    #     coords = [(0,0), (1,2), (0, 2)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # #    *
    # #  / |
    # # *--*
    # def test__verify_equilateral_triangle_isosceles(self):
    #     coords = [(0,0), (1,0), (2,1)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # # *--*
    # #  \ |
    # #    *
    # def test_verify_equilateral_triangle_right_not_on_origin(self):
    #     coords = [(0, 1), (1, 0), (1, 1)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    # #    *       but closed
    # #   /
    # #  /
    # # *             obtuse angle
    # #  \
    # #   *
    # def test_verify_equilateral_triangle_obtuse(self):
    #     coords = [(0,0), (-2, 1), (3, 2)]
    #     shape = Equilateral(coords)
    #     self.assertFalse(shape._verify_equilateral_triangle())

    #---------------------------------
    #----- calculate coordinates -----
    #---------------------------------

    # def test_calculate_coords_0_degree_segment(self):
    #     base = Segment(Coordinate(0,0), Coordinate(1,0))

    #     shape   = Equilateral(base)
    #     coords  = shape._calculate_coords()

    #     expected_coords = [
    #         Coordinate(0, 0),
    #         Coordinate(1/ 2, math.sqrt(3) / 2),
    #         Coordinate(1, 0)
    #     ]

    #     for i in range(len(expected_coords)):
    #         self.assertTrue(coords[i] == expected_coords[i])

    # def test_calculate_coords_30_degree_segment(self):
    #     base = Segment(Coordinate(0,0), Coordinate(math.sqrt(3) / 2, 1 / 2))

    #     shape   = Equilateral(base)
    #     coords  = shape._calculate_coords()

    #     expected_coords = [
    #         Coordinate(0, 0),
    #         Coordinate(0.00000000000000006123233995736766, 1.0),
    #         Coordinate(math.sqrt(3) / 2, 1 / 2)
    #     ]

    #     for i in range(len(expected_coords)):
    #         self.assertTrue(coords[i] == expected_coords[i])

    # def test_calculate_coords_45_degree_segment(self):
    #     base = Segment(Coordinate(0,0), Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2))

    #     shape   = Equilateral(base)
    #     coords  = shape._calculate_coords()

    #     expected_coords = [
    #         Coordinate(0, 0),
    #         Coordinate(-0.25881904510252063,0.9659258262890683),
    #         Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2)
    #     ]

    #     for i in range(len(expected_coords)):
    #         self.assertTrue(coords[i] == expected_coords[i])

    # def test_calculate_coords_45_degree_segment_backwards(self):
    #     base = Segment(Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2), Coordinate(0,0))

    #     shape   = Equilateral(base)
    #     coords  = shape._calculate_coords()

    #     expected_coords = [
    #         Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2),
    #         Coordinate(0.9659258262890683,-0.25881904510252074),
    #         Coordinate(0, 0)
    #     ]

    #     for i in range(len(expected_coords)):
    #         self.assertTrue(coords[i] == expected_coords[i])

    # def test_calculate_coords_60_degree_segment_offset(self):
    #     # build triangle from the end of a 45 degree equilateral triangle
    #     base = Segment(Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2), Coordinate(1, (math.sqrt(3) / 2) + (math.sqrt(2) / 2)))

    #     shape   = Equilateral(base)
    #     coords  = shape._calculate_coords()

    #     expected_coords = [
    #         Coordinate(math.sqrt(2) / 2, math.sqrt(2) / 2),
    #         Coordinate(0.04691816067802701,1.4582066316399054),
    #         Coordinate(1, (math.sqrt(3) / 2) + (math.sqrt(2) / 2))
    #     ]

    #     for i in range(len(expected_coords)):
    #         self.assertTrue(coords[i] == expected_coords[i])

if __name__ == "__main__":
    unittest.main()