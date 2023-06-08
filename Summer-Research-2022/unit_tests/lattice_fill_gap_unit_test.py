import unittest
import networkx as nx
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice      import *
from lattice_test import LatticeTest
from node         import Node
from polygon_vertex_incidence_matrix import PolygonVertexIncidenceMatrix

class TestFillGap(unittest.TestCase):

  def test_fill_gap_nodeu_not_node(self):
    l1 = LatticeTest(4)
    v1 = "not a node"
    l2 = LatticeTest(3)
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l2, v2)

  def test_fill_gap_nodev_not_node(self):
    l1 = LatticeTest(4)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    l2 = LatticeTest(3)
    v2 = "not a node"
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l2, v2)

  def test_fill_gap_nodeu_not_in_self(self):
    l1 = LatticeTest(4)
    l2 = LatticeTest(3)
    v1 = l2._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l2, v2)

  def test_fill_gap_nodev_not_in_self(self):
    l1 = LatticeTest(4)
    l2 = LatticeTest(3)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l2._nodes_list[VERTEX_LATTICE_LAYER][1]
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l2, v2)

  def test_fill_gap_fill_with_self(self):
    l1 = LatticeTest(4)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l1, v2)

  def test_fill_gap_with_non_simple_shape(self):
    l1 = LatticeTest(4)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][2]

    t1 = LatticeTest(3)
    t2 = LatticeTest(3)
    vertex_node1 = t1._bot_node.get_parents()[0]
    vertex_node2 = t2._bot_node.get_parents()[0]
    bowtie = t1.glue_vertex(vertex_node1, t2, vertex_node2)

    with self.assertRaises(Exception):
      l1.fill_gap(v1, bowtie, v2)

  def test_fill_gap_with_same_node(self):
    l1 = LatticeTest(4)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    with self.assertRaises(Exception):
      l1.fill_gap(v1, l1, v1)

  def test_fill_gap_nodeu_not_exterior(self):
    l1 = LatticeTest(3)
    l2 = LatticeTest(3)
    l3 = LatticeTest(3)
    l4 = LatticeTest(3)
    l5 = LatticeTest(3)
    l6 = LatticeTest(3) # last one is the filling shape!

    # glue the first two shapes
    e1 = l1._bot_node.get_parents()[0].get_parents()[0]
    e2 = l2._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = l1.glue_edge(e1, l2, e2)

    # glue the third shape
    e3 = l3._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E1"), l3, e3)

    # # glue the fourth shape
    e4 = l4._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E00"), l4, e4)
    
    # # glue the fifth shape
    e5 = l5._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("6E1"), l5, e5)

    # # glue the sixth shape (filling shape)
    v1 = glued_edges.get_node_from_label("4V100")
    v2 = glued_edges.get_node_from_label("4V1")
    filled_lattice = glued_edges.fill_gap(v1, l6, v2)

    lattice = Lattice(3)
    interior_node = filled_lattice.get_node_from_label("2V00000") #this is the node in the middle of the pizza. illegal to fill with this node!
    normal_node = filled_lattice._bot_node.get_parents()[0] if not interior_node else filled_lattice._bot_node.get_parents()[1]

    with self.assertRaises(Exception):
      filled_lattice.fill_gap(normal_node, lattice, interior_node)

  def test_fill_gap_one_segment_2_triangles(self):
    l1 = LatticeTest(3)
    l2 = LatticeTest(3)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
    post_glued = l1.fill_gap(v1, l2, v2)

    new_node = post_glued._testing_node_2

  # number of nodes and edges
    self.assertEqual(post_glued.number_of_nodes(), 13)
    self.assertEqual(post_glued.number_of_edges(), 44)

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued.list_layer_lengths(), [1, 4, 5, 2, 1])

    # check proper number of ties up and down from bottom node
    self.assertEqual(4, len(post_glued._bot_node.get_parents()))
    self.assertEqual(0, len(post_glued._bot_node.get_children()))

    # for each vertex node in post_glued...
    for v_node in post_glued._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children()))

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued._bot_node.get_parents())
      self.assertTrue(post_glued._bot_node in v_node.get_children())

    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(new_node.get_children()))
    self.assertEqual(2, len(new_node.get_parents()))

    # for each vertex level node in new node's children...
    for v_node_on_new in new_node.get_children():
      # check proper number of ties up to edge level
      self.assertEqual(3, len(v_node_on_new.get_parents()))
      # check tied up to new_node
      self.assertTrue(new_node in v_node_on_new.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(2, len(post_glued._top_node.get_children()))
    self.assertEqual(0, len(post_glued._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for s_node in new_node.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued._top_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertEqual(3, len(s_node.get_children()))

      # check new tied edge node in shape node's children
      self.assertTrue(new_node in s_node.get_children())

  # fill gap with one segment. square and triangle.
  def test_fill_gap_one_segment_square_triangle(self):
    l1 = LatticeTest(4)
    l2 = LatticeTest(3)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
    post_glued = l1.fill_gap(v1, l2, v2)
    new_node = post_glued._testing_node_2

  # number of nodes and edges
    self.assertEqual(post_glued.number_of_nodes(), 15)
    self.assertEqual(post_glued.number_of_edges(), 52)

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued.list_layer_lengths(), [1, 5, 6, 2, 1]) #@

    # check proper number of ties up and down from bottom node
    self.assertEqual(5, len(post_glued._bot_node.get_parents()))
    self.assertEqual(0, len(post_glued._bot_node.get_children()))

    # for each vertex node in post_glued...
    for v_node in post_glued._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children()))

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued._bot_node.get_parents())
      self.assertTrue(post_glued._bot_node in v_node.get_children())

    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(new_node.get_children()))
    self.assertEqual(2, len(new_node.get_parents()))

    # for each vertex level node in new node's children...
    for v_node_on_new in new_node.get_children():
      # check proper number of ties up to edge level
      self.assertEqual(3, len(v_node_on_new.get_parents()))
      # check tied up to new_node
      self.assertTrue(new_node in v_node_on_new.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(2, len(post_glued._top_node.get_children()))
    self.assertEqual(0, len(post_glued._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for s_node in new_node.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued._top_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertTrue(len(s_node.get_children()) == 3 or len(s_node.get_children()) == 4)

      # check new tied edge node in shape node's children
      self.assertTrue(new_node in s_node.get_children())

    # post_glued.show()
    # post_glued._geo_graph.show()

  def test_fill_gap_one_segment_2v_5v_square(self):
    l1 = LatticeTest(4)
    l2 = LatticeTest(3)
    v1 = l1.get_node_from_label("2V")
    v2 = l1.get_node_from_label("5V")
    print("NEXT ONE IS THE ONE WE WANT")
    shape = l1.fill_gap(v1, l2, v2)

    # shape.show()
    # shape._geo_graph.show()

  # fill between vertices opposite each other on a square
  # makes an indent thing
  #  _______       ______
  # |       |     |\     | # (pretend the shape on the top is a triangle bc we dont know how to draw it here lmaooooo)
  # |       | ->  | \___ | # (also pretend the bottom shape has 4 sides instead of 5)
  # |_______|     |______| # this is participatory art, you as the viewer complete the piece
  #
  def test_fill_gap_square(self):
    l1 = LatticeTest(4)
    v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
    v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
    if l1.is_connected(v1, v2):
        v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][2]

    tri = LatticeTest(3) 

    filled_lattice = l1.fill_gap(v1, tri, v2)
    glued_edges = filled_lattice._testing_glued_edges

    #* --------- ASSERTION TIME!!!!! ---------*#

    # check the number of nodes and edges in the lattice
    self.assertEqual(filled_lattice.number_of_nodes(), 13) #@
    self.assertEqual(filled_lattice.number_of_edges(), 46) #@
    self.assertEqual(filled_lattice.list_layer_lengths(), [1, 4, 5, 2, 1]) #@

    top = filled_lattice._top_node
    bot = filled_lattice._bot_node

    self.assertTrue(len(bot.get_parents()) == 4) #@ how many vertices you should have
    self.assertTrue(len(bot.get_children()) == 0)
    self.assertTrue(len(top.get_parents()) == 0)
    self.assertTrue(len(top.get_children()) == 2) #@ how many shapes you have
    # check that each shape is connected to top node
    for shape in filled_lattice._nodes_list[SHAPE_LATTICE_LAYER]:
      self.assertTrue(len(shape.get_parents()) == 1)
      self.assertTrue(shape in top.get_children())
      self.assertTrue(top in shape.get_parents())

      # check that each glued edge has connections to this shape
      #? note: this only works in this case where the edges are connected to all shapes in the lattice
      #? (because there are only two shapes)
      for glued_edge in glued_edges:
        self.assertTrue(shape in glued_edge.get_parents())
        self.assertTrue(glued_edge in shape.get_children())

    # check that the children of the glued edges have the edge as their parents
    for glued_edge in glued_edges:
      # check that the edge has the correct number of parents and children
      self.assertTrue(len(glued_edge.get_parents()) == 2) #@ can only connect to 2 shapes max in this shape!
      self.assertTrue(len(glued_edge.get_children()) == 2) # can only have 2 children safe to assume for all

      parent_lengths = [] #@ change or remove in other tests if needed
      for child in glued_edge.get_children():

        #@ check that one of the children has 3 connections and the other has 2 connections
        if len(child.get_parents()) == 3 or len(child.get_parents()) == 2:    #@ this part of the code is unique for this test case
          parent_lengths.append(len(child.get_parents()))                 #@ change or remove it in other tests
        self.assertTrue(glued_edge in child.get_parents())                #@

      self.assertEqual(set([3,2]), set(parent_lengths))                   #@ 


    # now to check bottom node connections
    for vertex in filled_lattice._nodes_list[VERTEX_LATTICE_LAYER]:
      # check that all vertices have the correct number of parents and children
      self.assertTrue(len(vertex.get_children()) == 1) # can only have one child (bottom node)
      # check that the bottom is connected to the vertices in both ways
      self.assertTrue(vertex in bot.get_parents())
      self.assertTrue(bot in vertex.get_children())

  # test gluing a triangle between two triangles in a bowtie shape
  # *       *
  # |\     /|
  # | \   / |
  # |  \ /  |
  # |   X   |
  # |  / \  |
  # | /   \ |
  # |/     \|
  # *-------*
  def test_glue_edge_between_two_shapes(self):  
    l1 = LatticeTest(3)
    vertex_node1 = l1._bot_node.get_parents()[0]
    l2 = LatticeTest(3)
    vertex_node2 = l2._bot_node.get_parents()[0]

    bowtie = l1.glue_vertex(vertex_node1, l2, vertex_node2)

    tri = LatticeTest(3)
    
    n1 = None
    n2 = None
    #just finding the nodes we want to glue. i showed the geo graph to find the labels in the first place.
    for i in bowtie._nodes_list[VERTEX_LATTICE_LAYER]:
      if i._label == "3V0":
        n1 = i
      if i._label == "3V1":
        n2 = i

    #bowtie._geo_graph.show()

    filled_lattice = bowtie.fill_gap(n1, tri, n2)
    glued_edges = filled_lattice._testing_glued_edges

    #* --------- ASSERTION TIME!!!!! ---------*#

    # check the number of nodes and edges in the lattice
    self.assertEqual(filled_lattice.number_of_nodes(), 17) #@
    self.assertEqual(filled_lattice.number_of_edges(), 62) #@
    self.assertEqual(filled_lattice.list_layer_lengths(), [1, 5, 7, 3, 1]) #@

    top = filled_lattice._top_node
    bot = filled_lattice._bot_node

    self.assertTrue(len(bot.get_parents()) == 5) #@ how many vertices you should have
    self.assertTrue(len(bot.get_children()) == 0)
    self.assertTrue(len(top.get_parents()) == 0)
    self.assertTrue(len(top.get_children()) == 3) #@ how many shapes you have
    # check shape node connections
    for shape in filled_lattice._nodes_list[SHAPE_LATTICE_LAYER]:
      # check connections between shape and top nodes
      self.assertTrue(len(shape.get_parents()) == 1)
      self.assertTrue(shape in top.get_children())
      self.assertTrue(top in shape.get_parents())

      # check that each shape has at least one of the two glue edges
      found = False
      children = shape.get_children()
      for child in children:
        if child in glued_edges:
            self.assertTrue(shape in child.get_parents())
            found = True
      # found means that the shape has at least one glued edge
      self.assertTrue(found)

    # now, to check for glued edge connections
    for glued_edge in glued_edges:
      # check that the edge has the correct number of parents and children
      self.assertTrue(len(glued_edge.get_parents()) == 2) #@ can only connect to 2 shapes max in this shape!
      self.assertTrue(len(glued_edge.get_children()) == 2) # can only have 2 children safe to assume for all

      parent_lengths = [] #@ change or remove in other tests if needed
      for child in glued_edge.get_children():

        #@ check that one of the children has 4 connections and the other has 3 connections
        if len(child.get_parents()) == 4 or len(child.get_parents()) == 3:#@ this part of the code is unique for this test case
          parent_lengths.append(len(child.get_parents()))                 #@ change or remove it in other tests         
        self.assertTrue(glued_edge in child.get_parents())                #@          

      self.assertEqual(set([4,3]), set(parent_lengths))                   #@ 

    # now to check bottom node connections
    for vertex in filled_lattice._nodes_list[VERTEX_LATTICE_LAYER]:
      # check that all vertices have the correct number of parents and children
      self.assertTrue(len(vertex.get_children()) == 1) # can only have one child (bottom node)
      # check that the bottom is connected to the vertices in both ways
      self.assertTrue(vertex in bot.get_parents())
      self.assertTrue(bot in vertex.get_children())

# glue a rectangle between three other rectangles
# __________________
#|\_______________/|
#| |             | |
#| |             | |
#|_|_____________|_|
  def test_fill_gap_between_three_shapes(self):
    l1 = LatticeTest(4)
    e1 = l1._bot_node.get_parents()[0].get_parents()[0]

    l2 = LatticeTest(4)
    e2 = l2._bot_node.get_parents()[0].get_parents()[0]
    
    two_squares = l1.glue_edge(e1, l2, e2)

    l3 = LatticeTest(4)
    e3 = l3._bot_node.get_parents()[0].get_parents()[0]
    next_edge_to_glue = two_squares.get_node_from_label("8E0")

    three_squares = two_squares.glue_edge(next_edge_to_glue, l3, e3)

    l4 = LatticeTest(4)
    start_vertex = three_squares.get_node_from_label("5V10")
    end_vertex = three_squares.get_node_from_label("4V1")


    print("THIS ONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    filled_lattice = three_squares.fill_gap(start_vertex, l4, end_vertex)
    glued_edges = filled_lattice._testing_glued_edges
    

    #* --------- ASSERTION TIME!!!!! ---------*#

    # check the number of nodes and edges in the lattice
    self.assertEqual(filled_lattice.number_of_nodes(), 25) #@
    self.assertEqual(filled_lattice.number_of_edges(), 100) #@
    self.assertEqual(filled_lattice.list_layer_lengths(), [1, 8, 11, 4, 1]) #@

    top = filled_lattice._top_node
    bot = filled_lattice._bot_node

    self.assertTrue(len(bot.get_parents()) == 8) #@ how many vertices you should have
    self.assertTrue(len(bot.get_children()) == 0)
    self.assertTrue(len(top.get_parents()) == 0)
    self.assertTrue(len(top.get_children()) == 4) #@ how many shapes you have
    # check shape node connections
    for shape in filled_lattice._nodes_list[SHAPE_LATTICE_LAYER]:
      # check connections between shape and top nodes
      self.assertTrue(len(shape.get_parents()) == 1)
      self.assertTrue(shape in top.get_children())
      self.assertTrue(top in shape.get_parents())

      # check that each shape has at least one of the two glue edges
      found = False
      children = shape.get_children()
      for child in children:
        if child in glued_edges:
            self.assertTrue(shape in child.get_parents())
            found = True
      # found means that the shape has at least one glued edge
      self.assertTrue(found)

    # now, to check for glued edge connections
    for glued_edge in glued_edges:
      # check that the edge has the correct number of parents and children
      self.assertTrue(len(glued_edge.get_parents()) == 2) #@ can only connect to 2 shapes max in this shape!
      self.assertTrue(len(glued_edge.get_children()) == 2) # can only have 2 children safe to assume for all

      parent_lengths = [] #@ change or remove in other tests if needed
      for child in glued_edge.get_children():

        #@ check that both of the children has 3 connections (bc every glued edge should be connected to vertices both with degree 3)
        if len(child.get_parents()) == 3:#@ this part of the code is unique for this test case
          parent_lengths.append(len(child.get_parents()))                 #@ change or remove it in other tests         
        self.assertTrue(glued_edge in child.get_parents())                #@          

      self.assertEqual(set([3,3]), set(parent_lengths))                   #@ 

    # now to check bottom node connections
    for vertex in filled_lattice._nodes_list[VERTEX_LATTICE_LAYER]:
      # check that all vertices have the correct number of parents and children
      self.assertTrue(len(vertex.get_children()) == 1) # can only have one child (bottom node)
      # check that the bottom is connected to the vertices in both ways
      self.assertTrue(vertex in bot.get_parents())
      self.assertTrue(bot in vertex.get_children())


#   # closed shape glueing edges                                         
#   #     *-------*
#   #    / \     / \
#   #   /   \   /   \
#   #  /     \ /     \
#   # *-------*-------*
#   #  \     / \     /
#   #   \   /   \   /
#   #    \ /     \ /
#   #     *-------*
  def test_glue_edge_closed_pizza(self):
    l1 = LatticeTest(3)
    l2 = LatticeTest(3)
    l3 = LatticeTest(3)
    l4 = LatticeTest(3)
    l5 = LatticeTest(3)
    l6 = LatticeTest(3) # last one is the filling shape!

    # glue the first two shapes
    e1 = l1._bot_node.get_parents()[0].get_parents()[0]
    e2 = l2._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = l1.glue_edge(e1, l2, e2)

    # glue the third shape
    e3 = l3._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E1"), l3, e3)

    # # glue the fourth shape
    e4 = l4._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E00"), l4, e4)
    
    # # glue the fifth shape
    e5 = l5._bot_node.get_parents()[0].get_parents()[0]
    glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("6E1"), l5, e5)

    # # glue the sixth shape (filling shape)
    v1 = glued_edges.get_node_from_label("4V100")
    v2 = glued_edges.get_node_from_label("4V1")
    filled_lattice = glued_edges.fill_gap(v1, l6, v2)
    glued_edges = filled_lattice._testing_glued_edges

    #filled_lattice._geo_graph.show()
    #filled_lattice.show()

    #* --------- ASSERTION TIME!!!!! ---------*#

    # check the number of nodes and edges in the lattice
    self.assertEqual(filled_lattice.number_of_nodes(), 27) #@
    self.assertEqual(filled_lattice.number_of_edges(), 110) #@
    self.assertEqual(filled_lattice.list_layer_lengths(), [1, 7, 12, 6, 1]) #@

    top = filled_lattice._top_node
    bot = filled_lattice._bot_node

    self.assertTrue(len(bot.get_parents()) == 7) #@ how many vertices you should have
    self.assertTrue(len(bot.get_children()) == 0)
    self.assertTrue(len(top.get_parents()) == 0)
    self.assertTrue(len(top.get_children()) == 6) #@ how many shapes you have
    # check shape node connections

    for shape in filled_lattice._nodes_list[SHAPE_LATTICE_LAYER]:
      # check connections between shape and top nodes
      self.assertTrue(len(shape.get_parents()) == 1)
      self.assertTrue(shape in top.get_children())
      self.assertTrue(top in shape.get_parents())

      # check that the two shapes that were filled between have a glued edge as a child 
      # (8S1000 and 8S10 are the shapes that were filled between, so we only need to check for those)
      if shape._label == "8S10" or shape._label == "8S1000":
        found = False
        children = shape.get_children()
        for child in children:
          if child in glued_edges:
              self.assertTrue(shape in child.get_parents())
              found = True
        # found means that the shape has at least one glued edge
        self.assertTrue(found)

    # now, to check for glued edge connections
    for glued_edge in glued_edges:
      # check that the edge has the correct number of parents and children
      self.assertTrue(len(glued_edge.get_parents()) == 2) #@ can only connect to 2 shapes max in this shape!
      self.assertTrue(len(glued_edge.get_children()) == 2) # can only have 2 children safe to assume for all

      parent_lengths = [] #@ change or remove in other tests if needed
      for child in glued_edge.get_children():

        #@ check that one of the children has 3 connections and the other has 6 connections
        if len(child.get_parents()) == 3 or len(child.get_parents()) == 6:#@ this part of the code is unique for this test case
          parent_lengths.append(len(child.get_parents()))                 #@ change or remove it in other tests         
        self.assertTrue(glued_edge in child.get_parents())                #@          

      self.assertEqual(set([3,6]), set(parent_lengths))                   #@ 

    # now to check bottom node connections
    for vertex in filled_lattice._nodes_list[VERTEX_LATTICE_LAYER]:
      # check that all vertices have the correct number of parents and children
      self.assertTrue(len(vertex.get_children()) == 1) # can only have one child (bottom node)
      # check that the bottom is connected to the vertices in both ways
      self.assertTrue(vertex in bot.get_parents())
      self.assertTrue(bot in vertex.get_children())

  def test_fill_gap_square_tie_square(self):
    l1 = LatticeTest(4)
    l2 = LatticeTest(4)

    # glue the first two shapes
    v1 = l1._bot_node.get_parents()[0]
    v2 = l2._bot_node.get_parents()[0]

    glue1 = l1.glue_vertex(v1, l2, v2)

    # glue1._geo_graph.show()
    # glue1.show()

    # glue the third shape
    v3 = glue1.get_node_from_label("3V0")
    v4 = glue1.get_node_from_label("4V1")

    glue2 = glue1.fill_gap(v3, l2, v4)


  
if __name__ == "__main__":
    unittest.main()