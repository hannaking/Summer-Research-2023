from itertools import combinations
import sys
import networkx as nx

import unittest

sys.path.insert(0, './Summer-Research-2022/')

from negative_example_generator import NegativeExampleGen

class RandomFaceGraphCreatorTest(unittest.TestCase):
    
    '''
    
    generate tests
    
    '''

    def test_generate_creates(self):
        graphs = NegativeExampleGen.generate(10, False)

        self.assertEqual(type(graphs), list)
        self.assertEqual(len(graphs), 10)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)

    '''
    
    generate_original tests
    
    '''

    def test_generate_original_creates(self):
        graphs = NegativeExampleGen.generate_original(10, 10, False)

        self.assertEqual(type(graphs), list)
        self.assertEqual(len(graphs), 10)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)
            self.assertLessEqual(len(graph.nodes), 10)

    '''
    
    create_all_filtered_graphs tests
    
    '''

    def test_create_all_filtered_graphs_creates(self):
        gs = []
        total = 10

        graphs = NegativeExampleGen.create_all_filtered_graphs(gs, total)

        self.assertEqual(type(graphs), list)
        self.assertEqual(len(graphs), total)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)

    def test_create_all_filtered_graphs_not_in_filter(self):
        g = nx.MultiGraph()
        g.add_node('A')
        nx.set_node_attributes(g, {'A' : [10, 3]}, 'default')
        gs = [g]
        total = 16 # 1 less than the total number of 1 node graphs

        graphs = NegativeExampleGen.create_all_filtered_graphs(gs, total, 1)

        for graph in graphs:
            self.assertFalse(NegativeExampleGen.is_in(g, graphs))

    '''
    
    filter_graphs tests
    
    '''

    def test_filter_graphs_in(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g3 = g2.copy()

        gs1 = [g1, g2]
        gs2 = [g3]

        graphs = NegativeExampleGen.filter_graphs(gs1, gs2)

        self.assertEqual(graphs, [g1])

    def test_filter_graphs_not_in(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')
        
        gs1 = [g1, g2]
        gs2 = [g3]

        graphs = NegativeExampleGen.filter_graphs(gs1, gs2)

        self.assertEqual(graphs, gs1)

    '''
    
    split_evenly tests
    
    '''
    
    def test_split_evenly_one(self):
        total = 1
        splits = 10
        
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        results = NegativeExampleGen.split_evenly(total, splits)

        self.assertEqual(expected, results)

    def test_split_evenly_whole(self):
        total = 10
        splits = 10
        
        expected = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        results = NegativeExampleGen.split_evenly(total, splits)

        self.assertEqual(expected, results)

    def test_split_evenly_half(self):
        total = 5
        splits = 10
        
        expected = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        results = NegativeExampleGen.split_evenly(total, splits)

        self.assertEqual(expected, results)

    def test_split_evenly_double(self):
        total = 20
        splits = 10
        
        expected = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        results = NegativeExampleGen.split_evenly(total, splits)

        self.assertEqual(expected, results)

    def test_split_evenly_one_and_a_half(self):
        total = 15
        splits = 10
        
        expected = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
        results = NegativeExampleGen.split_evenly(total, splits)

        self.assertEqual(expected, results)

    '''
    
    generate_negatives_from_graph tests
    
    '''

    def test_generate_negatives_from_graph_creates(self):
        pos = nx.MultiGraph()
        pos.add_edge('A', 'B')
        nx.set_node_attributes(pos, {'A' : [23, 4], 'B' : [27, 4]}, 'default')
        total = 100
        negs = []
        count = 4

        graphs = NegativeExampleGen.generate_negatives_from_graph(pos, total, negs, count)

        self.assertEqual(type(graphs), list)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)

    def test_generate_negatives_from_graph_ends(self):
        pos = nx.MultiGraph()
        pos.add_node('A')
        nx.set_node_attributes(pos, {'A' : [40, 6]}, 'default')
        total = 100
        negs = []
        count = 4

        graphs = NegativeExampleGen.generate_negatives_from_graph(pos, total, negs, count)

        self.assertGreater(len(graphs), -1)
    
    def test_generate_negatives_from_graph_limits(self):
        pos = nx.MultiGraph()
        pos.add_edge('A', 'B')
        nx.set_node_attributes(pos, {'A' : [23, 4], 'B' : [27, 4]}, 'default')
        total = 1
        negs = []
        count = 4

        graphs = NegativeExampleGen.generate_negatives_from_graph(pos, total, negs, count)

        self.assertEqual(len(graphs), 1)

    def test_generate_negatives_from_graph_not_in_negs(self):
        pos = nx.MultiGraph()
        pos.add_edge('A', 'B')
        nx.set_node_attributes(pos, {'A' : [23, 4], 'B' : [27, 4]}, 'default')
        total = 100
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'B')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [13, 3]}, 'default')
        g2 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g2.add_node('C')
        nx.set_node_attributes(g2, {'A' : [30, 5], 'B' : [12, 3], 'C' : [0, 1]}, 'default')
        negs = [g1, g2]
        count = 10

        graphs = NegativeExampleGen.generate_negatives_from_graph(pos, total, negs.copy(), count)
        
        for graph in graphs[2:]:
            self.assertFalse(NegativeExampleGen.is_in(graph, negs))

    '''
    
    generate_random_isomorphic_graph tests
    
    '''

    def test_generate_random_isomorphic_graph_creates(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        nx.set_node_attributes(g, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')

        graph = NegativeExampleGen.generate_random_isomorphic_graph(g)

        self.assertEqual(type(graph), nx.MultiGraph)

    def test_generate_random_isomorphic_graph_is_iso(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        nx.set_node_attributes(g, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')

        graph = NegativeExampleGen.generate_random_isomorphic_graph(g)

        self.assertTrue(NegativeExampleGen.is_isomorphic(graph, g))

    '''
    
    random_shape_shift tests
    
    '''

    def test_random_shape_shift_creates(self):
        attribute = [0, 1]
        
        result = NegativeExampleGen.random_shape_shift(attribute)

        self.assertTrue(type(result), list)
        self.assertEqual(len(result), 2)
        for att in result:
            self.assertTrue(type(att), int)


    def test_random_shape_shift_triangle(self):
        attribute = [10, 3]
        
        result = NegativeExampleGen.random_shape_shift(attribute)

        self.assertTrue(result[1], 3)

    def test_random_shape_shift_pentagon(self):
        attribute = [30, 5]

        result = NegativeExampleGen.random_shape_shift(attribute)

        self.assertTrue(result, [30, 5])

    '''

    read_all_positive_graphs tests

    '''

    def test_read_all_positive_graphs_creates(self):
        graphs = NegativeExampleGen.read_all_positive_graphs()

        self.assertEqual(type(graphs), list)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)

    def test_read_all_positive_graphs_creates_no_iso(self):
        all_graphs = NegativeExampleGen.read_all_positive_graphs(True)
        graphs = NegativeExampleGen.read_all_positive_graphs()

        self.assertGreater(len(all_graphs), len(graphs))
        self.assertEqual(type(graphs), list)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)
        for g1, g2 in combinations(graphs, 2):
            self.assertTrue(not NegativeExampleGen.is_isomorphic(g1, g2))

    '''
    
    has_isomorphic_match tests
    
    '''

    def test_has_isomorphic_match_exact(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertTrue(NegativeExampleGen.has_isomorphic_match(g1, gs))

    def test_has_isomorphic_match_names(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [27, 4], 'F' : [13, 3]}, 'default')
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertTrue(NegativeExampleGen.has_isomorphic_match(g1, gs))

    def test_has_isomorphic_match_not(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertFalse(NegativeExampleGen.has_isomorphic_match(g1, gs))

    '''
    
    is_isomorphic tests
    
    '''

    def test_is_isomorphic_same_exact(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
    
        self.assertTrue(NegativeExampleGen.is_isomorphic(g1, g2))


    def test_is_isomorphic_same_different_names(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [27, 4], 'F' : [13, 3]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_same_different_names_all_same_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [23, 4], 'C' : [23, 4]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [23, 4], 'F' : [23, 4]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_same_swapped_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [27, 4], 'B' : [13, 3], 'C' : [23, 4]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_different_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [30, 5], 'B' : [40, 6], 'C' : [50, 7]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_different_shapes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [21, 4], 'B' : [22, 4], 'C' : [10, 3]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_different_sides(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [23, 5], 'B' : [27, 5], 'C' : [13, 5]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_isomorphic(g1, g2))

    def test_is_isomorphic_different_extra_point(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
        g2.add_node('D')
        nx.set_node_attributes(g2, {'D' : [30, 5]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_isomorphic(g1, g2))

    '''
    
    is_in tests
    
    '''

    def test_is_in_exact(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertTrue(NegativeExampleGen.is_in(g1, gs))

    def test_is_in_names(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [27, 4], 'F' : [13, 3]}, 'default')
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertTrue(NegativeExampleGen.is_in(g1, gs))

    def test_is_in_not(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [27, 4], 'F' : [13, 3]}, 'default')
        
        g3 = nx.MultiGraph()
        g3.add_edge('A', 'B')
        nx.set_node_attributes(g3, {'A' : [12, 3], 'B' : [10, 3]}, 'default')

        gs = [g2, g3]

        self.assertFalse(NegativeExampleGen.is_in(g1, gs))

    '''
    
    is_matching tests
    
    '''

    def test_is_matching_same_exact(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
    
        self.assertTrue(NegativeExampleGen.is_matching(g1, g2))


    def test_is_matching_same_different_names(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [27, 4], 'F' : [13, 3]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_same_different_names_all_same_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [23, 4], 'C' : [23, 4]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('D', 'E')
        g2.add_edge('D', 'F')
        g2.add_edge('E', 'F')
        nx.set_node_attributes(g2, {'D' : [23, 4], 'E' : [23, 4], 'F' : [23, 4]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_same_swapped_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [27, 4], 'B' : [13, 3], 'C' : [23, 4]}, 'default')
    
        self.assertTrue(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_different_attributes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [30, 5], 'B' : [40, 6], 'C' : [50, 7]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_different_shapes(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [21, 4], 'B' : [22, 4], 'C' : [10, 3]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_different_sides(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = nx.MultiGraph()
        g2.add_edge('A', 'B')
        g2.add_edge('A', 'C')
        g2.add_edge('B', 'C')
        nx.set_node_attributes(g2, {'A' : [23, 5], 'B' : [27, 5], 'C' : [13, 5]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_matching(g1, g2))

    def test_is_matching_different_extra_point(self):
        g1 = nx.MultiGraph()
        g1.add_edge('A', 'B')
        g1.add_edge('A', 'C')
        g1.add_edge('B', 'C')
        nx.set_node_attributes(g1, {'A' : [23, 4], 'B' : [27, 4], 'C' : [13, 3]}, 'default')
        
        g2 = g1.copy()
        g2.add_node('D')
        nx.set_node_attributes(g2, {'D' : [30, 5]}, 'default')
    
        self.assertFalse(NegativeExampleGen.is_matching(g1, g2))


if __name__ == '__main__':
    unittest.main()