import unittest
import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

sys.path.insert(0, './Summer-Research-2022/')

from octagon.octagon import Octagon
from shapely.geometry import Point

# it's in the unit circle
# [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
#  Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
#  Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
#  Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
#  Point(1 * math.cos(math.radians(67.5)), 1 * math.sin(math.radians(67.5))),
#  Point(1 * math.cos(math.radians(112.5)), 1 * math.sin(math.radians(112.5))),
#  Point(1 * math.cos(math.radians(157.5)), 1 * math.sin(math.radians(157.5))),
#  Point(1 * math.cos(math.radians(202.5)), 1 * math.sin(math.radians(202.5)))]

class TestOctagon(unittest.TestCase):
    #-----------------------------------------------Init--------------------------------------------
    def test_init(self):
        point_list = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4), Point(5,5), Point(6,6)]
        oct = Octagon(point_list)
        self.assertEqual(oct._points, point_list)

    #------------------------------------------Coordinatize-----------------------------------------
    # 8 Points in
    # 7 Points in
    # 6 Points in
    # 5 Points in
    # 4 Points in
    # 3 Points in
    # 2 Points in (edge glued)
    # 1 Point in (vertex glued)
    def test_coordinatize_8_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
                      Point(1 * math.cos(math.radians(67.5)), 1 * math.sin(math.radians(67.5))),
                      Point(1 * math.cos(math.radians(112.5)), 1 * math.sin(math.radians(112.5))),
                      Point(1 * math.cos(math.radians(157.5)), 1 * math.sin(math.radians(157.5))),
                      Point(1 * math.cos(math.radians(202.5)), 1 * math.sin(math.radians(202.5)))]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], point_list)

    def test_coordinatize_7_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
                      Point(1 * math.cos(math.radians(67.5)), 1 * math.sin(math.radians(67.5))),
                      Point(1 * math.cos(math.radians(112.5)), 1 * math.sin(math.radians(112.5))),
                      Point(1 * math.cos(math.radians(157.5)), 1 * math.sin(math.radians(157.5))),
                      None]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(oct.are_octagons(scenarios))

    def test_coordinatize_6_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
                      Point(1 * math.cos(math.radians(67.5)), 1 * math.sin(math.radians(67.5))),
                      Point(1 * math.cos(math.radians(112.5)), 1 * math.sin(math.radians(112.5))),
                      None, None]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(oct.are_octagons(scenarios))

    def test_coordinatize_5_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
                      Point(1 * math.cos(math.radians(67.5)), 1 * math.sin(math.radians(67.5))),
                      None, None, None]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(oct.are_octagons(scenarios))
    
    def test_coordinatize_4_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      Point(1 * math.cos(math.radians(22.5)), 1 * math.sin(math.radians(22.5))),
                      None, None, None, None]
        oct = Octagon(point_list)
        
        scenarios = oct.coordinatize()
        
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(oct.are_octagons(scenarios))
    
    def test_coordinatize_3_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      Point(1 * math.cos(math.radians(337.5)), 1 * math.sin(math.radians(337.5))),
                      None, None, None, None, None]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertTrue(oct.are_octagons(scenarios))

    def test_coordinatize_2_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      Point(1 * math.cos(math.radians(292.5)), 1 * math.sin(math.radians(292.5))),
                      None, None, None, None, None, None]
        oct = Octagon(point_list)
        scenarios = oct.coordinatize()
        self.assertEqual(len(scenarios), 2)
        self.assertTrue(oct.are_octagons(scenarios))

    def test_coordinatize_1_in(self):
        point_list = [Point(1 * math.cos(math.radians(247.5)), 1 * math.sin(math.radians(247.5))),
                      None, None, None, None, None, None, None]
        oct = Octagon(point_list)
        
        scenarios = oct.coordinatize()
        
        self.assertEqual(len(scenarios), 20)
        self.assertTrue(oct.are_octagons(scenarios))

    # support methods match pentagon, no need to test here

if __name__ == "__main__":
    unittest.main()