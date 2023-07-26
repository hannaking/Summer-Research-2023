import unittest
import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

sys.path.insert(0, './Summer-Research-2022/')

from septagon.septagon import Septagon
from shapely.geometry import Point

# it's in the unit circle
# [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
#  Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
#  Point(1, 0),
#  Point(1 * math.cos(math.pi * 2 / 7), 1 * math.sin(math.pi * 2 / 7)),
#  Point(1 * math.cos(math.pi * 4 / 7), 1 * math.sin(math.pi * 4 / 7)),
#  Point(1 * math.cos(math.pi * 6 / 7), 1 * math.sin(math.pi * 6 / 7)),
#  Point(1 * math.cos(math.pi * 8 / 7), 1 * math.sin(math.pi * 8 / 7))]

class TestSeptagon(unittest.TestCase):
    #-----------------------------------------------Init--------------------------------------------
    def test_init(self):
        point_list = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4), Point(5,5), Point(6,6)]
        sept = Septagon(point_list)
        self.assertEqual(sept._points, point_list)

    #------------------------------------------Coordinatize-----------------------------------------
    # 7 Points in
    # 6 Points in
    # 5 Points in
    # 4 Points in
    # 3 Points in
    # 2 Points in (edge glued)
    # 1 Point in (vertex glued)
    def test_coordinatize_7_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      Point(1, 0),
                      Point(1 * math.cos(math.pi * 2 / 7), 1 * math.sin(math.pi * 2 / 7)),
                      Point(1 * math.cos(math.pi * 4 / 7), 1 * math.sin(math.pi * 4 / 7)),
                      Point(1 * math.cos(math.pi * 6 / 7), 1 * math.sin(math.pi * 6 / 7)),
                      Point(1 * math.cos(math.pi * 8 / 7), 1 * math.sin(math.pi * 8 / 7))]
        sept = Septagon(point_list)
        scenarios = sept.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], point_list)

    def test_coordinatize_6_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      Point(1, 0),
                      Point(1 * math.cos(math.pi * 2 / 7), 1 * math.sin(math.pi * 2 / 7)),
                      Point(1 * math.cos(math.pi * 4 / 7), 1 * math.sin(math.pi * 4 / 7)),
                      Point(1 * math.cos(math.pi * 6 / 7), 1 * math.sin(math.pi * 6 / 7)),
                      None]
        sept = Septagon(point_list)
        scenarios = sept.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(sept.are_septagons(scenarios))

    def test_coordinatize_5_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      Point(1, 0),
                      Point(1 * math.cos(math.pi * 2 / 7), 1 * math.sin(math.pi * 2 / 7)),
                      Point(1 * math.cos(math.pi * 4 / 7), 1 * math.sin(math.pi * 4 / 7)),
                      None, None]
        sept = Septagon(point_list)
        scenarios = sept.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(sept.are_septagons(scenarios))
    
    def test_coordinatize_4_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      Point(1, 0),
                      Point(1 * math.cos(math.pi * 2 / 7), 1 * math.sin(math.pi * 2 / 7)),
                      None, None, None]
        sept = Septagon(point_list)
        
        scenarios = sept.coordinatize()
        
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(sept.are_septagons(scenarios))
    
    def test_coordinatize_3_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      Point(1, 0),
                      None, None, None, None]
        sept = Septagon(point_list)
        scenarios = sept.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(sept.are_septagons(scenarios))

    def test_coordinatize_2_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      Point(1 * math.cos(math.pi * 12 / 7), 1 * math.sin(math.pi * 12 / 7)),
                      None, None, None, None, None]
        sept = Septagon(point_list)
        scenarios = sept.coordinatize()
        self.assertEqual(len(scenarios), 2)
        self.assertTrue(sept.are_septagons(scenarios))

    def test_coordinatize_1_in(self):
        point_list = [Point(1 * math.cos(math.pi * 10 / 7), 1 * math.sin(math.pi * 10 / 7)),
                      None, None, None, None, None, None]
        sept = Septagon(point_list)
        
        scenarios = sept.coordinatize()
        
        self.assertEqual(len(scenarios), 20)
        self.assertTrue(sept.are_septagons(scenarios))

    # support methods match pentagon, no need to test here

if __name__ == "__main__":
    unittest.main()