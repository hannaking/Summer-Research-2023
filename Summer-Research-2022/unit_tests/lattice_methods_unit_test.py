import unittest
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice import *
from lattice_test import *
from node    import Node
from unit_tests.shape_helpers import ShapeHelpers

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class TestMethods(unittest.TestCase):

    def test_print_cool_lattices(self):
        lattice = Lattice(6)
        lattice.show()

        # --------------------- get corresponding coordinates ------------------- #
    def test_get_corresponding_coordinates_simple_triangle(self):
        lattice = Lattice(3)
        coordinates = [x for x in lattice._get_corresponding_coordinates(0)]
        self.assertEqual(coordinates, [0,1,2])

    def test_get_corresponding_coordinates_simple_quadrilateral(self):
        lattice = Lattice(4)
        coordinates = [x for x in lattice._get_corresponding_coordinates(0)]
        self.assertEqual(coordinates, [0,1,2,3])

    def test_get_corresponding_coordinates_triangle_bowtie_shape_1(self):
        lattice = ShapeHelpers.bowtie()
        coordinates = [x for x in lattice._get_corresponding_coordinates(0)]
        self.assertEqual(coordinates, [0,1,2])

    def test_get_corresponding_coordinates_triangle_bowtie_shape_2(self):
        lattice = ShapeHelpers.bowtie()
        coordinates = [x for x in lattice._get_corresponding_coordinates(1)]
        self.assertEqual(coordinates, [3,0,4])

    def test_get_corresponding_coordinates_pentagram_shape_1_pentagon(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(0)]
        self.assertEqual(coordinates, [0,1,2,3,4])

    def test_get_corresponding_coordinates_pentagram_shape_2(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(1)]
        self.assertEqual(coordinates, [5,1,0])

    def test_get_corresponding_coordinates_pentagram_shape_3(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(2)]
        # self.assertEqual(coordinates, [5,6,7])

    def test_get_corresponding_coordinates_pentagram_shape_4(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(3)]
        # self.assertEqual(coordinates, [8,9,10])

    def test_get_corresponding_coordinates_pentagram_shape_5(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(4)]
        # self.assertEqual(coordinates, [11,12,13])

    def test_get_corresponding_coordinates_pentagram_shape_6(self):
        lattice = ShapeHelpers.pentagram()
        coordinates = [x for x in lattice._get_corresponding_coordinates(5)]
        # self.assertEqual(coordinates, [14,15,16])


    #---------------------------------get connected edges--------------------------------
    def test_get_connected_edges_lonely_vertex(self):
        vertex = Node(VERTEX_LATTICE_LAYER)

        connected_edges = Lattice.get_connected_edges(vertex)

        expected = [ ] # no edges connected to a lone vertex
        self.assertCountEqual(connected_edges, expected)

    def test_get_connected_edges_vertex_on_one_edge(self):
        seg = Lattice(2)
        vertex = seg._nodes_list[VERTEX_LATTICE_LAYER][0]

        connected_edges = Lattice.get_connected_edges(vertex)

        expected = [
            seg._nodes_list[EDGE_LATTICE_LAYER][0]
        ]

        self.assertCountEqual(connected_edges, expected)

    def test_get_connected_edges_vertex_on_two_edges(self):
        tri = Lattice(3)
        vertex = tri._nodes_list[VERTEX_LATTICE_LAYER][0]

        connected_edges = Lattice.get_connected_edges(vertex)

        # connected edges are merely the vertex's parents on the lattice
        parents = vertex.get_parents()
        expected = []
        for parent in parents:
            expected.append(parent)

        self.assertCountEqual(connected_edges, expected)

    def test_get_connected_edges_vertex_on_three_edges(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()
        vertex = shape.get_node_from_label("2V0")
        
        connected_edges = Lattice.get_connected_edges(vertex)

        # connected edges are merely the vertex's parents on the lattice
        parents = vertex.get_parents()
        expected = []
        for parent in parents:
            expected.append(parent)
        

        self.assertCountEqual(connected_edges, expected)
    
# ---------------------- get node from label -----------------#
    def test_get_node_from_label_not_a_string(self):
        l1 = Lattice(3)
        with self.assertRaises(Exception):
            l1.get_node_from_label(13398)

    def test_get_node_from_label_doesnt_exist_in_lattice(self):
        l1 = Lattice(3)
        self.assertEqual(l1.get_node_from_label("15V"), None)

    def test_get_node_from_label_bottom(self):
        l1 = Lattice(3)
        expected = l1._bot_node
        label = "1B"
        self.assertEqual(expected, l1.get_node_from_label(label))

    def test_get_node_from_label_vertex(self):
        l1 = Lattice(3)
        expected = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
        label = "3V"
        self.assertEqual(expected, l1.get_node_from_label(label))

    def test_get_node_from_label_edge(self):
        l1 = Lattice(3)
        expected = l1._nodes_list[EDGE_LATTICE_LAYER][1]
        label = "6E"
        self.assertEqual(expected, l1.get_node_from_label(label))

    def test_get_node_from_label_shape(self):
        l1 = Lattice(3)
        expected = l1._nodes_list[SHAPE_LATTICE_LAYER][0]
        label = "8S"
        self.assertEqual(expected, l1.get_node_from_label(label))

    def test_get_node_from_label_bottom(self):
        l1 = Lattice(3)
        expected = l1._top_node
        label = "0T"
        self.assertEqual(expected, l1.get_node_from_label(label))

# -----------------------------------get_top tests--------------------------------
    
    ## get_top_from_node
    def test_get_top_from_node_level_0(self): # bottom node
        l1 = Lattice(3)
        node_to_input = l1._bot_node
        expected_node = l1._top_node
        self.assertTrue(l1.get_top_from_node(node_to_input) == expected_node)

    def test_get_top_from_node_level_1(self):
        l1 = Lattice(3)
        node_to_input = l1._bot_node.get_parents()[0]
        expected_node = l1._top_node
        self.assertTrue(l1.get_top_from_node(node_to_input) == expected_node)

    def test_get_top_from_node_level_2(self):
        l1 = Lattice(3)
        node_to_input = l1._bot_node.get_parents()[0]
        node_to_input = node_to_input.get_parents()[0]
        expected_node = l1._top_node
        self.assertTrue(l1.get_top_from_node(node_to_input) == expected_node)

    def test_get_top_from_node_level_3(self):
        l1 = Lattice(3)
        v_nodes = l1._top_node.get_children()
        v_node = v_nodes[0]
        self.assertEqual(l1.get_top_from_node(v_node), l1._top_node)

    def test_get_top_from_node_level_4(self): #top node
        l1 = Lattice(3)
        self.assertEqual(l1.get_top_from_node(l1._top_node), l1._top_node)

#-----------------------------------get_bot tests----------------------------------
    
    ## get_bot_from_node
    def test_get_bot_from_node_level_0(self): # bottom node
        l1 = Lattice(3)
        node_to_input = l1._bot_node
        expected_node = l1._bot_node
        self.assertTrue(l1.get_bot_from_node(node_to_input) == expected_node)

    def test_get_bot_from_node_level_1(self):
        l1 = Lattice(3)
        node_to_input = l1._bot_node.get_parents()[0]
        expected_node = l1._bot_node
        self.assertTrue(l1.get_bot_from_node(node_to_input) == expected_node)

    def test_get_bot_from_node_level_2(self):
        l1 = Lattice(3)
        node_to_input = l1._bot_node.get_parents()[0]
        node_to_input = node_to_input.get_parents()[0]
        expected_node = l1._bot_node
        self.assertTrue(l1.get_bot_from_node(node_to_input) == expected_node)

    def test_get_bot_from_node_level_3(self):
        l1 = Lattice(3)
        v_nodes = l1._top_node.get_children()
        v_node = v_nodes[0]
        self.assertEqual(l1.get_bot_from_node(v_node), l1._bot_node)

    def test_get_bot_from_node_level_4(self): # top node
        l1 = Lattice(3)
        self.assertEqual(l1.get_bot_from_node(l1._top_node), l1._bot_node)

#---------------------------------------list layer lengths-------------------------------

    def test_list_layer_lengths_triangle_lattice(self):
        l1 = Lattice(3)
        correct_list = [1, 3, 3, 1, 1]

        self.assertEqual(correct_list, l1.list_layer_lengths())

    def test_list_layer_lengths_quad_lattice(self):
        l1 = Lattice(4)
        correct_list = [1, 4, 4, 1, 1]

        self.assertEqual(correct_list, l1.list_layer_lengths())

    #!another one here for post-gluing vertex and post-gluing edges

#--------------------------remove node tests------------------------------------#

    def test_remove_node_top(self):
        l1 = Lattice(3)
        node_to_remove = l1._top_node
        child_node = node_to_remove.get_children()[0]

        l1._remove_node(node_to_remove)

        exists = child_node._exists_in_parents(node_to_remove)
        self.assertFalse(exists) # should no longer exist

    def test_remove_node_shape(self):
        l1 = Lattice(2)
        node_to_remove = l1._top_node.get_children()[0]
        child_node = node_to_remove.get_children()[0]
        l1._remove_node(node_to_remove)

        exists = child_node._exists_in_parents(node_to_remove)
        self.assertFalse(exists)

    def test_remove_node_edge(self):
        l1 = Lattice(3)
        node_to_remove = l1._top_node.get_children()[0].get_children()[0]
        child_node = node_to_remove.get_children()[0]

        l1._remove_node(node_to_remove)

        exists = child_node._exists_in_parents(node_to_remove)
        self.assertFalse(exists)

    def test_remove_node_vertex(self):
        l1 = Lattice(3)
        node_to_remove = l1._bot_node.get_parents()[0]
        child_node = node_to_remove.get_children()[0]

        l1._remove_node(node_to_remove)

        exists = child_node._exists_in_parents(node_to_remove)
        self.assertFalse(exists)

    # you can't display a lattice without a bottom node 
    # or else it will just  the blue dot (the bottom node still exists,
    # but is severed)
    def test_remove_node_bottom(self): 
        l1 = Lattice(3)
        node_to_remove = l1._bot_node
        parent_node = node_to_remove.get_parents()[0]

        l1._remove_node(node_to_remove)

        exists = parent_node._exists_in_children(node_to_remove)
        self.assertFalse(exists)

    def test_remove_non_node(self):
        l1 = Lattice(3)
        with self.assertRaises(Exception):
            l1._remove_node("not a node")

    def test_remove_node_not_in_lattice(self):
        l1 = Lattice(2)
        
        mystery_node = Node(0)
        with self.assertRaises(Exception):
            l1._remove_node(mystery_node)
#--------------------------------merge tests------------------------------------#
    def test_merge_children_are_added_bottom_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._bot_node
        node2 = l2._bot_node

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_children()), 0) # 空荡荡的 lmao #????
        
    def test_merge_parents_are_added_bottom_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._bot_node
        node2 = l2._bot_node

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_parents()), 6) # 3 + 3 vertices from each lattice = sqrt(36)

        #check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

        # check that the new node exists in the children of its parents
        for parent in new_node.get_parents():
            self.assertTrue(new_node in parent.get_children())
    
    def test_merge_children_are_added_vertex_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._bot_node.get_parents()[0]
        node2 = l2._bot_node.get_parents()[1]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_children()), 2) #two bottom nodes bc not gluing

        #check that bottom nodes exist in the children of the new node
        for bottom in l1._nodes_list[BOTTOM_LATTICE_LAYER]:
            self.assertTrue(bottom in new_node.get_children())

    def test_merge_parents_are_added_vertex_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._bot_node.get_parents()[0]
        node2 = l2._bot_node.get_parents()[1]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_parents()), 4) # 2+2 from each vertex = ((5 - 1) ^ 0) + 3 - (-1)

        #check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

        # check that the new node exists in the children of its parents
        for parent in new_node.get_parents():
            self.assertTrue(new_node in parent.get_children())
        
    def test_merge_children_are_added_edge_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._bot_node.get_parents()[0].get_parents()[0]
        node2 = l2._bot_node.get_parents()[0].get_parents()[0]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_children()), 4) # four vertex nodes, because vertices aren't merged

        # check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

        self.assertEqual(len(new_node.get_parents()), 2)

        # check that the new node exists in the children of its parents
        for parent in new_node.get_parents():
            self.assertTrue(new_node in parent.get_children())

    def test_merge_parents_are_added_edge_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._top_node.get_children()[0].get_children()[0]
        node2 = l2._top_node.get_children()[0].get_children()[0]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_children()), 4) # four vertex nodes, because vertices aren't merged

        # check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

        self.assertEqual(len(new_node.get_parents()), 2) # two shape nodes

        # check that the new node exists in the children of its parents
        for parent in new_node.get_parents():
            self.assertTrue(new_node in parent.get_children())
        
    def test_merge_children_are_added_shape_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._top_node.get_children()[0]
        node2 = l2._top_node.get_children()[0]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_children()), 6) #3+3 from each shape (it's a triangle duhhh) = 7 - 1

        #check that all nodes exist in the children of the new node
        for edge in l1._nodes_list[EDGE_LATTICE_LAYER]:
            self.assertTrue(edge in new_node.get_children())

        # check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

    def test_merge_parents_are_added_shape_node(self):
        l1 = Lattice(3)
        l2 = Lattice(3)
        node1 = l1._top_node.get_children()[0]
        node2 = l2._top_node.get_children()[0]

        l1.smash_lattices(l2)
        new_node = l1._merge(node1, node2)

        self.assertEqual(len(new_node.get_parents()), 2) # 1+1 top node from each shape = (12 / 4) - 1

        #check that the new node exists in the parents of its children
        for children in new_node.get_children():
            self.assertTrue(new_node in children.get_parents())

        # check that the new node exists in the children of its parents
        for parent in new_node.get_parents():
            self.assertTrue(new_node in parent.get_children())
        
    
#---------------------------smash lattice----------------------------------------#
    def test_smash_lattices_two_triangles(self):
        l1 = Lattice(3)
        l2 = Lattice(3)    
        l1 = l1.smash_lattices(l2)

        lengths_of_lists_after_smash = l1.list_layer_lengths()
        expected_l1_list_lengths = [2, 6, 6, 2, 2]
        expected_l2_list_lengths = []

        self.assertEqual(expected_l1_list_lengths, lengths_of_lists_after_smash)
        self.assertEqual(expected_l2_list_lengths, l2.list_layer_lengths())

    def test_smash_lattices_diff_shapes(self):
        l1 = Lattice(3)
        l2 = Lattice(4)    
        l1 = l1.smash_lattices(l2)

        lengths_of_lists_after_smash = l1.list_layer_lengths()
        expected_l1_list_lengths = [2, 7, 7, 2, 2]
        expected_l2_list_lengths = []

        self.assertEqual(expected_l1_list_lengths, lengths_of_lists_after_smash)
        self.assertEqual(expected_l2_list_lengths, l2.list_layer_lengths())

    def test_smash_lattices_not_a_lattice(self):
        l1 = Lattice(3)

        with self.assertRaises(Exception):
            l1.smash_lattices("not a lattice")

#----------------------------bfs tests--------------------------------------


#----------------------------find flagged tests-----------------------------
    def test_find_flagged_node_flagged_node_exists_top(self):
        l1 = Lattice(3)
        flagged_node = l1._top_node
        flagged_node.flag()
        found = l1._find_flagged_node(TOP_LATTICE_LAYER)

        self.assertTrue(found is flagged_node)

    def test_find_flagged_node_flagged_node_exists_shape(self):
        l1 = Lattice(3)
        flagged_node = l1._top_node.get_children()[0]
        flagged_node.flag()
        found = l1._find_flagged_node(SHAPE_LATTICE_LAYER)

        self.assertTrue(found is flagged_node)

    def test_find_flagged_node_flagged_node_exists_edge(self):
        l1 = Lattice(3)
        flagged_node = l1._top_node.get_children()[0].get_children()[0]
        flagged_node.flag()
        found = l1._find_flagged_node(EDGE_LATTICE_LAYER)

        self.assertTrue(found is flagged_node)

    def test_find_flagged_node_flagged_node_exists_vertex(self):
        l1 = Lattice(3)
        flagged_node = l1._bot_node.get_parents()[0]
        flagged_node.flag()
        found = l1._find_flagged_node(VERTEX_LATTICE_LAYER)

        self.assertTrue(found is flagged_node)

    def test_find_flagged_node_flagged_node_exists_bottom(self):
        l1 = Lattice(3)
        flagged_node = l1._bot_node
        flagged_node.flag()
        found = l1._find_flagged_node(BOTTOM_LATTICE_LAYER)

        self.assertTrue(found is flagged_node)

    def test_find_flagged_node_no_flagged_node_exists(self):
        l1 = Lattice(3)

        self.assertIsNone(l1._find_flagged_node(TOP_LATTICE_LAYER))
        self.assertIsNone(l1._find_flagged_node(SHAPE_LATTICE_LAYER))
        self.assertIsNone(l1._find_flagged_node(EDGE_LATTICE_LAYER))
        self.assertIsNone(l1._find_flagged_node(VERTEX_LATTICE_LAYER))
        self.assertIsNone(l1._find_flagged_node(BOTTOM_LATTICE_LAYER))

    def test_find_flagged_node_flagged_node_on_different_layer(self):
        l1 = Lattice(3)
        flagged_node = l1._bot_node
        flagged_node.flag()
        found = l1._find_flagged_node(TOP_LATTICE_LAYER)

        self.assertIsNone(found)

#--------------------------------make copy tests-----------------------------
    def test_make_copy_of_lattice_not_a_node(self):
        l1 = Lattice(3)

        with self.assertRaises(Exception):
            l1._make_copy_of_lattice("not a node")

    def test_make_copy_of_lattice_node_not_in_lattice(self):
        l1 = Lattice(3)
        node = Node(1)

        with self.assertRaises(Exception):
            l2 = l1._make_copy_of_lattice(node)

    def test_make_copy_of_lattice_ensure_flagged_in_copy(self):
        l1 = Lattice(3)
        node_to_flag = l1._top_node

        copy = l1._make_copy_of_lattice(node_to_flag)
        found = copy._find_flagged_node(4)

        self.assertTrue(found == copy._top_node)

#---------------------------find shortest path bfs (oh boy)----------------------#
    # def test_find_shortest_path_bfs_triangle(self):
    #     l1 = Lattice(3)
    #     node1 = l1._bot_node.get_parents()[0]
    #     node2 = l1._bot_node.get_parents()[1] 

    #     predecessors_dict = l1.find_shortest_path_bfs(node1)
    #     visited = []

    #     for key, value in predecessors_dict.items():
    #         visited.append(key)
        
    #     # this part is necessary because the visited list will not include the start node by itself
    #     # (bc there's no need to record the predecessor of the start node)
    #     visited_plus_start_node = visited
    #     visited_plus_start_node.append(node1)
    #     #this assert statement tests that every vertex in the lattice has been visited
    #     self.assertEqual(set(visited_plus_start_node), set(l1._nodes_list[VERTEX_LATTICE_LAYER]))

    # def test_find_shortest_path_bfs_three_quad(self):
    #     l1 = LatticeTest(4)
    #     l2 = LatticeTest(4)
    #     l3 = LatticeTest(4)
    #     n1 = l1._bot_node.get_parents()[0]
    #     n2 = l2._bot_node.get_parents()[0]
    #     n3 = l3._bot_node.get_parents()[0]

    #     two_squares = l1.glue_vertex(n1, l2, n2)
    #     glued_node = two_squares._testing_node_2
    #     next_node = two_squares._bot_node.get_parents()[0]
    #     if next_node is glued_node:
    #         next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

    #     three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

    #     node = three_squares._top_node.get_children()[0].get_children()[0].get_children()[0]

    #     predecessors_dict = three_squares.find_shortest_path_bfs(node)
    #     visited = []

    #     for key, value in predecessors_dict.items():
    #         visited.append(key)
        
    #     print("vertices in the actual lattice itself: ")
    #     for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
    #         print(i)

    #     visited_plus_start_node = visited
    #     visited_plus_start_node.append(node)

    #     print("vertices that have been visited: ")
    #     for i in visited_plus_start_node:
    #         print(i)
    #     self.assertEqual(set(visited_plus_start_node), set(three_squares._nodes_list[VERTEX_LATTICE_LAYER]))

#-------------------------find shortest path normal------------------------------#

    # def test_find_shortest_path_end_on_start_vertex(self):
    #     l1 = Lattice(3)
    #     node1 = l1._bot_node.get_parents()[0]
    #     node2 = l1._bot_node.get_parents()[1] 

    #     path = l1.find_shortest_path(node1, node2)

    #     self.assertIs(path[len(path) - 1], node1) #last item in path must be start node

    # def test_find_shortest_path_triangle(self):
    #     l1 = Lattice(3)
    #     node1 = l1._bot_node.get_parents()[0]
    #     node2 = l1._bot_node.get_parents()[1]
    #     node3 = l1._bot_node.get_parents()[2] 

    #     path = l1.find_shortest_path(node1, node3)
    #     expected_path = [node3, node1]

    #     self.assertEqual(expected_path, path)

    # def test_find_shortest_path_square(self):
    #     l1 = Lattice(4)
    #     node1 = l1._bot_node.get_parents()[0]
    #     node2 = l1._bot_node.get_parents()[1]
    #     node3 = l1._bot_node.get_parents()[2] # these nodes should be opposite each other on the square

    #     path = l1.find_shortest_path(node1, node3)
    #     expected_path = [node3, node2, node1]

    #     self.assertEqual(expected_path, path)

    # # find shortest path with two squares that are glued by a vertex
    # def test_find_shortest_path_two_quad(self):
    #     l1 = LatticeTest(4)
    #     l2 = LatticeTest(4)
    #     n1 = l1._bot_node.get_parents()[0]
    #     n2 = l2._bot_node.get_parents()[0]
        
    #     two_squares = l1.glue_vertex(n1, l2, n2)
    #     glued_node = two_squares._testing_node_2

    #     n1 = two_squares._top_node.get_children()[0].get_children()[0].get_children()[0]
    #     n2 = two_squares._top_node.get_children()[2].get_children()[0].get_children()[0]



    #     n1_connected_to_glued = l1.is_connected(glued_node, n1)
    #     n2_connected_to_glued = l1.is_connected(glued_node, n2)

    #     # i want to test the vertices that are connected to the glued vertex. you could use other vertices,
    #     # but i'm deciding for this test to use these vertices.
    #     if n1_connected_to_glued and n2_connected_to_glued:
    #         path = two_squares.find_shortest_path(n1, n2)
    #     else:
    #         print("problem with test, n1 and n2 are not connected to glued node")

    #     expected_path = [n2, glued_node, n1]

    #     self.assertEqual(expected_path, path)

   # find shortest path between three squares that are glued by two vertices
    # def test_find_shortest_path_three_quad(self):
    #     l1 = LatticeTest(4)
    #     l2 = LatticeTest(4)
    #     l3 = LatticeTest(4)
    #     n1 = l1._bot_node.get_parents()[0]
    #     n2 = l2._bot_node.get_parents()[0]
    #     n3 = l3._bot_node.get_parents()[0]

    #     two_squares = l1.glue_vertex(n1, l2, n2)
    #     glued_node = two_squares._testing_node_2
    #     next_node = two_squares._bot_node.get_parents()[0]
    #     if next_node is glued_node:
    #         next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

    #     three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

    #     glued_node_1 = three_squares._testing_node_1
    #     glued_node_2 = three_squares._testing_node_2

    #     n1 = three_squares._top_node.get_children()[0].get_children()[0].get_children()[0]
    #     n2 = three_squares._top_node.get_children()[1].get_children()[0].get_children()[0]
    #     n1_connected_to_glued = True if l1.is_connected(glued_node_1, n1) else l1.is_connected(glued_node_2, n1)
    #     n2_connected_to_glued = True if l1.is_connected(glued_node_1, n2) else l1.is_connected(glued_node_2, n2)

    #     # i want to test the vertices that are connected to the glued vertices. you could use other vertices,
    #     # but i'm deciding for this test to use these vertices.
    #     if n1_connected_to_glued and n2_connected_to_glued:
    #         path = three_squares.find_shortest_path(n1, n2) #@ the event
    #     else:
    #         print("problem with test, n1 and n2 are not connected to either glued node")

    #     expected_path = [n3, glued_node, n2, glued_node, n1]

    #     self.assertEqual(expected_path, path)
#---------------------shortest path network x---------------------------------------
    def test_shortest_path_triangle(self):
        l1 = Lattice(3)
        node1 = l1._bot_node.get_parents()[0]
        node3 = l1._bot_node.get_parents()[2] 


        path = l1.find_shortest_path(node1, node3)
        expected_path = [node1, node3]

        self.assertCountEqual(expected_path, path) 
    
    def test_shortest_path_square(self):
        l1 = Lattice(4)
        node1 = l1._bot_node.get_parents()[0]
        node2 = l1._bot_node.get_parents()[1]
        node3 = l1._bot_node.get_parents()[2] 
        node4 = l1._bot_node.get_parents()[3] 

        path = l1.find_shortest_path(node1, node3)
        expected_path_1 = [node1, node2, node3]
        expected_path_2 = [node1, node4, node3]
        
        self.assertTrue(expected_path_1 == path or expected_path_2 == path) 
    
    def test_shortest_path_two_squares(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        
        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_vertex = two_squares._testing_node_2
        
        # i want to get two vertices that are connected to the glued vertex
        # for testing purposes
        for i in two_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if two_squares.is_connected(i, glued_vertex):
                node1 = i

        for i in two_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if two_squares.is_connected(i, glued_vertex) and i is not node1:
                node2 = i
        
        path = two_squares.find_shortest_path(node1, node2)
        expected_path = [node1, glued_vertex, node2]

        self.assertEqual(expected_path, path)

    def test_shortest_path_three_squares(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        l3 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        n3 = l3._bot_node.get_parents()[0]

        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_node = two_squares._testing_node_2
        next_node = two_squares._bot_node.get_parents()[0]
        if next_node is glued_node:
            next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

        three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

        glued_node_1 = three_squares._testing_node_1
        glued_node_2 = three_squares._testing_node_2

        # i want one vertex that's connected to the first glued vertex,
        # and one that's connected to the second glued vertex
        # for testing purposes

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if three_squares.is_connected(i, glued_node_1):
                node1 = i

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if three_squares.is_connected(i, glued_node_2) and i is not glued_node_1:
                node2 = i

        path = three_squares.find_shortest_path(node1, node2)
        expected_path = [node1, glued_node_1, glued_node_2, node2]

        self.assertEqual(expected_path, path)

    def test_shortest_path_four_squares(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        l3 = LatticeTest(4)
        l4 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        n3 = l3._bot_node.get_parents()[0]
        n4 = l4._bot_node.get_parents()[0]

        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_node = two_squares._testing_node_2
        
        next_node = two_squares._bot_node.get_parents()[0]
        if next_node is glued_node:
            next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

        three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

        glued_node_1 = three_squares._testing_node_1
        glued_node_2 = three_squares._testing_node_2

        next_node = three_squares._bot_node.get_parents()[0]

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "5V10":
                next_node = i

        four_squares = three_squares.glue_vertex(next_node, l4, n4) # we now have FOUR SUQARES!! 3 + 1 = 7 - 3

        glued_node_1 = four_squares._testing_node_0
        glued_node_2 = four_squares._testing_node_1
        glued_node_3 = four_squares._testing_node_2

        for i in four_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "3V100":
                node1 = i

        for i in four_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "4V1":
                node2 = i

        path = four_squares.find_shortest_path(node1, node2)
        expected_path_1 = [node1, glued_node_1, glued_node_2, glued_node_3, node2]
        expected_path_2 = ["3V100", "2V000", "5V100", "3V1", "4V1"]

        # four_squares._geo_graph.show()
        
        label_list = []
        for i in path:
            label_list.append(i._label)

        self.assertTrue(expected_path_1 == path or expected_path_2 == label_list)


#---------------------convert to edge path-------------------------------------
    def test_convert_to_edge_path_2v_3v(self): #make sure order doesn't matter
        l1 = LatticeTest(4)
        v1 = l1.get_node_from_label("2V")
        v2 = l1.get_node_from_label("3V")

        path_2v3v = l1.find_shortest_path(v1, v2)
        path_2v3v = l1.convert_to_edge_path(path_2v3v)

        path_3v2v = l1.find_shortest_path(v2, v1)
        path_3v2v = l1.convert_to_edge_path(path_3v2v)

        self.assertEqual(path_2v3v, path_3v2v)

    def test_convert_to_edge_path_one_square(self):
        l1 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        edge = n1.get_parents()[0] 
        if n2 not in edge.get_children():
            edge = n1.get_parents()[1]

        path = l1.find_shortest_path(n1, n2)

        edge_path = l1.convert_to_edge_path(path)

        expected_edge_path = [edge]

        self.assertCountEqual(expected_edge_path, edge_path)

    def test_convert_to_edge_path_butterfly(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        
        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_vertex = two_squares._testing_node_2
        
        # i want to get two vertices that are connected to the glued vertex
        # for testing purposes
        for i in two_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if two_squares.is_connected(i, glued_vertex):
                node1 = i

        for i in two_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if two_squares.is_connected(i, glued_vertex) and i is not node1:
                node2 = i
        
        path = two_squares.find_shortest_path(node1, node2)
        edge_path = two_squares.convert_to_edge_path(path)
        expected_edge_path = []

        # only get the edges that are connected to the glued vertex and our start and end nodes
        for i in two_squares._nodes_list[EDGE_LATTICE_LAYER]:
            children = i.get_children()
            if glued_vertex in children:
                if node1 in children or node2 in children:
                    expected_edge_path.append(i)

        self.assertCountEqual(expected_edge_path, edge_path)

    def test_convert_to_edge_path_three_squares(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        l3 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        n3 = l3._bot_node.get_parents()[0]

        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_node = two_squares._testing_node_2
        next_node = two_squares._bot_node.get_parents()[0]
        if next_node is glued_node:
            next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

        three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

        glued_node_1 = three_squares._testing_node_1
        glued_node_2 = three_squares._testing_node_2

        # i want one vertex that's connected to the first glued vertex,
        # and one that's connected to the second glued vertex
        # for testing purposes

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if three_squares.is_connected(i, glued_node_1):
                node1 = i

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if three_squares.is_connected(i, glued_node_2) and i is not glued_node_1:
                node2 = i

        path = three_squares.find_shortest_path(node1, node2)

        edge_path = three_squares.convert_to_edge_path(path)
        expected_edge_path = []

        # only get the edges that are connected to the glued vertices and our start and end nodes
        for i in three_squares._nodes_list[EDGE_LATTICE_LAYER]:
            children = i.get_children()
            if glued_node_1 in children and node1 in children:
                expected_edge_path.append(i)
            if glued_node_1 in children and glued_node_2 in children:
                expected_edge_path.append(i)
            if glued_node_2 in children and node2 in children:
                expected_edge_path.append(i)

        self.assertCountEqual(expected_edge_path, edge_path)

    def test_convert_to_edge_path_four_squares(self):
        l1 = LatticeTest(4)
        l2 = LatticeTest(4)
        l3 = LatticeTest(4)
        l4 = LatticeTest(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l2._bot_node.get_parents()[0]
        n3 = l3._bot_node.get_parents()[0]
        n4 = l4._bot_node.get_parents()[0]

        two_squares = l1.glue_vertex(n1, l2, n2)
        glued_node = two_squares._testing_node_2
        
        next_node = two_squares._bot_node.get_parents()[0]
        if next_node is glued_node:
            next_node = two_squares._bot_node.get_parents()[1] # we DON'T want the newly glued node

        three_squares = two_squares.glue_vertex(next_node, l3, n3) #we now have three squares

        glued_node_1 = three_squares._testing_node_1
        glued_node_2 = three_squares._testing_node_2

        next_node = three_squares._bot_node.get_parents()[0]

        for i in three_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "5V10":
                next_node = i

        four_squares = three_squares.glue_vertex(next_node, l4, n4) # we now have FOUR SUQARES!! 3 + 1 = 7 - 3

        glued_node_1 = four_squares._testing_node_0
        glued_node_2 = four_squares._testing_node_1
        glued_node_3 = four_squares._testing_node_2

        for i in four_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "3V100":
                node1 = i

        for i in four_squares._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "4V1":
                node2 = i

        path = four_squares.find_shortest_path(node1, node2)

        edge_path = four_squares.convert_to_edge_path(path)
        expected_edge_path = []

        # print("edge path")
        # for i in edge_path:
        #     print(i)
        # print("expected edge path")
        # for i in expected_edge_path:
        #     print(i)
        #four_squares._geo_graph.show()

        expected_path_2 = ["3V100", "2V000", "5V100", "3V1", "4V1"]
        # only get the edges that are connected to the glued vertices and our start and end nodes
        for i in four_squares._nodes_list[EDGE_LATTICE_LAYER]:

            if i._label == "6E100":
                expected_edge_path.append(i)
            if i._label == "9E100":
                expected_edge_path.append(i)
            if i._label == "6E1":
                expected_edge_path.append(i)
            if i._label == "7E1":
                expected_edge_path.append(i)

        # print(expected_edge_path)
        # print(edge_path)
        self.assertCountEqual(expected_edge_path, edge_path)

#---------------------------- is connected --------------------------------------
    def test_is_connected_first_non_vertex(self):
        l1 = Lattice(3)
        v2 = l1._bot_node.get_parents()[0]
        with self.assertRaises(Exception):
            l1.is_connected(l1._bot_node, v2)
            
    def test_is_connected_second_non_vertex(self):
        l1 = Lattice(3)
        v1 = l1._bot_node.get_parents()[0]
        with self.assertRaises(Exception):
            l1.is_connected(v1, l1._bot_node)        

    def test_is_connected_both_non_vertex(self):
        l1 = Lattice(3)
        with self.assertRaises(Exception):
            l1.is_connected(l1._bot_node, l1._top_node)
    
    def test_is_connected_non_nodes(self):
        l1 = Lattice(3)
        with self.assertRaises(Exception):
            l1.is_connected("hi", "bye")

    def test_is_connected_true(self):
        l1 = Lattice(3)
        v1 = l1._bot_node.get_parents()[0]
        v2 = l1._bot_node.get_parents()[1]

        self.assertTrue(l1.is_connected(v1, v2))

    def test_is_connected_non_neighbors(self):
        l1 = Lattice(4)
        v1 = l1._bot_node.get_parents()[0]
        v2 = l1._bot_node.get_parents()[2]

        self.assertFalse(l1.is_connected(v1, v2))

#----------------------------------------get neighbors----------------------------
    def test_get_neighbors_triangle_first_vertex(self):
        l1 = Lattice(3)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        n3 = l1._bot_node.get_parents()[2]
        expected_neighbors = [n2, n3]

        found_neighbors = l1.get_neighbors(n1)

        self.assertTrue(set(expected_neighbors) == set(found_neighbors))

    def test_get_neighbors_triangle_second_vertex(self):
        l1 = Lattice(3)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        n3 = l1._bot_node.get_parents()[2]
        expected_neighbors = [n1, n3]

        found_neighbors = l1.get_neighbors(n2)

        self.assertTrue(set(expected_neighbors) == set(found_neighbors))

    def test_get_neighbors_triangle_third_vertex(self):
        l1 = Lattice(3)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        n3 = l1._bot_node.get_parents()[2]
        expected_neighbors = [n1, n2]

        found_neighbors = l1.get_neighbors(n3)

        self.assertTrue(set(expected_neighbors) == set(found_neighbors))

    def test_get_neighbors_are_vertices(self):
        l1 = Lattice(3)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        n3 = l1._bot_node.get_parents()[2]

        found_neighbors = l1.get_neighbors(n1)

        for i in found_neighbors:
            self.assertTrue(i._lattice_layer == VERTEX_LATTICE_LAYER)

    def test_get_neighbors_square(self):
        l1 = Lattice(4)
        n1 = l1._bot_node.get_parents()[0]
        n2 = l1._bot_node.get_parents()[1]
        n3 = l1._bot_node.get_parents()[2]
        expected_neighbors = [n2, n3]

        found_neighbors = l1.get_neighbors(n1)

        for i in found_neighbors:
            self.assertIn(i, l1._nodes_list[VERTEX_LATTICE_LAYER])

        self.assertEqual(len(found_neighbors), 2)

if __name__ == "__main__":
    unittest.main()
