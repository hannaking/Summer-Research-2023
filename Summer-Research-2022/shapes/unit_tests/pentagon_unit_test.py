import unittest
import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

sys.path.insert(0, './Summer-Research-2022/')

from pentagon.pentagon import Pentagon
from shapely.geometry import Point
from geometry import Geometry

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

#[Point(0, 10),
# Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18))),
# Point(10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
# Point(-10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
# Point(-10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))]

class TestPentagon(unittest.TestCase):
    #-----------------------------------------------Init--------------------------------------------
    def test_init(self):
        point_list = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)]
        pent = Pentagon(point_list)
        self.assertEqual(pent._points, point_list)

    #------------------------------------------Coordinatize-----------------------------------------
    # 5 Points in
    # 4 Points in
    # 3 Points in
    # 2 Points in (edge glued)
    # 1 Point in (vertex glued)
    def test_coordinatize_5_in(self):
        point_list = [Point(0, 1),
                      Point( math.sqrt(10 + 2*math.sqrt(5)) / 4,  (math.sqrt(5) - 1) / 4),
                      Point( math.sqrt(10 - 2*math.sqrt(5)) / 4, -(math.sqrt(5) + 1) / 4),
                      Point(-math.sqrt(10 - 2*math.sqrt(5)) / 4, -(math.sqrt(5) + 1) / 4),
                      Point(-math.sqrt(10 + 2*math.sqrt(5)) / 4,  (math.sqrt(5) - 1) / 4)]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], point_list)
    
    def test_coordinatize_4_in(self):
        point_list = [Point(0, 1),
                      Point( math.sqrt(10 + 2*math.sqrt(5)) / 4,  (math.sqrt(5) - 1) / 4),
                      Point( math.sqrt(10 - 2*math.sqrt(5)) / 4, -(math.sqrt(5) + 1) / 4),
                      Point(-math.sqrt(10 - 2*math.sqrt(5)) / 4, -(math.sqrt(5) + 1) / 4),
                      None]
        pent = Pentagon(point_list)
        
        scenarios = pent.coordinatize()
        
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Pentagon.are_pentagons(scenarios))
    
    def test_coordinatize_3_in(self):
        point_list = [Point(0, 1),
                      Point( math.sqrt(10 + 2*math.sqrt(5)) / 4,  (math.sqrt(5) - 1) / 4),
                      Point( math.sqrt(10 - 2*math.sqrt(5)) / 4, -(math.sqrt(5) + 1) / 4),
                      None,
                      None]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Pentagon.are_pentagons(scenarios))

    def test_coordinatize_2_in(self):
        point_list = [Point(0,0), Point(1,0), None, None, None]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 2)
        self.assertTrue(pent.are_pentagons(scenarios))

    def test_coordinatize_1_in(self):
        point_list = [Point(0,0), None, None, None, None]
        pent = Pentagon(point_list)
        
        scenarios = pent.coordinatize()
        
        self.assertEqual(len(scenarios), 20)

    #----------------------------------------Get Second Point Scenario-------------------------------------
    # more than one scenario in (this will never happen)
    # one scenario in list
    # empty scenario list (this also should never happen)
    def test_get_second_point_scenario_multiple(self):
        point1 = Point(0,0)
        scenarios = [[point1, None, None, None, None],
                     [point1, None, None, None, None]]
        # so i can use the method
        pent = Pentagon([point1, None, None, None, None])
        new_scenarios = pent.get_second_point_scenario(scenarios)
        self.assertEquals(2, len(new_scenarios))
        self.assertEquals(3, sum([1 for _ in new_scenarios[0] if _ is None]))
        self.assertEquals(3, sum([1 for _ in new_scenarios[1] if _ is None]))
        self.assertEquals([point1, Point(1,0), None, None, None], new_scenarios[0])
        self.assertEquals([point1, Point(1,0), None, None, None], new_scenarios[1])

    def test_get_second_point_scenario_one(self):
        point1 = Point(0,0)
        scenarios = [[point1, None, None, None, None]]
        pent = Pentagon([point1, None, None, None, None])
        new_scenarios = pent.get_second_point_scenario(scenarios)
        self.assertEquals(1, len(new_scenarios))
        self.assertEquals(3, sum([1 for _ in new_scenarios[0] if _ is None]))
        self.assertEquals([point1, Point(1,0), None, None, None], new_scenarios[0])

    def test_get_second_point_scenario_empty(self):
        point1 = Point(0,0)
        scenarios = []
        pent = Pentagon([point1, None, None, None, None])
        new_scenarios = pent.get_second_point_scenario(scenarios)
        self.assertEquals(0, len(new_scenarios))

    #------------------------------------------Get Second Point-----------------------------------------
    # normal
    def test_get_second_point(self):
        point1 = Point(0,0)
        pent = Pentagon([point1, None, None, None, None])
        point2 = pent.get_second_point(point1)
        self.assertEqual(point2, Point(1,0))

    #----------------------------------------Get Third Point Scenarios----------------------------------
    # more than one scenario in (this will never happen)
    # one scenario in list
    # empty scenario list (this also should never happen)
    def test_get_third_point_scenarios_multiple(self):
        point1 = Point(0,10)
        point2 = Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))
        pent = Pentagon([point1, point2, None, None, None])
        scenarios = [[point1, point2, None, None, None], [point1, point2, None, None, None]]
        new_scenarios = pent.get_third_point_scenarios(scenarios)
        self.assertEquals(4, len(new_scenarios))
        # next test will check values
    def test_get_third_point_scenarios_one(self):
        point1 = Point(0,10)
        point2 = Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))
        pent = Pentagon([point1, point2, None, None, None])
        scenarios = [[point1, point2, None, None, None]]
        new_scenarios = pent.get_third_point_scenarios(scenarios)
        self.assertEquals(2, len(new_scenarios))
        # checking values in get third point, so no need to here

    def test_get_third_point_scenarios_empty(self):
        pent = Pentagon([None, None, None, None, None])
        scenarios = []
        new_scenarios = pent.get_third_point_scenarios(scenarios)
        self.assertEquals(0, len(new_scenarios))

    #------------------------------------------Get Third Points-----------------------------------------
    # normal
    def test_get_third_points(self):
        point1 = Point(0,10)
        point2 = Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))
        pent = Pentagon([point1, point2, None, None, None])
        point3s = pent.get_third_point(point1, point2)
        self.assertEquals(2, len(point3s))
        self.assertTrue(pent.is_pentagonable(point1, point2, point3s[0], None, None))
        self.assertTrue(pent.is_pentagonable(point1, point2, point3s[1], None, None))

    #---------------------------------------Get Next Point Scenarios--------------------------------------
    # getting fourth
    # getting fifth
    # two scenario in
    # no scenarios in
    # values checked in get next point test, so just checking quantity here
    def test_get_next_point_scenarios_fourth(self):
        point1 = Point(0,0)
        point2 = Point(1,0)
        point3 = Point(1,1)
        pent = Pentagon([point1, point2, point3, None, None])
        scenarios = [[point1, point2, point3, None, None]]
        new_scenarios = pent.get_next_point_scenarios(scenarios, )
        self.assertEquals(1, len(new_scenarios))
    def test_get_next_point_scenarios_fifth(self):
        point1 = Point(0,0)
        point2 = Point(1,0)
        point3 = Point(1,1)
        point4 = Point(0,1)
        pent = Pentagon([point1, point2, point3, point4, None])
        scenarios = [[point1, point2, point3, point4, None]]
        new_scenarios = pent.get_next_point_scenarios(scenarios)
        self.assertEquals(1, len(new_scenarios))
    def test_get_next_point_scenarios_two(self):
        point1 = Point(0,0)
        point2 = Point(1,0)
        pent = Pentagon([point1, point2, None, None, None])
        scenarios = [[point1, point2, None, None, None], [point1, point2, None, None, None]]
        new_scenarios = pent.get_next_point_scenarios(scenarios)
        self.assertEquals(2, len(new_scenarios))
    def test_get_next_point_scenarios_empty(self):
        point1 = Point(0,0)
        point2 = Point(1,0)
        pent = Pentagon([point1, point2, None, None, None])
        scenarios = []
        new_scenarios = pent.get_next_point_scenarios(scenarios)
        self.assertEquals(0, len(new_scenarios))

    #------------------------------------------Get Next Point-----------------------------------------
    # positive angle
    # negative angle
    def test_get_next_point_positive(self):
        point1 = Point(0,10)
        point2 = Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))
        point3 = Point(10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
        point4 = Point(-10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
        # expected 5: Point(-10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))]
        pent = Pentagon([point1, point2, point3, point4, None])
        point5 = pent.get_next_point(point1, point2, point3, point4)
        self.assertEquals(Point(-10*math.cos(math.radians(18)), 10*math.sin(math.radians(18))), point5)
    def test_get_next_point_negative(self):
        point1 = Point(0,10)
        point2 = Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18)))
        pent = Pentagon([point1, point2, None, None, None])
        point3 = pent.get_third_points(point1, point2)[1]
        pent.get_next_point(point1, point2, point3)
        self.assertTrue(pent.is_pentagonable(point1, point2, point3, None, None))

    #---------------------------------------Get Rotated Scenarios-------------------------------------
    # one scenario in
    # multiple scenario in (2)
    #rotated is tested so only checking quantity here
    def test_get_rotated_scenarios_one(self):
        scenarios = [[Point(0,0), Point(1,0), Point(2,0), Point(3,0), Point(4,0)]]
        pent = Pentagon(scenarios[0])
        rotated_scenarios = pent.get_rotated_scenarios(scenarios)
        self.assertEquals(10, len(rotated_scenarios))
    def test_get_rotated_scenarios_multiple(self):
        scenarios = [[Point(0,0), Point(1,0), Point(2,0), Point(3,0), Point(4,0)],
                     [Point(0,0), Point(1,0), Point(2,0), Point(3,0), Point(4,0)]]
        pent = Pentagon(scenarios[0])
        rotated_scenarios = pent.get_rotated_scenarios(scenarios)
        self.assertEquals(20, len(rotated_scenarios))

    #------------------------------------------Verify Pentagon-----------------------------------------
    # not testing - only action is to call are_pentagons

    #--------------------------------------Verify Pentagon n Points-----------------------------------------
    # not testing - only action is to call are_pentagonable

    #------------------------------------------Are Pentagonable-----------------------------------------
    # one of the scenarios has wrong len
    # num present sides < 3
    # has noned and point != None
    # first angle wrong
    # other angle wrong
    # a side wrong
    def test_are_pentagonable_len(self):
        scenarios = [[Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)],
                     [Point(0,0), Point(1,1), Point(2,2), Point(3,3)]]
        self.assertFalse(Pentagon.are_pentagonable(scenarios))
    def test_are_pentagonable_side(self):
        scenarios = [[Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)],
                     [Point(0,0), Point(1,1), Point(2,2), Point(3,3), None]]
        self.assertFalse(Pentagon.are_pentagonable(scenarios))
    def test_are_pentagonable_noned(self):
        scenarios = [[Point(0,0), Point(1,1), Point(2,2), None, Point(4,4)]]
        self.assertFalse(Pentagon.are_pentagonable(scenarios))
    def test_are_pentagonable_first_angle(self):
        # points beyond 3 don't matter for this test
        scenarios = [[Point(0,0), Point(1,0), Point(1,1), Point(0,0), Point(0,0)]]
        pent = Pentagon(scenarios[0])
        self.assertFalse(pent.are_pentagonable(scenarios))
    def test_are_pentagonable_other_angle(self):
        scenarios = [[Point(0, 10),
                      Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18))),
                      Point(10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
                      Point(-10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
                      Point(1,1)]]
        pent = Pentagon(scenarios[0])
        self.assertFalse(pent.are_pentagonable(scenarios))
    def test_are_pentagonable_side(self):
        scenarios = [[Point(0, 10),
                        Point(10*math.cos(math.radians(18)), 10*math.sin(math.radians(18))),
                        Point(10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
                        Point(-10*math.cos(math.radians(54)), -10*math.sin(math.radians(54))),
                        # last point is 2*side_length away from 4th point
                        Point(-10*math.cos(math.radians(18))-10*math.cos(math.radians(18)+10*math.cos(math.radians(54))), 20*math.sin(math.radians(18))+10*math.sin(math.radians(54)))]]
        pent = Pentagon(scenarios[0])
        self.assertFalse(pent.are_pentagonable(scenarios))

    #------------------------------------------Are Pentagons-----------------------------------------
    # a scenario not len 5
    # a scenario contains None
    # then the tests are in are_pentagonable
    def test_are_pentagons_len(self):
        scenarios = [[Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)],
                     [Point(0,0), Point(1,1), Point(2,2), Point(3,3)]]
        self.assertFalse(Pentagon.are_pentagons(scenarios))
    def test_are_pentagons_none(self):
        scenarios = [[Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)],
                     [Point(0,0), Point(1,1), Point(2,2), Point(3,3), None]]
        self.assertFalse(Pentagon.are_pentagons(scenarios))

if __name__ == "__main__":
    unittest.main()