import unittest
import networkx as nx
import sys
  
  
# adding Folder_2 to the system path
sys.path.insert(0, './Summer-Research-2022/')

from lattice import Lattice
from node    import Node

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

#! __init__ and therefore private build and therefore private make vertex, edge, and shape layer tests

class TestCreating(unittest.TestCase):

  #negative vertices
  def test_neg_vertices(self):
    #need the lambda or Lattice(-3) runs before the assert and it fails
    self.assertRaises(Exception, lambda: Lattice[:-3])

    #zero vertices
  def test_zero_vertices(self):
    self.assertRaises(Exception, lambda: Lattice[:0])

  #one vertex (a point)
  def test_one_vertices(self):
    self.assertRaises(Exception, lambda: Lattice[:1])

  # positive non-int
  def test_non_integer_vertices_pos(self):
    self.assertRaises(Exception, lambda: Lattice[:0.7])

  # negative non-int
  def test_non_integer_vertices_neg(self):
    self.assertRaises(Exception, lambda: Lattice[:-99.258])

  # + 1 because figure-level node for use when glueing later
  # * 2 because directed edges going both ways
  # + 2 because two edges to get to figure-level node

  # *----*   line segment. nodes should = 5 + 1 = 6, edges should = 5 * 2 + 2 = 12
  def test_two_vertices(self):
    two = Lattice(2)
    self.assertEqual(two.number_of_nodes(), 6)
    self.assertEqual(two.number_of_edges(), 12)
    self.assertEqual([1, 2, 1, 1, 1], two.list_layer_lengths())

    self.assertEqual(2, len(two._bot_node.get_parents()))
    self.assertEqual(0, len(two._bot_node.get_children()))
    self.assertEqual(BOTTOM_LATTICE_LAYER, two._bot_node._lattice_layer)

    for v_node in two._bot_node.get_parents():
      self.assertEqual(1, len(v_node.get_children()))
      self.assertEqual(1, len(v_node.get_parents()))
      self.assertEqual(VERTEX_LATTICE_LAYER, v_node._lattice_layer)
      for e_node in v_node.get_parents():
        self.assertEqual(2, len(e_node.get_children()))
        self.assertEqual(1, len(e_node.get_parents()))
        self.assertEqual(EDGE_LATTICE_LAYER, e_node._lattice_layer)
        for s_node in e_node.get_parents():
          self.assertEqual(1, len(s_node.get_children()))
          self.assertEqual(1, len(s_node.get_parents()))
          self.assertEqual(SHAPE_LATTICE_LAYER, s_node._lattice_layer)

    self.assertEqual(0, len(two._top_node.get_parents()))
    self.assertEqual(1, len(two._top_node.get_children()))
    self.assertEqual(TOP_LATTICE_LAYER, two._top_node._lattice_layer)

  #    *
  #   / \
  #  /   \
  # *-----*    triangle. nodes should = 8 + 1 = 9, edges should = 12 * 2 + 2 = 26
  def test_three_vertices(self):
    tri = Lattice(3)
    self.assertEqual(tri.number_of_nodes(), 9)
    self.assertEqual(tri.number_of_edges(), 26)
    self.assertEqual([1, 3, 3, 1, 1], tri.list_layer_lengths())

    self.assertEqual(3, len(tri._bot_node.get_parents()))
    self.assertEqual(0, len(tri._bot_node.get_children()))
    self.assertEqual(BOTTOM_LATTICE_LAYER, tri._bot_node._lattice_layer)

    for v_node in tri._bot_node.get_parents():
      self.assertEqual(1, len(v_node.get_children()))
      self.assertEqual(2, len(v_node.get_parents()))
      self.assertEqual(VERTEX_LATTICE_LAYER, v_node._lattice_layer)
      for e_node in v_node.get_parents():
        self.assertEqual(2, len(e_node.get_children()))
        self.assertEqual(1, len(e_node.get_parents()))
        self.assertEqual(EDGE_LATTICE_LAYER, e_node._lattice_layer)
        for s_node in e_node.get_parents():
          self.assertEqual(3, len(s_node.get_children()))
          self.assertEqual(1, len(s_node.get_parents()))
          self.assertEqual(SHAPE_LATTICE_LAYER, s_node._lattice_layer)

    self.assertEqual(0, len(tri._top_node.get_parents()))
    self.assertEqual(1, len(tri._top_node.get_children()))
    self.assertEqual(TOP_LATTICE_LAYER, tri._top_node._lattice_layer)

  # *---*
  # |   |
  # |   |
  # *---*    quadrilateral. nodes should = 10 + 1 = 11, edges should = 16 * 2 + 2 = 34
  def test_four_vertices(self):
    quad = Lattice(4)
    self.assertEqual(quad.number_of_nodes(), 11)
    self.assertEqual(quad.number_of_edges(), 34)
    self.assertEqual([1, 4, 4, 1, 1], quad.list_layer_lengths())

    self.assertEqual(4, len(quad._bot_node.get_parents()))
    self.assertEqual(0, len(quad._bot_node.get_children()))
    self.assertEqual(BOTTOM_LATTICE_LAYER, quad._bot_node._lattice_layer)

    for v_node in quad._bot_node.get_parents():
      self.assertEqual(1, len(v_node.get_children()))
      self.assertEqual(2, len(v_node.get_parents()))
      self.assertEqual(VERTEX_LATTICE_LAYER, v_node._lattice_layer)
      for e_node in v_node.get_parents():
        self.assertEqual(2, len(e_node.get_children()))
        self.assertEqual(1, len(e_node.get_parents()))
        self.assertEqual(EDGE_LATTICE_LAYER, e_node._lattice_layer)
        for s_node in e_node.get_parents():
          self.assertEqual(4, len(s_node.get_children()))
          self.assertEqual(1, len(s_node.get_parents()))
          self.assertEqual(SHAPE_LATTICE_LAYER, s_node._lattice_layer)

    self.assertEqual(0, len(quad._top_node.get_parents()))
    self.assertEqual(1, len(quad._top_node.get_children()))
    self.assertEqual(TOP_LATTICE_LAYER, quad._top_node._lattice_layer)

  #    *------*
  #   /        \
  #  *          *
  #   \        /
  #    *------*    hexagon. nodes should = 14 + 1 = 15, edges should = 24 * 2 + 2 = 50
  def test_six_vertices(self):
    hex = Lattice(6)
    self.assertEqual(hex.number_of_nodes(), 15)
    self.assertEqual(hex.number_of_edges(), 50)
    self.assertEqual([1, 6, 6, 1, 1], hex.list_layer_lengths())

    self.assertEqual(6, len(hex._bot_node.get_parents()))
    self.assertEqual(0, len(hex._bot_node.get_children()))
    self.assertEqual(BOTTOM_LATTICE_LAYER, hex._bot_node._lattice_layer)

    for v_node in hex._bot_node.get_parents():
      self.assertEqual(1, len(v_node.get_children()))
      self.assertEqual(2, len(v_node.get_parents()))
      self.assertEqual(VERTEX_LATTICE_LAYER, v_node._lattice_layer)
      for e_node in v_node.get_parents():
        self.assertEqual(2, len(e_node.get_children()))
        self.assertEqual(1, len(e_node.get_parents()))
        self.assertEqual(EDGE_LATTICE_LAYER, e_node._lattice_layer)
        for s_node in e_node.get_parents():
          self.assertEqual(6, len(s_node.get_children()))
          self.assertEqual(1, len(s_node.get_parents()))
          self.assertEqual(SHAPE_LATTICE_LAYER, s_node._lattice_layer)

    self.assertEqual(0, len(hex._top_node.get_parents()))
    self.assertEqual(1, len(hex._top_node.get_children()))
    self.assertEqual(TOP_LATTICE_LAYER, hex._top_node._lattice_layer)

if __name__ == "__main__":
  unittest.main()