import unittest
import sys
import networkx as nx

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from face_graph_generator import FaceGraphGenerator
from lattice import Lattice
from unit_tests.shape_helpers import *

class TestFaceGraphGenerator(unittest.TestCase):
    # single shape lattice for 1, 4, 8
    # edge glue
    # vertex glue
    # fill gap
    # anything larger, probably a few
    def test_build_single_segment(self):
        segment = Lattice(2)
        gen = FaceGraphGenerator(segment)
        
        # face graphs are concerned with edges, not vertices like lattice is. 
        # size is 1 instead of 2
        graph = gen.build(segment, [1], ["Segment"])

        self.assertEqual(len(graph.nodes), 1)
        self.assertTrue(graph.has_node(0))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 1})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Segment"})
        self.assertEqual(len(graph.edges), 0)
    
    def test_build_single_quadrilateral(self):
        quad = Lattice(4)
        gen = FaceGraphGenerator(quad)
        
        graph = gen.build(quad, [4], ["Square"])

        self.assertEqual(len(graph.nodes), 1)
        self.assertTrue(graph.has_node(0))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Square"})
        self.assertEqual(len(graph.edges), 0)

    def test_build_single_octagon(self):
        oct = Lattice(8)
        gen = FaceGraphGenerator(oct)
        
        graph = gen.build(oct, [8], ["RegularOct"])

        self.assertEqual(len(graph.nodes), 1)
        self.assertTrue(graph.has_node(0))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 8})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "RegularOct"})
        self.assertEqual(len(graph.edges), 0)

    def test_build_edge_glue(self):
        fig = ShapeHelpers.glued_edge_quad_tri()
        gen = FaceGraphGenerator(fig)
        
        graph = gen.build(fig, [3, 4], ("Equilateral", "Square"))

        self.assertEqual(len(graph.nodes), 2)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral", 1: "Square"})
        self.assertEqual(len(graph.edges), 1)

    def test_build_vertex_glue(self):
        fig = ShapeHelpers.glued_vertex_segment_quad()
        gen = FaceGraphGenerator(fig)
        
        graph = gen.build(fig, [1, 4], ("Segment", "Dart"))

        self.assertEqual(len(graph.nodes), 2)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 1, 1: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Segment", 1: "Dart"})
        self.assertEqual(len(graph.edges), 0)

    def test_build_fill_gap(self):
        fig = ShapeHelpers.filled_quad()
        gen = FaceGraphGenerator(fig)

        graph = gen.build(fig, [3, 4], ("Equilateral", "Dart"))

        self.assertEqual(len(graph.nodes), 2)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral", 1: "Dart"})
        self.assertEqual(len(graph.edges), 2)

    # multiple edge gluings to one face
    def test_build_tri_with_quad_on_each_edge(self):
        fig = ShapeHelpers.tri_with_quad_on_each_edge()
        gen = FaceGraphGenerator(fig)

        graph = gen.build(fig, [3, 4, 4, 4], ("Equilateral", "Parallelogram", "IsoscelesTrapezoid", "Square"))

        self.assertEqual(len(graph.nodes), 4)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(2))
        self.assertTrue(graph.has_node(3))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 4, 2: 4, 3: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral",
                                                                 1: "Parallelogram",
                                                                 2: "IsoscelesTrapezoid",
                                                                 3: "Square"})
        self.assertEqual(len(graph.edges), 3)
        self.assertEqual(graph.degree(0), 3)
        self.assertEqual(graph.degree(1), 1)
        self.assertEqual(graph.degree(2), 1)
        self.assertEqual(graph.degree(3), 1)
        self.assertEqual(list(graph.edges.data()), [(0, 1, {}),
                                                    (0, 2, {}),
                                                    (0, 3, {})])
        
    # vertex glue and edge glue
    def test_build_complex_fish(self):
        fig = ShapeHelpers.complex_fish()
        gen = FaceGraphGenerator(fig)

        graph = gen.build(fig, [3, 3, 3], ("Equilateral", "Right", "Isosceles"))

        self.assertEqual(len(graph.nodes), 3)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(2))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 3, 2: 3})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral",
                                                                 1: "Right",
                                                                 2: "Isosceles"})
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.degree(0), 1)
        self.assertEqual(list(graph.edges.data()), [(0, 1, {})])

    # edge gluings to different faces, and a fill gap to two different faces
    def test_build_goofy_shape(self):
        fig = ShapeHelpers.goofy_shape()
        gen = FaceGraphGenerator(fig)

        graph = gen.build(fig, [3, 4, 5, 4], ("Equilateral", "Square", "RegularPent", "Dart"))

        self.assertEqual(len(graph.nodes), 4)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(2))
        self.assertTrue(graph.has_node(3))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 4, 2: 5, 3: 4})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral",
                                                                 1: "Square",
                                                                 2: "RegularPent",
                                                                 3: "Dart"})
        self.assertEqual(len(graph.edges), 4)
        self.assertEqual(graph.degree(0), 2)
        self.assertEqual(graph.degree(1), 3)
        self.assertEqual(graph.degree(2), 1)
        self.assertEqual(graph.degree(3), 2)
        self.assertEqual(list(graph.edges.data()), [(0, 1, {}),
                                                    (0, 3, {}),
                                                    (1, 3, {}),
                                                    (1, 2, {})])
                                                    # out of order because of the fill gap
                                                    # edges added based on left to right lattice

    # multiple vertex gluings
    def test_build_glue_one_vertex_tri_tri_tri(self):
        fig = ShapeHelpers.glue_one_vertex_tri_tri_tri()
        gen = FaceGraphGenerator(fig)

        graph = gen.build(fig, [3, 3, 3], ("Equilateral", "Right", "Isosceles"))

        self.assertEqual(len(graph.nodes), 3)
        self.assertTrue(graph.has_node(0))
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(2))
        self.assertEqual(nx.get_node_attributes(graph, "size"), {0: 3, 1: 3, 2: 3})
        self.assertEqual(nx.get_node_attributes(graph, "type"), {0: "Equilateral",
                                                                 1: "Right",
                                                                 2: "Isosceles"})
        self.assertEqual(len(graph.edges), 0)

    # testing for number of graphs generated (constructor)
    # single shape 1 (1), 3 (4), 4 (8), 5 (1), 6 (1), 7 (1), 8 (1)
    # tri with quad on each edge             expected: 2048
    # complex fish                           expected: 64
    # goofy shape                            expected: 256
    # three triangles glued at one vertex    expected: 64
    def test_single_segment(self):
        fig = Lattice(2)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 1)

    def test_single_tri(self):
        fig = Lattice(3)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 4)

    def test_single_quad(self):
        fig = Lattice(4)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 8)

    def test_single_pent(self):
        fig = Lattice(5)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 1)

    def test_single_hex(self):
        fig = Lattice(6)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 1)

    def test_single_hept(self):
        fig = Lattice(7)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 1)

    def test_single_oct(self):
        fig = Lattice(8)
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 1)

    def test_tri_with_quad_on_each_edge(self):
        fig = ShapeHelpers.tri_with_quad_on_each_edge()
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 2048)

    def test_complex_fish(self):
        fig = ShapeHelpers.complex_fish()
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 64)

    def test_goofy_shape(self):
        fig = ShapeHelpers.goofy_shape()
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 256)

    def test_glue_one_vertex_tri_tri_tri(self):
        fig = ShapeHelpers.glue_one_vertex_tri_tri_tri()
        gen = FaceGraphGenerator(fig)

        self.assertEqual(len(gen.graphs), 64)

if __name__ == '__main__':
    unittest.main()