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


    #------------------------------------------Get Second Point-----------------------------------------
    # normal
    def test_get_second_point(self):
        pass

    #----------------------------------------Get Third Point Scenarios----------------------------------
    # more than one scenario in (this will never happen)
    # one scenario in list
    # empty scenario list (this also should never happen)

    #------------------------------------------Get Third Points-----------------------------------------
    # normal

    #---------------------------------------Get Next Point Scenarios--------------------------------------
    # getting fourth
    # getting fifth
    # one scenario in
    # two scenario in
    # no scenarios in

    #------------------------------------------Get Next Point-----------------------------------------
    # positive angle
    # negative angle

    #---------------------------------------Get Rotated Scenarios-------------------------------------
    # one scenario in
    # multiple scenario in (2)

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

    #------------------------------------------Are Pentagons-----------------------------------------
    # a scenario not len 5
    # a scenario contains None

if __name__ == "__main__":
    unittest.main()