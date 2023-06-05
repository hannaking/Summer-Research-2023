import unittest
import sys
import math

from shapely.geometry import *

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

DEFAULT_SIDE_LENGTH = 1

class TestShapely(unittest.TestCase):
    def test_touches_triangle_overlap(self):
        tri1 = LinearRing([(0,0), (1,0), (0,1)])
        tri2 = LinearRing([(0,0), (1,0), (1,1)])
        self.assertFalse(tri1.touches(tri2))

    def test_touches_bowtie(self):
        tri1 = Polygon([(0,0), (1,0), (1,1)])
        tri2 = Polygon([(0,0), (-1,0), (-1,1)])
        self.assertTrue(tri1.touches(tri2))

    def test_touches_triangles_edge_glue(self):
        tri1 = Polygon([(0,0), (-1,0), (0,1)])
        tri2 = Polygon([(0,0), (1,0), (0,1)])
        self.assertTrue(tri1.touches(tri2))

    def test_touches_triangles_same(self):
        tri1 = Polygon([(0,0), (1,0), (0,1)])
        tri2 = Polygon([(0,0), (1,0), (0,1)])
        self.assertFalse(tri1.touches(tri2))

    def test_touches_triangles_overlap_but_same_point(self):
        tri1 = Polygon([(0,0), (1,0), (1,1)])
        tri2 = Polygon([(0,0), (2,0), (2,1)])
        self.assertFalse(tri1.touches(tri2))

    def test_intersects_and_touches_overlap(self):
        rect = Polygon([(0,0), (2,0), (2,4), (0,4)])
        print(hex(id(rect)))
        tri = Polygon([(1,2), (3,1), (3,4)])
        print(hex(id(tri)))
        self.assertTrue(rect.intersects(tri) and not rect.touches(tri))

    def test_intersects_and_touches_just_touches(self):
        rect = Polygon([(0,0), (2,0), (2,4), (0,4)])
        tri = Polygon([(2,2), (3,1), (3,4)])
        self.assertFalse(rect.intersects(tri) and not rect.touches(tri))

    def test_intersects_and_touches_inside_by_vertex(self):
        rect = Polygon([(0,0), (2,0), (2,4), (0,4)])
        tri = Polygon([(0,0), (1,0), (0,1)])
        self.assertTrue(rect.intersects(tri) and not rect.touches(tri))

if __name__ == "__main__":
    unittest.main()