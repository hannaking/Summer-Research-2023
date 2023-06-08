import unittest
import sys
import math

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from node import Node
from shapes.shape_generator import ShapeGenerator
from shapes.vector import Vector
from shapely.geometry import Polygon, Point
from lattice import Lattice
from unit_tests.shape_helpers import ShapeHelpers

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

DEFAULT_SIDE_LENGTH = 1

    # for copy and pasting for pretty pictures <3 <3 <3
    #         ∧
    #         |
    # <-------|-------> 
    #         |
    #         ∨

class TestShapeGenerator(unittest.TestCase):

    # ----------------------------- scenario to polygons ---------------------- #
    def test_scenario_to_polygons_simple_triangle(self):
        lattice = Lattice(3)
        gen = ShapeGenerator()
        gen.generate_by_lattice_traversal(lattice)
        
        scenario = [
            Point(0,0), Point(1,0), Point(1/2, math.sqrt(3)/2)
        ]

        polygons = gen._scenario_to_polygons(scenario, lattice)

        self.assertEqual(len(polygons), 1) # we only have one shape
        coords_got = polygons[0].exterior.coords
        for i in range(len(scenario)):
            self.assertAlmostEqual(coords_got[i][0], scenario[i].x)
            self.assertAlmostEqual(coords_got[i][1], scenario[i].y)

    def test_scenario_to_polygons_bowtie(self):
        lattice = ShapeHelpers.bowtie()
        gen = ShapeGenerator()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(1,0), Point(0,0), Point(0,1),
            Point(2,0), Point(2,1)

        ]

        polygons = gen._scenario_to_polygons(scenario, lattice)

        self.assertEqual(len(polygons), 2) # we have two shapes
        
        coords_got_polygon1 = [x for x in polygons[0].exterior.coords]
        expected_coords_polygon1 = [
            (1,0), (0,0), (0,1), (1,0)
        ]
        coords_got_polygon2 = [x for x in polygons[1].exterior.coords]
        expected_coords_polygon2 = [
            (1,0), (2,0), (2,1), (1,0)
        ]

        self.assertCountEqual(coords_got_polygon1, expected_coords_polygon1)
        self.assertCountEqual(coords_got_polygon2, expected_coords_polygon2)

    # ----------------------- intersects without touching ---------------- #

    # two triangles completely apart from each other
    def test_intersects_without_touching_not_even_close(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (1,0), (0,1)])
        poly2 = Polygon([(5,0), (6,0), (5,1)])
        self.assertFalse(gen.intersects_without_touching(poly1, poly2))

    # vertex glued
    def test_intersects_without_touching_touching_at_vertex(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (1,0), (0,1)])
        poly2 = Polygon([(1,0), (2,0), (2,1)])
        self.assertFalse(gen.intersects_without_touching(poly1, poly2))

    # touching edge at one point
    def test_intersects_without_touching_touching_at_edge(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (1,0), (1,3)])
        poly2 = Polygon([(1,2), (2,2), (2,0)])
        self.assertFalse(gen.intersects_without_touching(poly1, poly2))

    def test_intersects_without_touching_intersecting_in_middle(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        poly2 = Polygon([(1,2), (3,1), (3,4)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))

    def test_intersects_without_touching_inside_connected_at_one_vertex(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        poly2 = Polygon([(0,0), (1,0), (0,1)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))

    def test_intersects_without_touching_inside_connected_at_one_edge(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        poly2 = Polygon([(2,0), (2,4), (1,3)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))  

    def test_intersects_without_touching_intersects_through(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        poly2 = Polygon([(3,0), (3,3), (-1,2)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))

    def test_intersects_without_touching_intersects_completely_covers(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        poly2 = Polygon([(0,0), (2,0), (2,4), (0,4)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))

    def test_intersects_without_touching_through_at_one_vertex(self):
        gen = ShapeGenerator()
        poly1 = Polygon([(0,0), (1,0), (0.5, 0.8660254037844386)])
        poly2 = Polygon([(0,0), (0.8660254037844387, 0.5), (0,1)])
        self.assertTrue(gen.intersects_without_touching(poly1, poly2))
    

    # ----------------------------- has overlap ----------------------------- #
    def test_has_overlap_three_triangles_no_overlap(self):
        gen = ShapeGenerator()
        lattice = ShapeHelpers.complex_fish()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(0,0), Point(0, -2), Point(-1,-1),
            Point(1,-1), Point(0,1), Point(1,1)
        ]
        self.assertFalse(gen.has_overlap(scenario, lattice))

    def test_has_overlap_two_triangles_overlap_bowtie1(self):
        gen = ShapeGenerator()
        lattice = ShapeHelpers.bowtie()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(0,0), Point(1,0), Point(0.5,0.8660254037844386),
            Point(0.8660254037844387 ,0.5), Point(0,1)
        ]
        self.assertTrue(gen.has_overlap(scenario, lattice))

    def test_has_overlap_two_triangles_overlap_bowtie2(self):
        gen = ShapeGenerator()
        lattice = ShapeHelpers.bowtie()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(0,0), Point(0,3), Point(3,0),
            Point(1,1), Point(1,-1)
        ]
        self.assertTrue(gen.has_overlap(scenario, lattice))

    def test_has_overlap_two_triangles_overlap_bowtie3(self):
        gen = ShapeGenerator()
        lattice = ShapeHelpers.bowtie()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(0,0), Point(1,0), Point(0.5, 0.8660254037844386),
            Point(0.8660254037844387, 0.5), Point(0,1)
        ]
        self.assertTrue(gen.has_overlap(scenario, lattice))

    def test_has_overlap_glued_vertex_tri_tri_quad_overlap(self):
        gen = ShapeGenerator()
        lattice = ShapeHelpers.complex_fish()
        gen.generate_by_lattice_traversal(lattice)

        scenario = [
            Point(0,0), Point(0.7071067811865476, -0.7071067811865476), Point(-0.0000000000000001, -1.414213562373095),
            Point(-0.7071067811865476, -0.7071067811865476), Point(0.7071067811865476, 0.7071067811865476),
            Point(-0.2588190451025206, 0.9659258262890683), Point(0.5000000000000001, 0.8660254037844386),
            Point(-0.4999999999999998, 0.8660254037844387)
        ]
        self.assertTrue(gen.has_overlap(scenario, lattice))

    
    
    # -------------------- lattice traversal helper ----------------------------- #
    def test_lattice_traversal_helper_base_case(self):
        gen = ShapeGenerator()
        lattice = Lattice(3)
        full_coords = [Point(0,0), Point(1,0), Point(1/2, math.sqrt(3)/2)] # <- an equilateral triangle
        coordinate_figure = []
        sl_index = 0

        gen.lattice_traversal_helper(lattice, full_coords, coordinate_figure, sl_index)

        self.assertEqual(len(coordinate_figure), 1)
        scenario = coordinate_figure[0]
        self.assertEqual(scenario[0], Point(0,0))
        self.assertEqual(scenario[1], Point(1,0))
        self.assertEqual(scenario[2], Point(1/2, math.sqrt(3)/2))

    # def test_lattice_traversal_helper_


    # ------------------- verify scenarios ---------------------------------------- #

    def test_verify_scenarios_types_differ(self):
        gen = ShapeGenerator()
        scenarios = [
            [None,       Point(0,0), Point(0,0)],
            [Point(0,0), None,       Point(0,0)],
        ]
        
        with self.assertRaises(Exception):
            gen.verify_scenarios(scenarios)

    def test_verify_scenarios_types_equal(self):
        gen = ShapeGenerator()
        scenarios = [
            [None, Point(0,0), Point(0,0)],
            [None, Point(0,0), Point(0,0)]
        ]
        
        try:
            gen.verify_scenarios(scenarios)
        except:
            self.fail("verify_scenario raised an exception unexpectedly")

if __name__ == "__main__":
    unittest.main()













































































































































































































































































 # blingus bloongus