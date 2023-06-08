import unittest
import networkx as nx
import sys

  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice import Lattice
from node    import Node

class TestGlueVertex(unittest.TestCase):

  def test_glue_vertex_not_isomorphic(self): # not isomorphic = they're on different layers
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_layer_node = l1._bot_node.get_parents()[0]
    edge_layer_node   = l2._top_node.get_children()[0].get_children()[1]
    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_layer_node, l2, edge_layer_node)

  def test_glue_vertex_both_not_layer_3(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    edge_node_l1 = l1._bot_node.get_parents()[0].get_parents()[0]
    edge_node_l2 = l2._bot_node.get_parents()[0].get_parents()[0]
    # you shouldn't be able to glue two edges using glue_vertex()
    with self.assertRaises(Exception):
      l1.glue_vertex(edge_node_l1, l2, edge_node_l2)

  def test_glue_vertex_diff_layer(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_node_l1 = l1._bot_node.get_parents()[0]
    edge_node_l2 = l2._bot_node.get_parents()[0].get_parents()[0]

    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_node_l1, l2, edge_node_l2)

  def test_glue_vertex_neither_node_from_this_lattice(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    vertex_node2 = vertex_nodes1[1]
    with self.assertRaises(Exception):
      l2.glue_vertex(vertex_node1, vertex_node2)

  # glue two vertices that are on the same lattice (that is on the current lattice)
  def test_glue_vertex_same_lattice_l1(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    vertex_node2 = vertex_nodes1[1]
    # both of these vertices are on l1
    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_node1, l2, vertex_node2)

  # glue two vertices that are on the same lattice (that isn't the l1 lattice)
  def test_glue_vertex_same_lattice_l2(self):
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_nodes_l2 = l2._bot_node.get_parents()
    vertex_node1_l2 = vertex_nodes_l2[0]
    vertex_node2_l2 = vertex_nodes_l2[1]
    # both of these vertices are on l2
    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_node1_l2, l2, vertex_node2_l2)

  def test_glue_vertex_both_non_nodes(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    with self.assertRaises(Exception):
      l1.glue_vertex(3, l2, 0)

  def test_glue_vertex_one_node_one_non_node(self): # should raise exception
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_node = l1._bot_node.get_parents()[0]
    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_node, l2, 0)

  def test_glue_vertex_to_itself(self):
    l1 = Lattice(3)
    l2 = Lattice(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    with self.assertRaises(Exception):
      l1.glue_vertex(vertex_node1, l2, vertex_node1)
      
  #-------------------------------shapes-----------------------------#
  # glue the same shape by the vertex
  # *       *
  # |\     /|
  # | \   / |
  # |  \ /  |
  # |   *   |
  # |  / \  |
  # | /   \ |
  # |/     \|
  # *       *
  def test_glue_vertex_same_shape(self):
    l1 = Lattice(3)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = Lattice(3)
    vertex_node2 = l2._bot_node.get_parents()[0]

    post_glued = l1.glue_vertex(vertex_node1, l2, vertex_node2)
    new_node = post_glued._testing_new_node

    self.assertEqual(post_glued.number_of_nodes(), 15)
    self.assertEqual(post_glued.number_of_edges(), 50)

    self.assertTrue(post_glued._bot_node._exists_in_parents(new_node)) # bottom node has glued vertex as parent
    self.assertTrue(new_node._exists_in_children(post_glued._bot_node))

    self.assertTrue(len(new_node.get_parents()) == 4) # glued vertex has 4 parent connections
    for node in new_node.get_parents():
        self.assertTrue(node._exists_in_children(new_node)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node._exists_in_parents(node))  # is this parent a parent of the vertex1?
    
  # glue different shapes by the vertex
  #   *
  #   |\  *-----*
  #   | \ |     |
  #   |  \|     |
  #   *---*-----*
  def test_glue_vertex_diff_shapes(self):
    l1 = Lattice(3)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = Lattice(4)
    vertex_node2 = l2._bot_node.get_parents()[0]

    post_glued = l1.glue_vertex(vertex_node1, l2, vertex_node2)
    new_node = post_glued._testing_new_node

    self.assertEqual(post_glued.number_of_nodes(), 17)
    self.assertEqual(post_glued.number_of_edges(), 58)

    self.assertTrue(post_glued._bot_node._exists_in_parents(new_node)) # bottom node has glued vertex as parent
    self.assertTrue(new_node._exists_in_children(post_glued._bot_node))

    self.assertTrue(len(new_node.get_parents()) == 4) # glued vertex has 4 parent connections
    for node in new_node.get_parents():
        self.assertTrue(node._exists_in_children(new_node)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node._exists_in_parents(node))  # is this parent a parent of the vertex1?

  # glue two shapes to the same vertex
 #   *
 #   |\  *-----*
 #   | \ |     |
 #   |  \|     |
 #   *---*-----*
 #      /|
 #     / |
 #    /  |
 #   *---*
  def test_glue_vertex_two_to_same_vertex(self):
    l1 = Lattice(4)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = Lattice(3)
    vertex_node2 = l2._bot_node.get_parents()[0]
    l3 = Lattice(3)
    vertex_node3 = l3._bot_node.get_parents()[0]

    post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2)
    new_node = post_glued1._testing_new_node
    post_glued2 = post_glued1.glue_vertex(new_node, l3, vertex_node3)
    new_node = post_glued2._testing_new_node

    self.assertEqual(post_glued2.number_of_nodes(), 23)
    self.assertEqual(post_glued2.number_of_edges(), 82)

    self.assertTrue(post_glued2._bot_node._exists_in_parents(new_node)) # bottom node has glued vertex as parent
    self.assertTrue(new_node._exists_in_children(post_glued2._bot_node))

    self.assertTrue(len(new_node.get_parents()) == 6) # glued vertex has 6 parent connections
    for node in new_node.get_parents():
        self.assertTrue(node._exists_in_children(new_node)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node._exists_in_parents(node))  # is this parent a parent of the vertex1?

  #shape + line segment by vertex
  #
  #       *-----* 
  #       |     |
  #       |     |
  # *-----*-----*
  def test_glue_vertex_line_segment_to_square(self):
    l1 = Lattice(4)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = Lattice(2)
    vertex_node2 = l2._bot_node.get_parents()[0]

    post_glued = l1.glue_vertex(vertex_node1, l2, vertex_node2)
    new_node = post_glued._testing_new_node

    self.assertEqual(post_glued.number_of_nodes(), 14)
    self.assertEqual(post_glued.number_of_edges(), 44)

    self.assertTrue(post_glued._bot_node._exists_in_parents(new_node)) # bottom node has glued vertex as parent
    self.assertTrue(new_node._exists_in_children(post_glued._bot_node))

    self.assertTrue(len(new_node.get_parents()) == 3) # glued vertex has 3 parent connections
    for node in new_node.get_parents():
        self.assertTrue(node._exists_in_children(new_node)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node._exists_in_parents(node))  # is this parent a parent of the vertex1?
    
    #! Illegal !# needs to throw something

#   # glue a line segment connecting two vertices inside the square
#   #       *------*
#   #       |    / |
#   #       |   /  |
#   #       |  /   |
#   #       | /    |   
#   #       *------*
#   def test_glue_vertex_segment_inside(self):
#     square = Lattice(4)
#     segment = Lattice(2)
#     sqrVertex = square._bot_node.get_parents()[0]
#     segVertex = segment._bot_node.get_parents()[0]

  # glue a snake of shapes via vertices
  # .        .____.
  # |\      /|\   |
  # | \    / | \  |
  # |  \  /  |  \ |
  # |___\/___|   \|
  def test_glue_vertex_snake(self):
    l1 = Lattice(3)
    l2 = Lattice(3)
    l3 = Lattice(3)
    vertex_node1 = l1._bot_node.get_parents()[0]
    vertex_node2 = l2._bot_node.get_parents()[0]
    vertex_node3 = l3._bot_node.get_parents()[0]

    post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2) # /_\/_\ two triangle glued lattice
    post_glued1_vertex = post_glued1._bot_node.get_parents()[0]
    if len(post_glued1_vertex.get_parents()) == 4:
      post_glued1_vertex = post_glued1._bot_node.get_parents()[1] # we DON'T want the one with 4 parents

    post_glued2 = post_glued1.glue_vertex(post_glued1_vertex, l3, vertex_node3) # now we have all three
    new_node_1 = post_glued2._testing_old_node # glued node between first 2 triangles
    new_node_2 = post_glued2._testing_new_node # glued node between last 2 triangles

    self.assertEqual(post_glued2.number_of_nodes(), 21)
    self.assertEqual(post_glued2.number_of_edges(), 74)

  # tests for first glued node
    self.assertTrue(post_glued2._bot_node._exists_in_parents(new_node_1)) # bottom node has glued vertex as parent
    self.assertTrue(new_node_1._exists_in_children(post_glued2._bot_node))

    self.assertTrue(len(new_node_1.get_parents()) == 4) # glued vertex has 6 parent connections
    for node in new_node_1.get_parents():
        self.assertTrue(node._exists_in_children(new_node_1)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node_1._exists_in_parents(node))  # is this parent a parent of the vertex1?

  # tests for second glued node
    self.assertTrue(post_glued2._bot_node._exists_in_parents(new_node_2)) # bottom node has glued vertex as parent
    self.assertTrue(new_node_2._exists_in_children(post_glued2._bot_node))

    self.assertTrue(len(new_node_2.get_parents()) == 4) # glued vertex has 6 parent connections
    for node in new_node_2.get_parents():
        self.assertTrue(node._exists_in_children(new_node_2)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node_2._exists_in_parents(node))  # is this parent a parent of the vertex1?
  

# flower shape by vertex
#   |\    /|
#   | \  / |
#   |__\/__|
#      /\
#     /  \
#    /____\


def test_glue_vertex_flower(self):
    l1 = Lattice(3)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = Lattice(3)
    vertex_node2 = l2._bot_node.get_parents()[0]
    l3 = Lattice(3)
    vertex_node3 = l3._bot_node.get_parents()[0]

    post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2)
    new_node = post_glued1._testing_new_node
    post_glued2 = post_glued1.glue_vertex(new_node, l3, vertex_node3)

    self.assertEqual(post_glued2.number_of_nodes(), 21)
    self.assertEqual(post_glued2.number_of_edges(), 74)

    self.assertTrue(post_glued2._bot_node._exists_in_parents(new_node)) # bottom node has glued vertex as parent
    self.assertTrue(new_node._exists_in_children(post_glued2._bot_node))

    self.assertTrue(len(new_node.get_parents()) == 4) # glued vertex has 4 parent connections
    for node in new_node.get_parents():
        self.assertTrue(node._exists_in_children(new_node)) # is vertex1 the child of this parent node?
        self.assertTrue(new_node._exists_in_parents(node))  # is this parent a parent of the vertex1?

if __name__ == "__main__":
    unittest.main()