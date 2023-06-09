# cleaned + commented 7/14

import unittest
import sys

sys.path.insert(0, './Summer-Research-2022/')

from node import Node

class TestNodes(unittest.TestCase):
#------------------------------flag and unflag tests-------------------------------------------
    # no change from base state (False)
    # flag
    # flag then unflag then reflag
    # unflag non-flagged
    # flag then unflag
    def test_flag_baseline(self):
        node = Node(1)
        self.assertFalse(node._flagged)
    
    def test_flag(self):
        node = Node(1)
        self.assertFalse(node._flagged)
        node.flag()
        self.assertTrue(node._flagged)

    def test_flag_after_unflag(self):
        node = Node(1)
        self.assertFalse(node._flagged)
        node.flag()
        self.assertTrue(node._flagged)
        node.unflag()
        self.assertFalse(node._flagged)
        node.flag()
        self.assertTrue(node._flagged)

    def test_unflag_no_change_to_flag_before(self):
        node = Node(1)
        self.assertFalse(node._flagged)
        node.unflag()
        self.assertFalse(node._flagged)

    def test_unflag_after_flag(self):
        node = Node(1)
        self.assertFalse(node._flagged)
        node.flag()
        self.assertTrue(node._flagged)
        node.unflag()
        self.assertFalse(node._flagged)

#-------------------------------------add child tests------------------------------------------
    # add child to empty child list
    # add same child twice
    # attempt to add non-Node
    def test_add_child(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_child(node2)
        self.assertTrue(len(node1.get_children()) == 1)
        self.assertEqual([node2], node1.get_children())

    def test_add_child_same_twice(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_child(node2)
        node1.add_child(node2)
        self.assertEqual(node1.get_children(), [node2])
        self.assertEqual([node2], node1.get_children())

    def test_add_child_not_node(self):
        node1 = Node(1)
        with self.assertRaises(Exception):
            node1.add_child(4)

#------------------------------------------add parent tests------------------------------------
    # add parent to empty parent list
    # add same parent twice
    # attempt to add non-Node
    def test_add_parent(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        self.assertTrue(len(node1.get_parents()) == 1)
        self.assertEqual([node2], node1.get_parents())

    def test_add_parent_same_twice(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        node1.add_parent(node2)
        self.assertEqual(node1.get_parents(), [node2])
        self.assertEqual([node2], node1.get_parents())

    def test_add_parent_not_a_node(self):
        node = Node(1)
        with self.assertRaises(Exception):
            node.add_parent("Hello")

#------------------------------------------get children----------------------------------------
    # get children of empty node
    # get children of node with one child
    # get children of node with two children
    # get the children of a Node whose children list has been set, not added to
    # get the children of a Node whose children list has been set, not added to, after it already had stuff in it
    # get the children of a Node whose children list has been set to empty
    # get the children of a Node whose children list has been set to empty, not added to, after it already had stuff in it
    def test_get_children_empty(self):
        node = Node(1)
        self.assertTrue(len(node.get_children()) == 0)
        self.assertEqual([], node.get_children())
    
    def test_get_children_added_one(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_child(node2)
        self.assertTrue(len(node1.get_children()) == 1)

    def test_get_children_added_another(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_child(node2)
        node3 = Node(1) 
        node1.add_child(node3)
        self.assertTrue(len(node1.get_children()) == 2)
    
    def test_get_children_after_set_to_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_children([node2])
        self.assertTrue(len(node.get_children()) == 1)
        self.assertEqual([node2], node.get_children())

    def test_get_children_after_set_to_list_some_already_in(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_child(node2)
        node3 = Node(1) 
        node1.add_child(node3)
        self.assertTrue(len(node1.get_children()) == 2)
        node1.set_children([node2])
        self.assertTrue(len(node1.get_children()) == 1)
        self.assertEqual([node2], node1.get_children())

    def test_get_children_after_set_to_empty_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_children([])
        self.assertTrue(len(node.get_children()) == 0)
        self.assertEqual([], node.get_children())

    def test_get_children_after_set_to_empty_list_some_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.add_child(node2)
        node.set_children([])
        self.assertTrue(len(node.get_children()) == 0)
        self.assertEqual([], node.get_children())
        
#------------------------------------------get parents-----------------------------------------
    # get parents of empty node
    # get parents of node with one parent
    # get parents of node with two parents
    # get the parents of a Node whose parents list has been set, not added to
    # get the parents of a Node whose parents list has been set, not added to, after it already had stuff in it
    # get the parents of a Node whose parents list has been set to empty
    # get the parents of a Node whose parents list has been set to empty, not added to, after it already had stuff in it
    def test_get_parents_empty(self):
        node = Node(1)
        self.assertTrue(len(node.get_parents()) == 0)

    def test_get_parents_added_one(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        self.assertTrue(len(node1.get_parents()) == 1)

    def test_get_parents_added_another(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        node3 = Node(1) 
        node1.add_parent(node3)
        self.assertTrue(len(node1.get_parents()) == 2)

    def test_get_parents_after_set_to_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_parents([node2])
        self.assertTrue(len(node.get_parents()) == 1)
        self.assertEqual([node2], node.get_parents())

    def test_get_parents_after_set_to_list_some_already_in(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        node3 = Node(1) 
        node1.add_parent(node3)
        self.assertTrue(len(node1.get_parents()) == 2)
        node1.set_parents([node2])
        self.assertTrue(len(node1.get_parents()) == 1)
        self.assertEqual([node2], node1.get_parents())

    def test_get_parents_after_set_to_empty_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_parents([])
        self.assertTrue(len(node.get_parents()) == 0)
        self.assertEqual([], node.get_parents())

    def test_get_parents_after_set_to_empty_list_some_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.add_parent(node2)
        node.set_parents([])
        self.assertTrue(len(node.get_parents()) == 0)
        self.assertEqual([], node.get_parents())

#-------------------------------------------set children---------------------------------------
    # set to list no children already
    # set to list some children already
    # set to empty list no children already
    # set to empty list some children already
    def test_set_children_to_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_children([node2])
        self.assertTrue(len(node.get_children()) == 1)
        self.assertEqual([node2], node.get_children())

    def test_set_children_to_list_some_already_in(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        node3 = Node(1) 
        node1.add_parent(node3)
        node1.set_children([node2])
        self.assertTrue(len(node1.get_children()) == 1)
        self.assertEqual([node2], node1.get_children())

    def test_set_children_to_empty_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_children([])
        self.assertTrue(len(node.get_children()) == 0)
        self.assertEqual([], node.get_children())

    def test_set_children_to_empty_list_some_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.add_parent(node2)
        node.set_children([])
        self.assertTrue(len(node.get_children()) == 0)
        self.assertEqual([], node.get_children())
        
#------------------------------------------set parents-----------------------------------------
    # set to list no parents already
    # set to list some parents already
    # set to empty list no parents already
    # set to empty list some parents already
    def test_set_parents_to_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_parents([node2])
        self.assertTrue(len(node.get_parents()) == 1)
        self.assertEqual([node2], node.get_parents())

    def test_set_parents_to_list_some_already_in(self):
        node1 = Node(1)
        node2 = Node(1) 
        node1.add_parent(node2)
        node3 = Node(1) 
        node1.add_parent(node3)
        node1.set_parents([node2])
        self.assertTrue(len(node1.get_parents()) == 1)
        self.assertEqual([node2], node1.get_parents())

    def test_set_parents_to_empty_list_none_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.set_parents([])
        self.assertTrue(len(node.get_parents()) == 0)
        self.assertEqual([], node.get_parents())

    def test_set_parents_to_empty_list_some_already_in(self):
        node = Node(1)
        node2 = Node(1)
        node.add_parent(node2)
        node.set_parents([])
        self.assertTrue(len(node.get_parents()) == 0)
        self.assertEqual([], node.get_parents())

#-------------------------------------------lattice_layer--------------------------------------
    # init with a valid layer
    # init with non-number layer
    # init with out-of-range layer
    # init with non-int layer
    def test_set_lattice_layer(self):
        node = Node(1)  # will call set_lattice_layer
        self.assertEqual(node.get_lattice_layer(), 1)

    def test_set_lattice_layer_not_a_num(self):
        with self.assertRaises(Exception):
            node = Node("h")

    def test_set_lattice_layer_not_between_0_and_4(self):       
        with self.assertRaises(Exception):
            node = Node(5)
    
    def test_set_lattice_layer_non_int(self):
        with self.assertRaises(Exception):
            node = Node(1.4)

#--------------------------------------------------exists in children-----------------------------------
    # no children
    # is in children (normal)
    # not in children
    # not a Node
    def test_exists_in_children_no_children(self):
        node = Node(2)
        node2 = Node(4)
        self.assertFalse(node._exists_in_children(node2))

    def test_exists_in_children_true(self):
        node = Node(2)
        node2 = Node(3)
        node3 = Node(3)
        node.set_children([node2, node3])
        self.assertTrue(node._exists_in_children(node3))
        
    def test_exists_in_children_false(self):
        node = Node(2)
        node2 = Node(4)
        node.set_children([Node(3), Node(3)])
        self.assertFalse(node._exists_in_children(node2))
    
    def test_exists_in_children_not_node(self):
        node = Node(2)
        with self.assertRaises(Exception):
            node._exists_in_children(5)

#--------------------------------------------------exists in parents-----------------------------------
    # no parents
    # is in parents (normal)
    # not in parents
    # not a Node
    def test_exists_in_parents_no_parents(self):
        node = Node(2)
        node2 = Node(4)
        self.assertFalse(node._exists_in_parents(node2))

    def test_exists_in_parents_true(self):
        node = Node(3)
        node2 = Node(2)
        node3 = Node(2)
        node.set_parents([node2, node3])
        self.assertTrue(node._exists_in_parents(node3))
         
    def test_exists_in_parents_false(self):
        node = Node(3)
        node2 = Node(4)
        node.set_parents([Node(2), Node(2)])
        self.assertFalse(node._exists_in_parents(node2))

    def test_exists_in_parents_not_node(self):
        node = Node(2)
        with self.assertRaises(Exception):
            node._exists_in_parents('l')

#-------------------------------------------disown child---------------------------------------------
    # not a Node
    # not in children
    # is in children (normal)
    def test_disown_child_not_a_node(self):
        node = Node(3)
        node.set_children([Node(4), Node(2)])
        with self.assertRaises(Exception):
            node.disown_child("hello")

    def test_disown_child_not_a_child(self):
        node = Node(3)
        node.set_children([Node(4), Node(2)])
        other_node = Node(0)
        node.disown_child(other_node)
        self.assertEqual(len(node.get_children()), 2)

    def test_disown_child_in(self):
        node1 = Node(0)
        node2 = Node(1) 
        node3 = Node(1) 
        node1.add_child(node2)
        node1.add_child(node3)
        node1.disown_child(node2)
        self.assertTrue(len(node1.get_children()) == 1)
        self.assertEqual([node3], node1.get_children())

#-------------------------------------------disown parents---------------------------------------------
    # not a Node
    # not in parents
    # is in parents (normal)
    def test_disown_parent_not_a_node(self):
        node = Node(3)
        node.set_parents([Node(4), Node(2)])
        with self.assertRaises(Exception):
            node.disown_parent("hello")

    def test_disown_parent_not_a_parent(self):
        node = Node(3)
        node.set_parents([Node(4), Node(2)])
        other_node = Node(0)
        node.disown_parent(other_node)
        self.assertEqual(len(node.get_parents()), 2)

    def test_disown_parent_in(self):
        node1 = Node(0)
        node2 = Node(1) 
        node3 = Node(1) 
        node1.add_parent(node2)
        node1.add_parent(node3)
        node1.disown_parent(node2)
        self.assertTrue(len(node1.get_parents()) == 1)
        self.assertEqual([node3], node1.get_parents())

#--------------------------------get parents and children-------------------------------------------------
    # no parents or children
    # parents empty
    # children empty
    # normal (children and parents present) 
    def test_get_parents_and_children_both_empty(self):
        node = Node(1)
        self.assertEqual([], node.get_parents_and_children())

    def test_get_parents_and_children_parents_children_only(self):
        node1 = Node(1)
        node2 = Node(0)
        node1.add_child(node2)
        self.assertEqual([node2], node1.get_parents_and_children())

    def test_get_parents_and_children_children_parents_only(self):
        node1 = Node(1)
        node2 = Node(0)
        node1.add_parent(node2)
        self.assertEqual([node2], node1.get_parents_and_children())

    def test_get_parents_and_children_both_nonempty(self):
        node1 = Node(2)
        node2 = Node(1)
        node3 = Node(0)
        node1.add_child(node3)
        node1.add_parent(node2)
        self.assertEqual([node2, node3], node1.get_parents_and_children())

if __name__ == "__main__":
    unittest.main()