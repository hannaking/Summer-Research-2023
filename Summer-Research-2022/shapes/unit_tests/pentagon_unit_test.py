import unittest
import sys
import math

sys.path.insert(0, './Summer-Research-2022/')

from shapes.pentagon.pentagon import Pentagon
from shapely.geometry import *
from lattice import Lattice
from shapes.geometry import Geometry

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

# I think there will be rounding inaccuracies in the asserts, making them fail

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
        point_list = [Point(0,0), Point(1,0), Point(1.31, 0.95), Point(0.5, 1.5), Point(-0.31, 0.95)]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], point_list)
    
    def test_coordinatize_4_in(self):
        point_list = [Point(0,0), Point(1,0), Point(1.31, 0.95), Point(0.5, 1.5), None]
        pent = Pentagon(point_list)
        print("------------------------------here-------------------------------")
        scenarios = pent.coordinatize()
        print("------------------------------done--------------------------------")
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], [Point(0,0), Point(1,0), Point(1.31, 0.95), Point(0.5, 1.5), Point(-0.31, 0.95)])
    
    def test_coordinatize_3_in(self):
        point_list = [Point(0,0), Point(1,0), Point(1.31, 0.95), None, None]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0], [Point(0,0), Point(1,0), Point(1.31, 0.95), Point(0.5, 1.5), Point(-0.31, 0.95)])

    def test_coordinatize_2_in(self):
        point_list = [Point(0,0), Point(1,0), None, None, None]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 2)
        self.assertTrue([Point(0,0), Point(1,0), Point(1.31, 0.95), Point(0.5, 1.5), Point(-0.31, 0.95)] in scenarios)
        self.assertTrue([Point(0,0), Point(1,0), Point(1.31, -0.95), Point(0.5, -1.5), Point(-0.31, -0.95)] in scenarios)

    def test_coordinatize_1_in(self): # also vertex glued test
        point_list = [Point(0,0), None, None, None, None]
        pent = Pentagon(point_list)
        scenarios = pent.coordinatize()
        self.assertEqual(len(scenarios), 20)

if __name__ == "__main__":
    unittest.main()