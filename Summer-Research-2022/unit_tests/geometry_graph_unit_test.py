import unittest
import networkx as nx
import sys
  
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice import *
from lattice_test import*
from node    import Node

class TestGeometryGraph(unittest.TestCase):
    def test_build_graph_triangle(self):
        tri = Lattice(3)
       
        self.assertEqual(3, tri._geo_graph.number_of_nodes())
        self.assertEqual(3, tri._geo_graph.number_of_edges())

        tri._geo_graph.show()

    def test_build_graph_square(self):
        square = Lattice(4)
       
        self.assertEqual(4, square._geo_graph.number_of_nodes())
        self.assertEqual(4, square._geo_graph.number_of_edges())

        square._geo_graph.show()

    def test_build_graph_butterfly(self):
        l1 = Lattice(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = Lattice(3)
        vertex_node2 = l2._bot_node.get_parents()[0]

        shape = l1.glue_vertex(vertex_node1, l2, vertex_node2)

        self.assertEqual(5, shape._geo_graph.number_of_nodes())
        self.assertEqual(6, shape._geo_graph.number_of_edges())

        shape._geo_graph.show()

    def test_build_graph_square_snake(self):
        l1 = LatticeTest(4)
        vertex_node1 = l1._bot_node.get_parents()[0]
        edge_node1 = vertex_node1.get_parents()[0]

        l2 = LatticeTest(4)
        vertex_node2 = l2._bot_node.get_parents()[0]
        edge_node2 = vertex_node2.get_parents()[0]
        
        post_glued = l1.glue_edge(edge_node1, l2, edge_node2)
        new_edge = post_glued._testing_node_2
        l3 = LatticeTest(4)
        vertex_node3 = l3._bot_node.get_parents()[0]
        edge_node3 = vertex_node3.get_parents()[0]

        # this makes sure we are not going to glue on the same edge that has been glued
        if post_glued._top_node.get_children()[0].get_children()[0] is not new_edge:
            next_edge_to_glue = post_glued._top_node.get_children()[0].get_children()[0]
        else:
            next_edge_to_glue = post_glued._top_node.get_children()[0].get_children()[1]

        shape = post_glued.glue_edge(next_edge_to_glue, l3, edge_node3)

        self.assertEqual(8, shape._geo_graph.number_of_nodes())
        self.assertEqual(10, shape._geo_graph.number_of_edges())

        shape._geo_graph.show()

    def test_build_graph_triangle_square_glued_by_vertex(self):
        l1 = Lattice(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = Lattice(4)
        vertex_node2 = l2._bot_node.get_parents()[0]

        shape = l1.glue_vertex(vertex_node1, l2, vertex_node2)

        self.assertEqual(6, shape._geo_graph.number_of_nodes())
        self.assertEqual(7, shape._geo_graph.number_of_edges())

        shape._geo_graph.show()

    def test_build_graph_square_and_line_segment(self):
        l1 = Lattice(4)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = Lattice(2)
        vertex_node2 = l2._bot_node.get_parents()[0]

        shape = l1.glue_vertex(vertex_node1, l2, vertex_node2)

        self.assertEqual(5, shape._geo_graph.number_of_nodes())
        self.assertEqual(5, shape._geo_graph.number_of_edges())

        shape._geo_graph.show()

    #------------------------------------------- build perimeter -------------------------------------------
    def test_get_perimeter_triangle(self):
        tri = Lattice(3)
        per = tri._geo_graph.get_perimeter()
       
        self.assertEqual(3, per.number_of_nodes())
        self.assertEqual(3, per.number_of_edges())

        # nx.draw_planar(per, with_labels=True)
        # plt.show()

    def test_get_perimeter_square(self):
        square = Lattice(4)
        per = square._geo_graph.get_perimeter()
       
        self.assertEqual(4, per.number_of_nodes())
        self.assertEqual(4, per.number_of_edges())

        # nx.draw_planar(per, with_labels=True)
        # plt.show()

    def test_get_perimeter_butterfly(self):
        l1 = Lattice(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = Lattice(3)
        vertex_node2 = l2._bot_node.get_parents()[0]

        shape = l1.glue_vertex(vertex_node1, l2, vertex_node2)
        per = shape._geo_graph.get_perimeter()

        self.assertEqual(5, per.number_of_nodes())
        self.assertEqual(6, per.number_of_edges())

        # nx.draw_planar(per, with_labels=True)
        # plt.show()

    def test_get_perimeter_square_snake(self):
        l1 = LatticeTest(4)
        vertex_node1 = l1._bot_node.get_parents()[0]
        edge_node1 = vertex_node1.get_parents()[0]

        l2 = LatticeTest(4)
        vertex_node2 = l2._bot_node.get_parents()[0]
        edge_node2 = vertex_node2.get_parents()[0]
        
        post_glued = l1.glue_edge(edge_node1, l2, edge_node2)
        new_edge = post_glued._testing_node_2
        l3 = LatticeTest(4)
        vertex_node3 = l3._bot_node.get_parents()[0]
        edge_node3 = vertex_node3.get_parents()[0]

        # this makes sure we are not going to glue on the same edge that has been glued
        if post_glued._top_node.get_children()[0].get_children()[0] is not new_edge:
            next_edge_to_glue = post_glued._top_node.get_children()[0].get_children()[0]
        else:
            next_edge_to_glue = post_glued._top_node.get_children()[0].get_children()[1]

        shape = post_glued.glue_edge(next_edge_to_glue, l3, edge_node3)
        per = shape._geo_graph.get_perimeter()

        self.assertEqual(8, per.number_of_nodes())
        self.assertEqual(8, per.number_of_edges())

        # nx.draw_planar(per, with_labels=True)
        # plt.show()

    def test_get_perimeter_surrounded(self):
        l1 = LatticeTest(4)


if __name__ == "__main__":
    unittest.main()
