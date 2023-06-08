import unittest
import networkx as nx
import sys

  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice      import *
from lattice_test import LatticeTest
from node         import Node

class TestGlueEdge(unittest.TestCase):

#------------throw exceptions-----------

  def test_glue_edge_u_not_node(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    lat2_edge = lat2._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge("str", lat2, lat2_edge)
  
  def test_glue_edge_v_not_node(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    lat1_edge = lat1._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge(lat1_edge, lat2, 4)

  def test_glue_edge_u_not_in_self(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    node = Node(0)
    lat2_edge = lat2._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge(node, lat2, lat2_edge)

  def test_glue_edge_v_not_in_lat_v(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    node = Node(0)
    lat1_edge = lat1._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge(lat1_edge, lat2, node)

  def test_glue_edge_u_not_edge_in_self(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    lat2_edge = lat2._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge(lat1._top_node, lat2, lat2_edge)

  def test_glue_edge_v_not_edge_in_lat_v(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(3)
    lat1_edge = lat1._top_node.get_children()[0].get_children()[0]
    with self.assertRaises(Exception):
      lat1.glue_edge(lat1_edge, lat2, lat2._top_node)

  def test_glue_edge_self_is_lat_v(self):
    lat1 = LatticeTest(3)
    lat1_edge1 = lat1._top_node.get_children()[0].get_children()[0]
    lat1_edge2 = lat1._top_node.get_children()[0].get_children()[1]
    with self.assertRaises(Exception):
      lat1.glue_edge(lat1_edge1, lat1, lat1_edge2)

  def test_glue_edge_self_is_line_segment(self):                                          # prob a better way to assert these two idk
    lat1 = LatticeTest(2)
    lat2 = LatticeTest(3)
    lat1_edge = lat1._top_node.get_children()[0].get_children()[0]
    lat2_edge = lat2._top_node.get_children()[0].get_children()[0]
    self.assertTrue(isinstance(lat1.glue_edge(lat1_edge, lat2, lat2_edge), Lattice))

  def test_glue_edge_lat_v_is_line_segment(self):
    lat1 = LatticeTest(3)
    lat2 = LatticeTest(2)
    lat1_edge = lat1._top_node.get_children()[0].get_children()[0]
    lat2_edge = lat2._top_node.get_children()[0].get_children()[0]
    self.assertTrue(isinstance(lat1.glue_edge(lat1_edge, lat2, lat2_edge), Lattice))

# ----------basic edge gluing-----------

  # glue two triangles together by the edge
  #    *
  #   /|\
  #  / | \
  # *--*--*
  def test_glue_edge_same_shape(self):
    l1 = LatticeTest(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    edges1 = vertex_node1.get_parents()
    edge_node1 = edges1[0]

    l2 = LatticeTest(3)
    vertex_nodes2 = l2._bot_node.get_parents()
    vertex_node2 = vertex_nodes2[0]
    edges2 = vertex_node2.get_parents()
    edge_node2 = edges2[0]
    post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

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
      

  # *----*
  # |    | \
  # *----*--*
  def test_glue_edge_diff_shapes(self):
    l1 = LatticeTest(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    edges1 = vertex_node1.get_parents()
    edge_node1 = edges1[0]

    l2 = LatticeTest(4)
    vertex_nodes2 = l2._bot_node.get_parents()
    vertex_node2 = vertex_nodes2[0]
    edges2 = vertex_node2.get_parents()
    edge_node2 = edges2[0]
    post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

    new_node = post_glued._testing_node_2

    # number of nodes and edges
    self.assertEqual(post_glued.number_of_nodes(), 15) #u-pdatesd
    self.assertEqual(post_glued.number_of_edges(), 52) #updated

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued.list_layer_lengths(), [1, 5, 6, 2, 1]) #updated

    # check proper number of ties up and down from bottom node
    self.assertEqual(5, len(post_glued._bot_node.get_parents())) #updated
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

      # check new tied edge node in shape node's children
      self.assertTrue(new_node in s_node.get_children())

      # check proper number of ties from shape down to edge level
      if str(s_node)[-1] == "0":
        self.assertEqual(3, len(s_node.get_children()))
      else:
        self.assertEqual(4, len(s_node.get_children()))
    
#--------more complicated stuff---------
    
  # *-----*-----* # attempt to glue two shapes on the SAME edge
  # |     | \   |
  # |     |  \  |
  # *-----*---\-* # not allowed!!!!!
  #        \   \
  #         *---*
  def test_glue_edge_two_on_same_edge(self):
    l1 = LatticeTest(4)
    vertex_node1 = l1._bot_node.get_parents()[0]
    edge_node1 = vertex_node1.get_parents()[0]

    l2 = LatticeTest(4)
    vertex_node2 = l2._bot_node.get_parents()[0]
    edge_node2 = vertex_node2.get_parents()[0]
    
    post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

    new_edge = post_glued._testing_node_1

    l3 = LatticeTest(4)
    vertex_node3 = l3._bot_node.get_parents()[0]
    edge_node3 = vertex_node3.get_parents()[0]

    with self.assertRaises(Exception):
      illegal_glued = post_glued.glue_edge(new_edge, l3, edge_node3)
  
  #
  #       *-----*
  #       |     |
  #       |     |
  # *-----*-----*
  # |     |     |
  # |     |     |
  # *-----*-----*
  def test_glue_edge_two_sides(self):
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

    post_glued_2 = post_glued.glue_edge(next_edge_to_glue, l3, edge_node3)

    #* ASSERT TIME!!!! -----------------------------
    #@ denotes that it needs to be updated if we copy and paste to a different test

    # number of nodes and edges
    post_glued_2.print_lattice()
    self.assertEqual(post_glued_2.number_of_nodes(), 23) #@
    self.assertEqual(post_glued_2.number_of_edges(), 86) #@

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued_2.list_layer_lengths(), [1, 8, 10, 3, 1]) #@

    # check proper number of ties up and down from bottom node
    self.assertEqual(8, len(post_glued_2._bot_node.get_parents())) #@
    self.assertEqual(0, len(post_glued_2._bot_node.get_children()))

    # for each vertex node in post_glued_2...
    for v_node in post_glued_2._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children())) 

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued_2._bot_node.get_parents())
      self.assertTrue(post_glued_2._bot_node in v_node.get_children())

      # check proper number of ties up and down from top node
      self.assertEqual(3, len(post_glued_2._top_node.get_children())) #@
      self.assertEqual(0, len(post_glued_2._top_node.get_parents()))

    first_glued = post_glued_2._testing_node_1
    second_glued = post_glued_2._testing_node_2

    # first glued edge---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(first_glued.get_children())) 
    self.assertEqual(2, len(first_glued.get_parents()))

    big_node = None
    mid_nodes = []
    for v in post_glued_2._nodes_list[VERTEX_LATTICE_LAYER]:
      if len(v.get_parents()) == 4:
        big_node = v
      elif len(v.get_parents()) == 3:
        mid_nodes.append(v)

    self.assertTrue(big_node in first_glued.get_children())
    self.assertTrue(first_glued in big_node.get_parents())

    for s_node in first_glued.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued_2._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued_2._top_node.get_children())

      # check new tied edge node in shape node's children
      self.assertTrue(first_glued in s_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertEqual(4, len(s_node.get_children()))

    # second glued edge---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(second_glued.get_children()))
    self.assertEqual(2, len(second_glued.get_parents()))

    self.assertTrue(big_node in second_glued.get_children())
    self.assertTrue(second_glued in big_node.get_parents())

    for s_node in second_glued.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued_2._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued_2._top_node.get_children())

      # check new tied edge node in shape node's children
      self.assertTrue(second_glued in s_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertEqual(4, len(s_node.get_children())) 


  # # triangle with three quadrilaterals
  # #          *   *
  # #         / \ / \
  # #        /   *   \ 
  # #       *\  / \ /*         
  # #          *---*
  # #          |   |
  # #          *---*
  def test_glue_edge_all_edges(self):
    tri = LatticeTest(3)
    edges_tri = tri._top_node.get_children()[0].get_children()
    tri_edge = edges_tri[0]

    quad1 = LatticeTest(4)
    edge_quad1 = quad1._top_node.get_children()[0].get_children()[0]
    quad2 = LatticeTest(4)
    edge_quad2 = quad2._top_node.get_children()[0].get_children()[0]
    quad3 = LatticeTest(4)
    edge_quad3 = quad3._top_node.get_children()[0].get_children()[0]

    post_glued1 = tri.glue_edge(tri_edge, quad1, edge_quad1) # triangle and square

    #* need to check that the shape we're searching is a triangle
    triangle = None
    for i in post_glued1._nodes_list[SHAPE_LATTICE_LAYER]:
      if len(i.get_children()) == 3:
        triangle = i

    #loop through edges until we find one without more than one shape glued to it
    next_edge_to_glue = triangle.get_children()[0]
    i = 1
    while len(next_edge_to_glue.get_parents()) > 1:
      next_edge_to_glue = triangle.get_children()[i]
      i += 1 

    post_glued2 = post_glued1.glue_edge(next_edge_to_glue, quad2, edge_quad2) # triangle and 2 squares
    
    #* need to check that the shape we're searching is a triangle
    triangle = None
    for i in post_glued2._nodes_list[SHAPE_LATTICE_LAYER]:
      if len(i.get_children()) == 3:
        triangle = i

    #loop through edges until we find one without more than one shape glued to it
    next_edge_to_glue = triangle.get_children()[0]
    i = 1
    while len(next_edge_to_glue.get_parents()) > 1:
      next_edge_to_glue = triangle.get_children()[i]
      i += 1 

    post_glued3 = post_glued2.glue_edge(next_edge_to_glue, quad3, edge_quad3) # triangle and 3 squares

    #* now we need to know the triangle for testing purposes
    triangle = None
    for i in post_glued3._nodes_list[SHAPE_LATTICE_LAYER]:
      if len(i.get_children()) == 3:
        triangle = i

    #----------- ASSERTION TIME!!!!!!!!!------------------------------#
    self.assertEqual(post_glued3.number_of_nodes(), 27)

    self.assertEqual(post_glued3.number_of_edges(), 104)
    
    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued3.list_layer_lengths(), [1, 9, 12, 4, 1])

    # check proper number of ties up and down from bottom node
    self.assertEqual(9, len(post_glued3._bot_node.get_parents()))
    self.assertEqual(0, len(post_glued3._bot_node.get_children()))

    # for each vertex node in post_glued_2...
    for v_node in post_glued3._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children())) 

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued3._bot_node.get_parents())
      self.assertTrue(post_glued3._bot_node in v_node.get_children())

      # check proper number of ties up and down from top node
      self.assertEqual(4, len(post_glued3._top_node.get_children()))
      self.assertEqual(0, len(post_glued3._top_node.get_parents()))

    first_glued   = post_glued3._testing_node_0
    second_glued  = post_glued3._testing_node_1
    third_glued   = post_glued3._testing_node_2

    #now to test connections for   E A C H   glued edge :O

    # first glued edge---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(first_glued.get_children())) 
    self.assertEqual(2, len(first_glued.get_parents()))

    for s_node in first_glued.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued3._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued3._top_node.get_children())

      # check new tied edge node in shape node's children
      self.assertTrue(first_glued in s_node.get_children())

      # check proper number of ties from shape down to edge level
      if s_node is triangle:
        self.assertEqual(3, len(s_node.get_children()))
      else:
        self.assertEqual(4, len(s_node.get_children()))
    
    # second glued edge---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(second_glued.get_children())) 
    self.assertEqual(2, len(second_glued.get_parents()))

    for s_node in second_glued.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued3._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued3._top_node.get_children())

      # check new tied edge node in shape node's children
      self.assertTrue(second_glued in s_node.get_children())

      # check proper number of ties from shape down to edge level
      if s_node is triangle:
        self.assertEqual(3, len(s_node.get_children()))
      else:
        self.assertEqual(4, len(s_node.get_children()))

    # third glued edge---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(third_glued.get_children())) 
    self.assertEqual(2, len(third_glued.get_parents()))

    for s_node in third_glued.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued3._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued3._top_node.get_children())

      # check new tied edge node in shape node's children
      self.assertTrue(third_glued in s_node.get_children())

      # check proper number of ties from shape down to edge level
      if s_node is triangle:
        self.assertEqual(3, len(s_node.get_children()))
      else:
        self.assertEqual(4, len(s_node.get_children()))
    
  #   *            *   *
  #  /|\          /|\ /|
  # * | *   then * | X |
  #  \|/          \|/ \|
  #   *            *   *
  def test_glue_edge_then_vertex(self):
    l1 = LatticeTest(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]
    edges1 = vertex_node1.get_parents()
    edge_node1 = edges1[0]

    l2 = LatticeTest(3)
    vertex_nodes2 = l2._bot_node.get_parents()
    vertex_node2 = vertex_nodes2[0]
    edges2 = vertex_node2.get_parents()
    edge_node2 = edges2[0]
    post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

    vertex_to_glue = post_glued._bot_node.get_parents()[2]

    l3 = LatticeTest(3)
    vertex = l3._bot_node.get_parents()[0]

    post_glued2 = post_glued.glue_vertex(vertex_to_glue, l3, vertex)

    glued_edge = post_glued2._testing_node_1
    glued_vertex = post_glued2._testing_node_2

    #------------- ASSERTION TIME!!-------------------------#

    # number of nodes and edges
    self.assertEqual(post_glued2.number_of_nodes(), 19)
    self.assertEqual(post_glued2.number_of_edges(), 68)

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued2.list_layer_lengths(), [1, 6, 8, 3, 1])

    # check proper number of ties up and down from bottom node
    self.assertEqual(6, len(post_glued2._bot_node.get_parents()))
    self.assertEqual(0, len(post_glued2._bot_node.get_children()))

    # for each vertex node in post_glued...
    for v_node in post_glued2._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children()))

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued2._bot_node.get_parents())
      self.assertTrue(post_glued2._bot_node in v_node.get_children())

    # testing the edge node---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(glued_edge.get_children()))
    self.assertEqual(2, len(glued_edge.get_parents()))

    # for each vertex level node in new node's children...
    for v_node_on_new in glued_edge.get_children():
      # check proper number of ties up to edge level
      self.assertEqual(3, len(v_node_on_new.get_parents()))
      # check tied up to new_node
      self.assertTrue(glued_edge in v_node_on_new.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(3, len(post_glued2._top_node.get_children()))
    self.assertEqual(0, len(post_glued2._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for s_node in glued_edge.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued2._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued2._top_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertEqual(3, len(s_node.get_children()))

      # check new tied edge node in shape node's children
      self.assertTrue(glued_edge in s_node.get_children())

    #now to test the vertex------------------------------------
    # check proper number of ties up and down from glued vertex node
    self.assertEqual(1, len(glued_vertex.get_children()))
    self.assertEqual(4, len(glued_vertex.get_parents()))

    self.assertTrue(post_glued2._bot_node in glued_vertex.get_children())
    self.assertTrue(glued_vertex in post_glued2._bot_node.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(3, len(post_glued2._top_node.get_children()))
    self.assertEqual(0, len(post_glued2._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for edge in glued_vertex.get_parents():
      # edge should be connected to 1 shape
      self.assertEqual(1, len(edge.get_parents()))

      # check new tied edge node in shape node's children
      self.assertTrue(glued_vertex in edge.get_children())

  #   *   *          *   *
  #   |\ /|         /|\ /|
  #   | X |   then * | X |
  #   |/ \|         \|/ \|
  #   *   *          *   *
  def test_glue_vertex_then_edge(self):
    l1 = LatticeTest(3)
    vertex_nodes1 = l1._bot_node.get_parents()
    vertex_node1 = vertex_nodes1[0]

    l2 = LatticeTest(3)
    vertex_nodes2 = l2._bot_node.get_parents()
    vertex_node2 = vertex_nodes2[0]

    post_glued = l1.glue_vertex(vertex_node1, l2, vertex_node2)

    edge_to_glue = post_glued._bot_node.get_parents()[2].get_parents()[0]

    l3 = LatticeTest(3)
    vertex = l3._bot_node.get_parents()[0]
    edge = vertex.get_parents()[0]

    post_glued2 = post_glued.glue_edge(edge_to_glue, l3, edge)

    glued_vertex = post_glued2._testing_node_1
    glued_edge = post_glued2._testing_node_2

    #------------- ASSERTION TIME!!-------------------------#

    # number of nodes and edges
    self.assertEqual(post_glued2.number_of_nodes(), 19)
    self.assertEqual(post_glued2.number_of_edges(), 68)

    # correct distribution of nodes among the layers 
    self.assertEqual(post_glued2.list_layer_lengths(), [1, 6, 8, 3, 1])

    # check proper number of ties up and down from bottom node
    self.assertEqual(6, len(post_glued2._bot_node.get_parents()))
    self.assertEqual(0, len(post_glued2._bot_node.get_children()))

    # for each vertex node in post_glued...
    for v_node in post_glued2._nodes_list[VERTEX_LATTICE_LAYER]:
      # check proper number of ties down to bottom node
      self.assertEqual(1, len(v_node.get_children()))

      #check tied up   from bottom to v_node
      # and       down from v_node to bottom
      self.assertTrue(v_node in post_glued2._bot_node.get_parents())
      self.assertTrue(post_glued2._bot_node in v_node.get_children())

    # testing the edge node---------------------------
    # check proper number of ties up and down from glued edge node
    self.assertEqual(2, len(glued_edge.get_children()))
    self.assertEqual(2, len(glued_edge.get_parents()))

    # for each vertex level node in new node's children...
    for v_node_on_new in glued_edge.get_children():
      # check proper number of ties up to edge level
      self.assertEqual(3, len(v_node_on_new.get_parents()))
      # check tied up to new_node
      self.assertTrue(glued_edge in v_node_on_new.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(3, len(post_glued2._top_node.get_children()))
    self.assertEqual(0, len(post_glued2._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for s_node in glued_edge.get_parents():
      # check proper number of ties up to top level
      self.assertEqual(1, len(s_node.get_parents()))

      # check tied up   from shape to top
      # and        down from top to shape
      self.assertTrue(post_glued2._top_node in s_node.get_parents())
      self.assertTrue(s_node in post_glued2._top_node.get_children())

      # check proper number of ties from shape down to edge level
      self.assertEqual(3, len(s_node.get_children()))

      # check new tied edge node in shape node's children
      self.assertTrue(glued_edge in s_node.get_children())

    #now to test the vertex------------------------------------
    # check proper number of ties up and down from glued vertex node
    self.assertEqual(1, len(glued_vertex.get_children()))
    self.assertEqual(4, len(glued_vertex.get_parents()))

    self.assertTrue(post_glued2._bot_node in glued_vertex.get_children())
    self.assertTrue(glued_vertex in post_glued2._bot_node.get_parents())
    
    # check proper number of ties up and down from top node
    self.assertEqual(3, len(post_glued2._top_node.get_children()))
    self.assertEqual(0, len(post_glued2._top_node.get_parents()))

    #for each shape level node in parents of new_node...
    for edge in glued_vertex.get_parents():
      # edge should be connected to 1 shape
      self.assertEqual(1, len(edge.get_parents()))

      # check new tied edge node in shape node's children
      self.assertTrue(glued_vertex in edge.get_children())


if __name__ == "__main__":
    unittest.main()