import math
import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *
from quadrilaterals.kite import Kite
from shape_generator import ShapeGenerator

sys.path.append("Summer-Research-2022")

from lattice import Lattice

class TestKite(unittest.TestCase):
    '''
    
    Helper Methods
    
    '''
    
    @staticmethod
    def show_failed(scenarios):
        for scenario in scenarios:
                if not Kite.are_kites([scenario]):
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

# ==================================================== coordinatize() tests ====================================================

    def test_coordinatize_1_point(self):
        points = [Point(0, 0), None, None, None]
        shape = Kite(points)
        scenarios = shape.coordinatize()
        TestKite.show_failed(scenarios)
        self.assertTrue(Kite.are_kites(scenarios))
        self.assertEqual(len(scenarios), 80)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

    def test_coordinatize_2_points(self):
        points = [Point(0, 0), Point(0, 1), None, None]
        shape = Kite(points)
        scenarios = shape.coordinatize()
        TestKite.show_failed(scenarios)
        self.assertTrue(Kite.are_kites(scenarios))
        self.assertEqual(len(scenarios), 80)
        unique = set()
        for scenario in scenarios:
            self.assertNotIn(tuple(scenario), unique)
            unique.add(tuple(scenario))

# ================================================== get_second_point() tests ==================================================

    def test_get_second_point_int(self):
        pt1 = Point(1,1)
        shape = Kite([pt1])
        second_points = shape.get_second_point(pt1)

        self.assertAlmostEqual(second_points[0].x, 1 + 1)
        self.assertAlmostEqual(second_points[0].y, 1)
        self.assertAlmostEqual(second_points[1].x, 1 + math.sqrt(3))
        self.assertAlmostEqual(second_points[1].y, 1)

    def test_get_second_point_irrational(self):
        pt1 = Point(math.pi, math.e)
        shape = Kite([[pt1]])
        second_points = shape.get_second_point(pt1)

        self.assertAlmostEqual(second_points[0].x, math.pi + 1)
        self.assertAlmostEqual(second_points[0].y, math.e)
        self.assertAlmostEqual(second_points[1].x, math.pi + math.sqrt(3))
        self.assertAlmostEqual(second_points[1].y, math.e)

# ==================================================== _verify_kite() tests ====================================================
    
    def test_verify_kite_square(self):
        coords = [Point(0,0), Point(-1,1), Point(0,2), Point(1,1)]
        shape = Kite(coords)
        self.assertTrue(shape._verify_kite())

    def test_verify_kite_1_long(self):
        coords = [Point(0,0), Point(1,-2), Point(2,0), Point(1,1)]
        shape = Kite(coords)
        self.assertTrue(shape._verify_kite())

    def test_verify_kite_2_long(self):
        coords = [Point(0,0), Point(1,-2), Point(0,-4), Point(-1,-2)]
        shape = Kite(coords)
        self.assertTrue(shape._verify_kite())

    def test_verify_kite_dart(self):
        coords = [Point(0,0), Point(-1,1), Point(-2,0), Point(-1,3)]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_same_intercept(self):
        coords = [Point(0,0), Point(1,-1), Point(-1,0), Point(1,-2)]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_diagonals_inside(self):
        coords = [Point(0,0), Point(2,-1), Point(1,-2), Point(-1,-1)]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_too_many(self):
        coords = [Point(0,0), Point(1,-1), Point(0,-3), Point(-1,-1), Point(-2, 0)]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_too_few(self):
        coords = [Point(0,0), Point(1,-1), Point(0,-3)]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_extra_none(self):
        coords = [Point(0,0), Point(1,-1), Point(0,-3), Point(-1,-1), None]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

    def test_verify_kite_none(self):
        coords = [Point(0,0), Point(1,-1), Point(0,-3), None]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite())

# =============================================== _verify_kite_3_points() tests ================================================

    def test_verify_kite_3_points_midpoint(self):
        coords = [Point(0,0), Point(1,1), Point(2,0), None]
        shape = Kite(coords)
        self.assertTrue(shape._verify_kite_3_points())

    def test_verify_kite_3_points_nonmidpoint(self):
        coords = [Point(0,0), Point(-2,1), Point(-3,0), None]
        shape = Kite(coords)
        self.assertTrue(shape._verify_kite_3_points())
    
    def test_verify_kite_3_points_psudotriangle(self):
        coords = [Point(0,0), Point(0,1), Point(2,0), None]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite_3_points())

    def test_verify_kite_3_points_half_dart(self):
        coords = [Point(0,0), Point(-1,1), Point(1,0), None]
        shape = Kite(coords)
        self.assertFalse(shape._verify_kite_3_points())

if __name__ == "__main__":
    unittest.main()