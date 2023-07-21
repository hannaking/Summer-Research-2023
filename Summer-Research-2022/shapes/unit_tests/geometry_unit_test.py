import unittest
import sys
import math

sys.path.insert(0, './Summer-Research-2022/')

from node import Node
from shapely.geometry import Point
from shapes.vector import Vector
from shapes.geometry import Geometry

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

DEFAULT_SIDE_LENGTH = 1

PLACEHOLDER_COORD = Point(-0.1, -0.1)

class TestGeometry(unittest.TestCase):

 # -------------------------- rotate ------------------------------ #
    def test_rotate_0_degrees(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        point3 = Point(0, 1)
        scenario = [point1, point2, point3]
        angle = math.radians(0)

        rotated_scenario = Geometry.rotate(scenario, angle)

        expected = [
            point1, 
            point2, 
            point3
        ]

        self.assertEqual(len(rotated_scenario), len(expected))
        for i in range(len(rotated_scenario)):
            self.assertAlmostEqual(rotated_scenario[i].x, expected[i].x)
            self.assertAlmostEqual(rotated_scenario[i].y, expected[i].y)

    def test_rotate_45_degrees(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        point3 = Point(0, 1)
        scenario = [point1, point2, point3]
        angle = math.radians(45)

        rotated_scenario = Geometry.rotate(scenario, angle)

        expected = [
            Point(0, 0),
            Point(0.70710678, -0.70710678),
            Point(0.70710678, 0.70710678)
        ]

        self.assertEqual(len(rotated_scenario), len(expected))
        for i in range(len(rotated_scenario)):
            self.assertAlmostEqual(rotated_scenario[i].x, expected[i].x)
            self.assertAlmostEqual(rotated_scenario[i].y, expected[i].y)

    def test_rotate_90_degrees(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        point3 = Point(0, 1)
        scenario = [point1, point2, point3]
        angle = math.radians(90)

        rotated_scenario = Geometry.rotate(scenario, angle)

        expected = [
            Point(0, 0),
            Point(0, -1),
            Point(1, 0)
        ]

        self.assertEqual(len(rotated_scenario), len(expected))
        for i in range(len(rotated_scenario)):
            self.assertAlmostEqual(rotated_scenario[i].x, expected[i].x)
            self.assertAlmostEqual(rotated_scenario[i].y, expected[i].y)

    def test_rotate_180_degrees(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        point3 = Point(0, 1)
        scenario = [point1, point2, point3]
        angle = math.radians(180)

        rotated_scenario = Geometry.rotate(scenario, angle)

        expected = [
            Point(0, 0),
            Point(-1, 0),
            Point(0, -1)
        ]

        self.assertEqual(len(rotated_scenario), len(expected))
        for i in range(len(rotated_scenario)):
            self.assertAlmostEqual(rotated_scenario[i].x, expected[i].x)
            self.assertAlmostEqual(rotated_scenario[i].y, expected[i].y)

    def test_rotate_neg_90_degrees(self):
        point1 = Point(0, 0)
        point2 = Point(1, 0)
        point3 = Point(0, 1)
        scenario = [point1, point2, point3]
        angle = math.radians(-90)

        rotated_scenario = Geometry.rotate(scenario, angle)

        expected = [
            Point(0, 0),
            Point(0, 1),
            Point(-1, 0)
        ]

        self.assertEqual(len(rotated_scenario), len(expected))
        for i in range(len(rotated_scenario)):
            self.assertAlmostEqual(rotated_scenario[i].x, expected[i].x)
            self.assertAlmostEqual(rotated_scenario[i].y, expected[i].y)

 # ---------------------------------get_angle--------------------------------#
        
    def test_get_angle_acute_positive(self):
        p1 = Point(0, 1)
        p2 = Point(1, 0)
        p3 = Point(0, 0)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, math.pi / 4)

    def test_get_angle_acute_negative(self):
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(0, 1)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, -math.pi / 4)

    def test_get_angle_right_positive(self):
        p1 = Point(1, 1)
        p2 = Point(1, 0)
        p3 = Point(0, 0)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, math.pi / 2)

    def test_get_angle_right_negative(self):
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(1, 1)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, -math.pi / 2)

    def test_get_angle_obtuse_positive(self):
        p1 = Point(2, 1)
        p2 = Point(1, 0)
        p3 = Point(0, 0)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, 3 * math.pi / 4)

    def test_get_angle_obtuse_negative(self):
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(2, 1)
        points = [p1, p2, p3]

        scenarios = []
        for rotation in [0, 45, 90, 135, 180, -45, -90, -135]:
            new_scenario = Geometry.rotate(points, math.radians(rotation))
            scenarios.append(new_scenario)
        
        for scenario in scenarios:
            angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
            self.assertAlmostEqual(angle, -3 * math.pi / 4)



 # ----------------------------- get second points --------------------------#
    # origin
    def test_get_second_points_0_0(self):
        points = [Point(0,0), None, None]
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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
        second_points = Geometry.get_second_points(points[0])

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



    #--------------------------------find reference angle--------------------------------
    # all angles are in radians.
    #
    # ∧
    # |
    # |-------> <- this (ref angle = 0 radians)
    # |
    # ∨
    def test_find_reference_angle_parallel_to_x_axis_positive(self):
        start = Point(0, 0)
        end = Point(1, 0)
         

        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = 0
        self.assertEqual(ref_angle, expected)

    #         ∧
    #         |
    # <-------| <- this (ref angle = pi radians)
    #         |
    #         ∨
    def test_find_reference_angle_parallel_to_x_axis_negative(self):
        start = Point(0, 0)
        end = Point(-1, 0)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧  <- this (ref angle = pi / 2 radians)
    #         |
    # <-------|-------> 


    def test_find_reference_angle_parallel_to_y_axis_positive(self):
        start = Point(0, 0)
        end = Point(0, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    # <-------|-------> 
    #         |
    #         ∨  <- this (ref angle = -pi / 2 radians)

    def test_find_reference_angle_parallel_to_y_axis_negative(self):
        start = Point(0, 0)
        end = Point(0, -1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    # ∧ /
    # |/   <- this (ref angle = pi / 6 radians)
    # |-------> 

    def test_find_reference_angle_30_degree_positive(self): 
        start = Point(0, 0)
        end = Point(math.sqrt(3) / 2, 1/2)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 6
        self.assertAlmostEqual(ref_angle, expected)

    # <--------|
    #        / |
    #       /  ∨
    #      ^ this (ref angle = -pi / 6 radians)
    def test_find_reference_angle_30_degree_negative(self): 
        start = Point(0, 0)
        end = Point(math.sqrt(3) / 2, -1/2)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 6
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_45_degree_positive(self):
        start = Point(0, 0)
        end = Point((math.sqrt(2) / 2), (math.sqrt(2) / 2))
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 4
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_45_degree_negative(self):
        start = Point(0, 0)
        end = Point((math.sqrt(2) / 2), -(math.sqrt(2) / 2))
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 4
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_60_degree_positive(self):
        start = Point(0, 0)
        end = Point(1/2, (math.sqrt(3) / 2))
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 3
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_60_degree_negative(self):
        start = Point(0, 0)
        end = Point(1/2, -(math.sqrt(3) / 2))
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 3
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_90_degree_positive(self):
        start = Point(0, 0)
        end = Point(0, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    def test_find_reference_angle_90_degree_negative(self):
        start = Point(0, 0)
        end = Point(0, -1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    #@ now, test for starting location not at the origin. when testing diagonal segments, our angle will be 45 degrees, we won't bother doing 30 or 60.
    #         ∧
    #         |  o__. <- this segment (o is the starting point)
    # <-------|-------> 

    def test_find_reference_angle_not_on_origin_horizontal_startpoint_1(self):
        start = Point(1, 1)
        end = Point(2, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = 0
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧
    #         |  .__o <- this segment (o is the starting point)
    # <-------|-------> 


    def test_find_reference_angle_not_on_origin_horizontal_startpoint_2(self):
        start = Point(2, 1)
        end = Point(1, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧  .
    #         |  |   <- this segment (o is the starting point)
    #         |  o  
    # <-------|-------> 

    def test_find_reference_angle_not_on_origin_vertical_startpoint_1(self):
        start = Point(1, 1)
        end = Point(1, 2)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧  o
    #         |  |   <- this segment (o is the starting point)
    #         |  .  
    # <-------|-------> 

    def test_find_reference_angle_not_on_origin_vertical_startpoint_2(self):
        start = Point(1, 2)
        end = Point(1, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -math.pi / 2
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧    .
    #         |   /  <- this segment (o is the starting point)
    #         |  o  
    # <-------|-------> 
    def test_find_reference_angle_not_on_origin_diagonal_startpoint_1(self):
        start = Point(1, 1)
        end = Point(2, 2)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = math.pi / 4
        self.assertAlmostEqual(ref_angle, expected)

    #         ∧    o
    #         |   /  <- this segment (o is the starting point)
    #         |  .  
    # <-------|-------> 
    def test_find_reference_angle_not_on_origin_diagonal_startpoint_2(self):
        start = Point(2, 2)
        end = Point(1, 1)
         

         
        ref_angle =  Geometry._find_reference_angle(end, start)

        expected = -(3*math.pi / 4)
        self.assertAlmostEqual(ref_angle, expected)

#---------------------------------find goal angle---------------------------------
    # test that we find the goal angle. 
    # background info: a reference angle is the angle of the reference segment from the x-axis.
    # the given angle is the angle we want to use to find the next vertex. 
    # the given angle is counterclockwise from the reference angle.
    # now, we are not creating any vectors here, but for a mental image,
    # imagine a vector formed by the given angle and the start point. we want to find the angle between this vector and the x-axis.
    # 
    # ∧   / <- imaginary vector
    # |  /  
    # | /
    # |/| <- goal angle              given angle = angle btwn imaginary vector and ref segment
    # |--------------------->        goal angle = ref angle + given angle
    # |\| <- reference angle         (ref angle is negative, given angle is positive, so we get this difference as the goal angle)
    # | \
    # |  \ 
    # V   \
    #     ^ ref segment

    #### ref angle is 0 ####

    # ∧
    # | 0°
    # |-------> 
    def test_find_goal_angle_horizontal_segment_given_0_degrees(self):
        start = Point(0, 0)
         # initialization does not matter, just need it to create the object

        given_angle = 0
        ref_angle = 0
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle # when the ref angle is 0, given angle will be the goal angle
        self.assertAlmostEqual(goal_angle, expected)  

    # ∧ /
    # |/ 30°
    # |-------> 
    def test_find_goal_angle_horizontal_segment_given_30_degrees(self):
        start = Point(0, 0)
         # initialization does not matter, just need it to create the object

        given_angle = math.radians(30)
        ref_angle = 0
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle # when the ref angle is 0, given angle will be the goal angle
        self.assertAlmostEqual(goal_angle, expected)  

    # ∧ /
    # |/ 45°
    # |-------> 
    def test_find_goal_angle_horizontal_segment_given_45_degrees(self):
        start = Point(0, 0)
         

        given_angle = math.radians(45)
        ref_angle = 0
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle # when the ref angle is 0, given angle will be the goal angle
        self.assertAlmostEqual(goal_angle, expected)

    # ∧ /
    # |/ 60°
    # |-------> 

    def test_find_goal_angle_horizontal_segment_given_60_degrees(self):
        start = Point(0, 0)
         

        given_angle = math.radians(60)
        ref_angle = 0
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle # when the ref angle is 0, given angle will be the goal angle
        self.assertAlmostEqual(goal_angle, expected)

    # ∧
    # | 90°
    # |-------> 
    def test_find_goal_angle_horizontal_segment_given_90_degrees(self):
        start = Point(0, 0)
         

        given_angle = math.radians(90)
        ref_angle = 0
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle # when the ref angle is 0, given angle will be the goal angle
        self.assertAlmostEqual(goal_angle, expected)

    #### ref angle is positive ####

    #           ∧
    #     0°    |  
    # <---------|---------> 

    def test_find_goal_angle_vertical_segment_given_0_degrees(self):
        start = Point(0, 0)
         

        given_angle = 0
        ref_angle = math.pi / 2
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle # when ref angle is positive, goal angle is given angle + ref angle
        self.assertAlmostEqual(goal_angle, expected)
    #            30°∧ 
    #            \  |
    #             \ |
    #    <---------\|--------->         
    def test_find_goal_angle_vertical_segment_given_30_degrees(self):
        start = Point(0, 0)
         

        given_angle = math.radians(30)
        ref_angle = math.pi / 2
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle
        self.assertAlmostEqual(goal_angle, expected)

    #           ∧    
    #           |30°/
    #           |  /
    #           | /
    #    <------|/------> 
    def test_find_goal_angle_diagonal_segment_given_30_degrees_quadrant_1(self):
        start = Point(0, 0)
         

        given_angle = math.radians(30)
        ref_angle = math.pi / 4
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle
        self.assertAlmostEqual(goal_angle, expected)
    #               \  ∧
    #          30°   \ |
    #       <---------\|---------> 
    def test_find_goal_angle_diagonal_segment_given_30_degrees_quadrant_2(self):
        start = Point(0, 0)
         

        given_angle = math.radians(30)
        ref_angle = (3 * math.pi) / 4
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle
        self.assertAlmostEqual(goal_angle, expected)

    #### ref angle is negative ####

    #     <------/|------> 
    #           / |
    #          /  |
    #         /   |
    #        /30° ∨
    def test_find_goal_angle_diagonal_segment_given_30_degrees_quadrant_3(self):
        start = Point(0, 0)
         

        given_angle = math.radians(30)
        ref_angle = -(3 * math.pi) / 4
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle
        self.assertAlmostEqual(goal_angle, expected)

    #     <------|\------>
    #            | \  30°
    #            |  \ 
    #            |   \
    #            ∨    \
    def test_find_goal_angle_diagonal_segment_given_30_degrees_quadrant_4(self):
        start = Point(0, 0)
         

        given_angle = math.radians(30)
        ref_angle = -(math.pi) / 4
        goal_angle =  Geometry._find_goal_angle(given_angle, ref_angle)

        expected = given_angle + ref_angle
        self.assertAlmostEqual(goal_angle, expected)

#-----------------------------------------find vector-----------------------------------------#
    # note: goal angle will not always be a nice angle like 0, 30, 45, 60, 90, etc.,
    # but they make for nice tests

    #### goal angle is 0 ####

    def test_find_vector_goal_angle_0(self):
        start = Point(0, 0)
         # initialization does not matter, we just want the object to be created

        goal_angle = 0
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(1, 0).toArr()
        
        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    #### goal angle is positive ####

    def test_find_vector_goal_angle_30(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(30)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(math.sqrt(3) / 2, 1/2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_45(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(45)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(math.sqrt(2) / 2, math.sqrt(2) / 2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_60(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(60)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(1/2, math.sqrt(3) / 2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_90(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(90)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(0, 1).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    #### goal angle is negative ####

    def test_find_vector_goal_angle_negative_30(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(-30)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(math.sqrt(3) / 2, -1/2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_negative_45(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(-45)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(math.sqrt(2) / 2, -math.sqrt(2) / 2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_negative_60(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(-60)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(1/2, -math.sqrt(3) / 2).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

    def test_find_vector_goal_angle_negative_90(self):
        start = Point(0, 0)
         

        goal_angle = math.radians(-90)
        vector =  Geometry._find_vector(DEFAULT_SIDE_LENGTH, goal_angle)

        # convert to array for easy comparison
        vector = vector.toArr() 
        expected = Vector(0, -1).toArr()

        self.assertAlmostEqual(vector[0], expected[0])
        self.assertAlmostEqual(vector[1], expected[1])

#-----------------------------------------find new coord-----------------------------------------#
    # all diagonal vectors are at 45 degrees to make tests simpler

    #### quadrant 1 ####

    ## start at origin ##

    def test_find_new_point_quadrant1_origin_horizontal(self):
        start = Point(0, 0)
         

        vector = Vector(1, 0)
        new_point =  Geometry._find_new_point(vector, start)
        expected = Point(1, 0)

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant1_origin_diagonal(self):
        start = Point(0, 0)
         

        vector = Vector(1, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(1, 1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant1_origin_vertical(self):
        start = Point(0, 0)
         

        vector = Vector(0, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(0, 1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    ## start at non-origin ##

    def test_find_new_point_quadrant1_non_origin_horizontal(self):
        start = Point(1, 1)
         

        vector = Vector(1, 0)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(2, 1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant1_non_origin_diagonal(self):
        start = Point(1, 1)
         

        vector = Vector(1, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(2, 2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant1_non_origin_vertical(self):
        start = Point(1, 1)
         

        vector = Vector(0, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(1, 2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    #### quadrant 2 ####

    ## start at origin ##

    def test_find_new_point_quadrant2_origin_horizontal(self):
        start = Point(0, 0)
         

        vector = Vector(-1, 0)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-1, 0) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_origin_diagonal(self):
        start = Point(0, 0)
         

        vector = Vector(-1, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-1, 1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # origin vertical test is same as origin vertical test in quadrant 1, so don't need to test in quadrant 2

    ## start at non-origin ##

    def test_find_new_point_quadrant2_non_origin_horizontal(self):
        start = Point(-1, 1)
         

        vector = Vector(-1, 0)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-2, 1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_non_origin_diagonal(self):
        start = Point(-1, 1)
         

        vector = Vector(-1, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-2, 2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_non_origin_vertical(self):
        start = Point(-1, 1)
         

        vector = Vector(0, 1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-1, 2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    #### quadrant 3 ####

    ## start at origin ##

    # origin horizontal test is same as origin horizontal test in quadrant 2, so don't need to test in quadrant 3

    def test_find_new_point_quadrant2_origin_diagonal(self):
        start = Point(0, 0)
         

        vector = Vector(-1, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-1, -1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_origin_vertical(self):
        start = Point(0, 0)
         

        vector = Vector(0, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(0, -1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    ## start at non-origin ##

    def test_find_new_point_quadrant2_non_origin_horizontal(self):
        start = Point(-1, -1)
         

        vector = Vector(-1, 0)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-2, -1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_non_origin_diagonal(self):
        start = Point(-1, -1)
         

        vector = Vector(-1, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-2, -2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant2_non_origin_vertical(self):
        start = Point(-1, -1)
         

        vector = Vector(0, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(-1, -2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    #### quadrant 4 ####

    ## start at origin ##

    # origin horizontal test is same as origin horizontal test in quadrant 1, so don't need to test in quadrant 4

    def test_find_new_point_quadrant4_origin_diagonal(self):
        start = Point(0, 0)
         

        vector = Vector(1, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(1, -1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # origin vertical test is same as origin vertical test in quadrant 3, so don't need to test in quadrant 4

    ## start at non-origin ##

    def test_find_new_point_quadrant4_non_origin_horizontal(self):
        start = Point(1, -1)
         

        vector = Vector(1, 0)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(2, -1) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant4_non_origin_diagonal(self):
        start = Point(1, -1)
         

        vector = Vector(1, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(2, -2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_find_new_point_quadrant4_non_origin_vertical(self):
        start = Point(1, -1)
         

        vector = Vector(0, -1)
        new_point =  Geometry._find_new_point(vector, start)


        expected = Point(1, -2) 

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    #---------------------------calculate coord from angle-----------------------------------#
    # how these tests are structured:
    # have a series of tests for each starting point we want to test: 
    #   - start at origin
    #   - start at (1,1)   - quadrant 1
    #   - start at (-1,1)  - quadrant 2
    #   - start at (-1,-1) - quadrant 3
    #   - start at (1,-1)  - quadrant 4
    # for each of these tests, we have a series of tests for each segment we want to test:
    #   - right horizontal
    #   - up-right diagonal
    #   - up vertical
    #   - up-left diagonal
    #   - left horizontal
    #   - down-left diagonal
    #   - down vertical
    #   - down-right diagonal
    # and for each of these segments, we test for each angle we want to give:
    #   - 0 radians    (0 degrees)
    #   - pi/6 radians (30 degrees)
    #   - pi/4 radians (45 degrees)
    #   - pi/3 radians (60 degrees)
    #   - pi/2 radians (90 degrees)
    #   - pi radians   (180 degrees)
    # when calculating the expected Point, I manually calculated cos(goal angle), sin(goal angle), then added the offset to both values

    # -------- start at origin -------- #

    # -- right horizontal -- #
    # ∧
    # | 
    # |-----* endpoint (1,0)
    # ref angle = 0°

    def test_calculate_point_from_angle_origin_right_horizontal_0_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(1, 0) # goal angle 0 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_right_horizontal_30_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(3)/2, 1/2) # goal angle 30 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_right_horizontal_45_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_right_horizontal_60_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(1/2, math.sqrt(3)/2) # goal angle 60 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_right_horizontal_90_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, 1) # goal angle 90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_right_horizontal_180_degrees(self):
        start = Point(0, 0)
        end = Point(1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1, 0) # goal angle 180 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- up-right diagonal -- #
    # ∧
    # |  . endpoint (1,1)
    # | /
    # |/----> 
    # ref angle = 45°

    def test_calculate_point_from_angle_origin_up_right_diagonal_0_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_right_diagonal_30_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0.25881905, 0.96592583) # goal angle 75 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_right_diagonal_45_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, 1) # goal angle 90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_right_diagonal_60_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-0.25881905, 0.96592583) # goal angle 105 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_right_diagonal_90_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 135 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_right_diagonal_180_degrees(self):
        start = Point(0, 0)
        end = Point(1, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- up vertical -- #
    #       . endpoint (0,1)
    #       |
    #       |
    # <-----|----->
    # ref angle = 90°

    def test_calculate_point_from_angle_origin_up_vertical_0_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, 1) # goal angle 90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_vertical_30_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1/2, math.sqrt(3)/2) # goal angle 120 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_vertical_45_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 135 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_vertical_60_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(3)/2, 1/2) # goal angle 150 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_vertical_90_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1, 0) # goal angle 180 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_vertical_180_degrees(self):
        start = Point(0, 0)
        end = Point(0, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, -1) # goal angle 270 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- up-left diagonal -- #
    #         ∧
    #      .  | endpoint(-1, 1)
    #       \ |
    # <------\|
    # ref angle = 135°

    def test_calculate_point_from_angle_origin_up_left_diagonal_0_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 135 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_left_diagonal_30_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-0.96592583, 0.25881905) # goal angle 165 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_left_diagonal_45_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1, 0) # goal angle 180 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)
    
    def test_calculate_point_from_angle_origin_up_left_diagonal_60_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-0.96592583, -0.25881905) # goal angle 195 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_left_diagonal_90_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle 225 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_up_left_diagonal_180_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle 315 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- left horizontal -- #
    #        ∧
    #        |
    #        |
    # *------| endpoint (-1, 0)
    # ref angle = 180°

    def test_calculate_point_from_angle_origin_left_horizontal_0_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1, 0) # goal angle 180 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_left_horizontal_30_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(3)/2, -1/2) # goal angle 210 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_left_horizontal_45_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle 225 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_left_horizontal_60_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-1/2, -math.sqrt(3)/2) # goal angle 240 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_left_horizontal_90_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, -1) # goal angle 270 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_left_horizontal_180_degrees(self):
        start = Point(0, 0)
        end = Point(-1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(1, 0) # goal angle 360 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- down-left diagonal -- #
    # <----/|
    #     / |
    #    *  | endpoint(-1, -1)
    #       V
    # ref angle = -135°

    def test_calculate_point_from_angle_origin_down_left_diagonal_0_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle -135 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_left_diagonal_30_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-0.25881905, -0.96592583) # goal angle -105 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_left_diagonal_45_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, -1) # goal angle -90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_left_diagonal_60_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0.25881905, -0.96592583) # goal angle -75 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_left_diagonal_90_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle -45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_left_diagonal_180_degrees(self):
        start = Point(0, 0)
        end = Point(-1, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- down vertical -- #
    # <-----|----->
    #       |
    #       |
    #       * endpoint(0, -1)
    # ref angle = -90°

    def test_calculate_point_from_angle_origin_down_vertical_0_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, -1) # goal angle is -90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_vertical_30_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0.5, -0.8660254) # goal angle is -60 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_vertical_45_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle is -45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_vertical_60_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(3)/2, -1/2) # goal angle is -30 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_vertical_90_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(1, 0) # goal angle is 0 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_vertical_180_degrees(self):
        start = Point(0, 0)
        end = Point(0, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0, 1) # goal angle is 90 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    # -- down-right diagonal -- #
    # |\----->
    # | \
    # |  * endpoint(1, -1)
    # V
    # ref angle = -45°

    def test_calculate_point_from_angle_origin_down_right_diagonal_0_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, -math.sqrt(2)/2)    # goal angle is -45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_right_diagonal_30_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0.96592583, -0.25881905) # goal angle is -15 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_right_diagonal_45_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(1, 0) # goal angle is 0 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_right_diagonal_60_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(0.96592583, 0.25881905) # goal angle is 15 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_right_diagonal_90_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(math.sqrt(2)/2, math.sqrt(2)/2) # goal angle is 45 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)

    def test_calculate_point_from_angle_origin_down_right_diagonal_180_degrees(self):
        start = Point(0, 0)
        end = Point(1, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected = Point(-math.sqrt(2)/2, math.sqrt(2)/2) # goal angle is 135 degrees

        self.assertAlmostEqual(new_point.x, expected.x)
        self.assertAlmostEqual(new_point.y, expected.y)
    
    # -------------------------------- start at (1,1) - QUADRANT 1 ------------------------------- #

    # -- right horizontal -- # #
    # ∧
    # | .___. endpoint(2, 1)
    # |----->
    # ref angle = 0°

    def test_calculate_point_from_angle_quadrant1_right_horizontal_0_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) # goal angle 0 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_right_horizontal_30_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, 1/2) # goal angle 30 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_right_horizontal_45_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_right_horizontal_60_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1/2, math.sqrt(3)/2) # goal angle 60 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_right_horizontal_90_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_right_horizontal_180_degrees(self):
        start = Point(1, 1)
        end = Point(2, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-right diagonal -- # #
    # ∧    . endpoint(2, 2)
    # |   /  
    # |  *  
    # |-------> 
    # ref angle = 45°

    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_0_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_30_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, 0.96592583) # goal angle 75 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
        
    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_45_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0,1) # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_60_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, 0.96592583) # goal angle 105 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_90_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	 # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_right_diagonal_180_degrees(self):
        start = Point(1, 1)
        end = Point(2, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2))  # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up vertical -- #
    # ∧  . endpoint (1, 2)
    # |  |  
    # |  *  
    # |-------> 
    # ref angle = 90°

    def test_calculate_point_from_angle_quadrant1_up_vertical_0_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_vertical_30_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, math.sqrt(3)/2)  # goal angle 120 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_vertical_45_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_vertical_60_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, 1/2) 		  # goal angle 150 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_vertical_90_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 		  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_vertical_180_degrees(self):
        start = Point(1, 1)
        end = Point(1, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 		  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-left diagonal -- #
    #  .  endpoint (0,2)
    #  |\
    #  | *
    #  |---->
    # ref angle = 135°

    def test_calculate_point_from_angle_quadrant1_up_left_vertical_0_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_left_vertical_30_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, 0.25881905) 		  # goal angle 165 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_left_vertical_45_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
    
    def test_calculate_point_from_angle_quadrant1_up_left_vertical_60_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, -0.25881905) 		  # goal angle 195 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
        
    def test_calculate_point_from_angle_quadrant1_up_left_vertical_90_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_up_left_vertical_180_degrees(self):
        start = Point(1, 1)
        end = Point(0, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle 315 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- left horizontal -- #   
    # ∧
    # |
    # .___.
    # |----->  endpoint (0, 1)
    # ref angle = 180°

    def test_calculate_point_from_angle_quadrant1_left_horizontal_0_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1,0) # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_horizontal_30_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, -1/2) # goal angle 210 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_horizontal_45_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_horizontal_60_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, -math.sqrt(3)/2) 		  # goal angle 240 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_horizontal_90_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1)                               # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_horizontal_180_degrees(self):
        start = Point(1, 1)
        end = Point(0, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1,0)                                # goal angle 360 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- left-down diagonal -- #
    # ∧
    # |  .
    # | /
    # |*----->  endpoint (0,0)
    # ref angle = -135°

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_0_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, -math.sqrt(2)/2)     # goal angle -135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_30_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, -0.96592583) 		  # goal angle -105 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_45_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_60_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, -0.96592583) 		  # goal angle -75 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_90_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_left_down_diagonal_180_degrees(self):
        start = Point(1, 1)
        end = Point(0, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down vertical -- #
    # ∧
    # |  .
    # |  |
    # |--*-->  endpoint (1,0)
    # ref angle = -90°

    def test_calculate_point_from_angle_quadrant1_down_vertical_0_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_vertical_30_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.5, -0.8660254) 			  # goal angle is -60 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_vertical_45_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_vertical_60_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, -1/2) 		  # goal angle is -30 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_vertical_90_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_vertical_180_degrees(self):
        start = Point(1, 1)
        end = Point(1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 					  # goal angle is 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down-right diagonal -- #
    # ∧
    # | .
    # |  \
    # |---*->  endpoint (2,0)
    # ref angle = -45°

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_0_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_30_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, -0.25881905) 		  # goal angle is -15 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_45_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_60_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, 0.25881905) 		  # goal angle is 15 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_90_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant1_down_right_diagonal_180_degrees(self):
        start = Point(1, 1)
        end = Point(2, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -------------------------------- start at (-1,1) - QUADRANT 2 ------------------------------- #

    # -- right horizontal -- #
    #         ∧
    #         |
    #     .___. endpoint (0, 1)
    # <-------|
    # ref angle = 0°

    def test_calculate_point_from_angle_quadrant2_right_horizontal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 	# goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_right_horizontal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, 1/2) 		  # goal angle 30 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_right_horizontal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_right_horizontal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1/2, math.sqrt(3)/2) 		  # goal angle 60 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_right_horizontal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1)				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
    
    def test_calculate_point_from_angle_quadrant2_right_horizontal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0)				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-right diagonal -- #
    #        ∧
    #        |
    #        . endpoint (0,2)
    #       /|
    #      * |
    # <------|
    # ref angle = 45°

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, 0.96592583) 		  # goal angle 75 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1)				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, 0.96592583)		  # goal angle 105 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_right_diagonal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up vertical -- #
    #      . ∧ endpoint (-1, 2)
    #      | |  
    #      * |
    # <------|
    # ref angle = 90°

    def test_calculate_point_from_angle_quadrant2_up_vertical_0_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1)				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_vertical_30_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, math.sqrt(3)/2) 		  # goal angle 120 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_vertical_45_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_vertical_60_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, 1/2) 		  # goal angle 150 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_vertical_90_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_vertical_180_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-left diagonal -- #
    #    .   ∧ endpoint (-2, 2)
    #     \  |  
    #      * |
    # <------|
    # ref angle = 135°

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, 0.25881905) 		  # goal angle 165 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, -0.25881905) 		  # goal angle 195 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_up_left_diagonal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle 315 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- left horizontal -- #
    #        ∧ 
    #   .__. |
    # <------| endpoint (-2, 1)
    # ref angle = 180°
    
    def test_calculate_point_from_angle_quadrant2_left_horizontal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_left_horizontal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, -1/2) 		  # goal angle 210 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_left_horizontal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_left_horizontal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, -math.sqrt(3)/2) 		  # goal angle 240 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_left_horizontal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_left_horizontal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 				  # goal angle 360 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down-left diagonal -- #
    #        ∧ 
    #      . |
    #     /  |
    # <--*---| endpoint (-2, 0)
    # ref angle = -135°

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, -math.sqrt(2)/2)     # goal angle -135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, -0.96592583) 		  # goal angle -105 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, -0.96592583) 		  # goal angle -75 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_left_diagonal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(-2, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
    
    # -- down vertical -- #
    #        ∧ 
    #      . |
    #      | |
    # <----*-| endpoint (-1, 0)
    # ref angle = -90°

    def test_calculate_point_from_angle_quadrant2_down_vertical_0_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_vertical_30_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.5, -0.8660254) 			  # goal angle is -60 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_vertical_45_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_vertical_60_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, -1/2) 		  # goal angle is -30 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_vertical_90_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_vertical_180_degrees(self):
        start = Point(-1, 1)
        end = Point(-1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 					  # goal angle is 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down-right diagonal -- #
    #         ∧ 
    #      .  |
    #       \ |
    # <------\| endpoint (0, 0)
    # ref angle = -45°

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_0_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_30_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, -0.25881905) 		  # goal angle is -15 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_45_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_60_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, 0.25881905) 		  # goal angle is 15 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_90_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant2_down_right_diagonal_180_degrees(self):
        start = Point(-1, 1)
        end = Point(0, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] + 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -------------------------------- start at (-1, -1) - QUADRANT 3 ------------------------------- #
    
    # -- right horizontal -- #  
    # <------|
    #     .__. endpoint (0, -1)
    #        |
    #        V
    # ref angle = 0°

    def test_calculate_point_from_angle_quadrant3_right_horizontal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_right_horizontal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, 1/2) 		  # goal angle 30 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_right_horizontal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_right_horizontal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1/2, math.sqrt(3)/2) 		  # goal angle 60 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_right_horizontal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 					  # goal angle is 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_right_horizontal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 					  # goal angle is 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-right diagonal -- #
    # <------.| endpoint (0, 0)
    #       / |
    #      *  |
    #         V
    # ref angle = 45°

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, 0.96592583) 		  # goal angle 75 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1)				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, 0.96592583)		  # goal angle 105 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_right_diagonal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(0, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up vertical -- #
    # <----.-| endpoint (-1, 0)
    #      | |
    #      * |
    #        V
    # ref angle = 90°

    def test_calculate_point_from_angle_quadrant3_up_vertical_0_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1)				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_vertical_30_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, math.sqrt(3)/2) 		  # goal angle 120 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_vertical_45_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_vertical_60_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, 1/2) 		  # goal angle 150 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_vertical_90_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) # goal is 180 degrees 
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_vertical_180_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-left diagonal -- #
    # <--.---| endpoint (-2, 0)
    #     \  | 
    #      * |
    #        V
    # ref angle = 135°

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, 0.25881905) 		  # goal angle 165 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.96592583, -0.25881905) 		  # goal angle 195 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_up_left_diagonal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle 315 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- left horizontal -- #
    # <-------| endpoint (-2, -1)
    #   .___. | 
    #         V
    # ref angle = 180°
        
    def test_calculate_point_from_angle_quadrant3_left_horizontal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_left_horizontal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, -1/2) 		  # goal angle 210 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_left_horizontal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-(math.sqrt(2)/2), -(math.sqrt(2)/2)) # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])
        
    def test_calculate_point_from_angle_quadrant3_left_horizontal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, -math.sqrt(3)/2) 		  # goal angle 240 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_left_horizontal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_left_horizontal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 				  # goal angle 360 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down-left diagonal -- #
    # <-------| 
    #       . | 
    #      /  |
    #     *   | endpoint (-2, -2)
    #         V
    # ref angle = -135°

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle -135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-0.25881905, -0.96592583) # goal angle -105 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.25881905, -0.96592583) # goal angle -75 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_left_diagonal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(-2, -2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- down vertical -- #
    # <-------| 
    #       . | 
    #       | |
    #       * | endpoint (-1, -2)
    #         V
    # ref angle = -90°

    def test_calculate_point_from_angle_quadrant3_down_vertical_0_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 				  # goal angle -90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_vertical_30_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.5, -0.8660254) 			  # goal angle is -60 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_vertical_45_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_vertical_60_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, -1/2) 		  # goal angle is -30 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_vertical_90_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_vertical_180_degrees(self):
        start = Point(-1, -1)
        end = Point(-1, -2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 					  # goal angle is 90 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # <-------| 
    #       . | 
    #        \|
    #         * endpoint (0, -2)
    #         |
    #         V
    # ref angle = -90°

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_0_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, -math.sqrt(2)/2) 	  # goal angle -45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_30_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, -0.25881905) 		  # goal angle is -15 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_45_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 					  # goal angle is 0 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_60_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0.96592583, 0.25881905) 		  # goal angle is 15 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_90_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant3_down_right_diagonal_180_degrees(self):
        start = Point(-1, -1)
        end = Point(0, -2)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] - 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])


   # -------------------------------- start at (1, -1) - QUADRANT 4 ------------------------------- #

   # -- right horizontal -- #
   # |------>
   # | .___. endpoint (2, -1)
   # |
   # V
   # ref angle = 0°

    def test_calculate_point_from_angle_quadrant4_right_horizontal_0_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1, 0) 				  # goal angle 0 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_right_horizontal_30_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(3)/2, 1/2) 		  # goal angle 30 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_right_horizontal_45_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 		  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_right_horizontal_60_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (1/2, math.sqrt(3)/2) 		  # goal angle 60 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_right_horizontal_90_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_right_horizontal_180_degrees(self):
        start = Point(1, -1)
        end = Point(2, -1)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 				  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up-right diagonal -- # #
    # |----.----> endpoint(2, 0)
    # |   /  
    # V  *  
    # REF_ANGLE = 45

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_0_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 45 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_30_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.cos(math.radians(45 + 30)), math.sin(math.radians(45 + 30))) 		  # goal angle 75 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_45_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) 				  # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_60_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.cos(math.radians(45 + 60)), math.sin(math.radians(45 + 60))) 		  # goal angle 105 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_90_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)


        expected_before_offset = (math.cos(math.radians(45 + 90)), math.sin(math.radians(45 + 90))) 		  # goal angle 135 degrees
        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees


        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_right_diagonal_180_degrees(self):
        start = Point(1, -1)
        end = Point(2, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (math.cos(math.radians(45 + 180)), math.sin(math.radians(45 + 180))) 		  # goal angle 225 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    # -- up vertical -- #
   # |-.-----> endpoint (1, 0)
   # | |
   # | *
   # V
   # ref angle = 90°
    def test_calculate_point_from_angle_quadrant4_up_vertical_0_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(0)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, 1) # goal angle 90 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_vertical_30_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(30)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1/2, math.sqrt(3)/2)  # goal angle 120 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_vertical_45_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(45)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(2)/2, math.sqrt(2)/2) 	  # goal angle 135 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_vertical_60_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(60)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-math.sqrt(3)/2, 1/2) 		  # goal angle 150 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_vertical_90_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(90)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (-1, 0) 		  # goal angle 180 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

    def test_calculate_point_from_angle_quadrant4_up_vertical_180_degrees(self):
        start = Point(1, -1)
        end = Point(1, 0)
        given_angle = math.radians(180)

        new_point =  Geometry.calculate_point_from_angle(given_angle, start, end)

        expected_before_offset = (0, -1) 		  # goal angle 270 degrees
        expected_after_offset = (expected_before_offset[0] + 1, expected_before_offset[1] - 1)

        self.assertAlmostEqual(new_point.x, expected_after_offset[0])
        self.assertAlmostEqual(new_point.y, expected_after_offset[1])

if __name__ == "__main__":
    unittest.main()