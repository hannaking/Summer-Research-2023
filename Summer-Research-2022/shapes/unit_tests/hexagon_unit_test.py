import unittest
import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

sys.path.insert(0, './Summer-Research-2022/')

from hexagon.hexagon import Hexagon
from shapely.geometry import Point

# it's in the unit circle
# [Point(1 * math.cos(math.radians(240)), (1 * math.sin(math.radians(240))),
#  Point(1 * math.cos(math.radians(300)), (1 * math.sin(math.radians(300))),
#  Point(1, 0),
#  Point(1 * math.cos(math.radians(60)), (1 * math.sin(math.radians(60))),
#  Point(1 * math.cos(math.radians(120)), (1 * math.sin(math.radians(120))),
#  Point(-1, 0)]

class TestHexagon(unittest.TestCase):
    #-----------------------------------------------Init--------------------------------------------
    def test_init(self):
        point_list = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4), Point(5,5)]
        hex = Hexagon(point_list)
        self.assertEqual(hex._points, point_list)

    #------------------------------------------Coordinatize-----------------------------------------
    # 6 Points in
    # 5 Points in
    # 4 Points in
    # 3 Points in
    # 2 Points in (edge glued)
    # 1 Point in (vertex glued)
    def test_coordinatize_6_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      Point(1 * math.cos(math.radians(300)), 1 * math.sin(math.radians(300))),
                      Point(1, 0),
                      Point(1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60))),
                      Point(1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120))),
                      Point(-1, 0)]
        hex = Hexagon(point_list)
        scenarios = hex.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], point_list)

    def test_coordinatize_5_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      Point(1 * math.cos(math.radians(300)), 1 * math.sin(math.radians(300))),
                      Point(1, 0),
                      Point(1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60))),
                      Point(1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120))),
                      None]
        hex = Hexagon(point_list)
        scenarios = hex.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Hexagon.are_hexagons(scenarios))
    
    def test_coordinatize_4_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      Point(1 * math.cos(math.radians(300)), 1 * math.sin(math.radians(300))),
                      Point(1, 0),
                      Point(1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60))),
                      None, None]
        hex = Hexagon(point_list)
        
        scenarios = hex.coordinatize()
        
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Hexagon.are_hexagons(scenarios))
    
    def test_coordinatize_3_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      Point(1 * math.cos(math.radians(300)), 1 * math.sin(math.radians(300))),
                      Point(1, 0),
                      None, None, None]
        hex = Hexagon(point_list)
        scenarios = hex.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(Hexagon.are_hexagons(scenarios))

    def test_coordinatize_2_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      Point(1 * math.cos(math.radians(300)), 1 * math.sin(math.radians(300))),
                      None, None, None, None]
        hex = Hexagon(point_list)
        scenarios = hex.coordinatize()
        self.assertEqual(len(scenarios), 2)
        self.assertTrue(hex.are_hexagons(scenarios))

    def test_coordinatize_1_in(self):
        point_list = [Point(1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240))),
                      None, None, None, None, None]
        hex = Hexagon(point_list)
        
        scenarios = hex.coordinatize()
        
        self.assertEqual(len(scenarios), 20)
        self.assertTrue(hex.are_hexagons(scenarios))

    # support methods match pentagon, no need to test here

if __name__ == "__main__":
    unittest.main()