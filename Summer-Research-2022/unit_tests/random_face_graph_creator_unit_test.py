import sys
import networkx as nx

import unittest

sys.path.insert(0, './Summer-Research-2022/')

from random_face_graph_creator import RandomFaceGraphCreator

class RandomFaceGraphCreatorTest(unittest.TestCase):
    
    '''
    
    _create_random_face_graphs test

    '''

    def test_create_random_face_graphs_creates(self):
        graphs = RandomFaceGraphCreator.create_random_face_graphs(10)

        self.assertEqual(type(graphs), list)
        self.assertEqual(len(graphs), 10)
        for graph in graphs:
            self.assertEqual(type(graph), nx.MultiGraph)

    '''
    
    _create_random_face_graph tests

    '''

    def test_create_random_face_graph_creates(self):
        graph = RandomFaceGraphCreator.create_random_face_graph()

        self.assertEqual(type(graph), nx.MultiGraph)

    '''
    
    _create_all_nodes tests
    
    '''

    def test_create_all_nodes_creates(self):
        nodes = RandomFaceGraphCreator._create_all_nodes()

        self.assertEqual(type(nodes), dict)
        for point, attrs in nodes.items():
            self.assertEqual(type(point), str)
            self.assertEqual(type(attrs), list)
            self.assertEqual(len(attrs), 2)
            for attr in attrs:
                self.assertEqual(type(attr), int)
        self.assertNotEqual(nodes, {})

    def test_create_all_nodes_1_node(self):
        nodes = RandomFaceGraphCreator._create_all_nodes(1)

        self.assertEqual(len(nodes), 2)
    
    def test_create_all_nodes_no_skips(self):
        nodes = RandomFaceGraphCreator._create_all_nodes()
        name = 'A'

        for i, node in enumerate(nodes):
            if i < len(nodes) - 1:
                self.assertEqual(node, name)
                name = chr(ord(name) + 1)
            else:
                self.assertEqual(node, 'Universe')

    '''

    _create_all_edges tests

    '''

    def test_create_all_edges_creates(self):
        nodes = {'A' : [10, 3], 'B' : [10, 3], 'C' : [10, 3], 'D' : [10, 3], 'E' : [10, 3], 'Universe' : [-1, -1]}
        
        edges = RandomFaceGraphCreator._create_all_edges(nodes)

        self.assertEqual(type(edges), list)
        for edge in edges:
            self.assertEqual(type(edge), list)
            self.assertEqual(len(edge), 2)
            for point in edge:
                self.assertEqual(type(point), str)

    def test_create_all_edges_1_node(self):
        nodes = {'A' : [10, 3], 'Universe' : [-1, -1]}

        expected = [['A', 'Universe'], ['A', 'Universe'], ['A', 'Universe']]
        edges = RandomFaceGraphCreator._create_all_edges(nodes)
        
        self.assertEqual(expected, edges)

    def test_create_all_edges_5_nodes(self):
        nodes = {'A' : [10, 3], 'B' : [10, 3], 'C' : [10, 3], 'D' : [10, 3], 'E' : [10, 3], 'Universe' : [-1, -1]}
        
        edges = RandomFaceGraphCreator._create_all_edges(nodes)
        
        self.assertTrue(len(edges) >= 9 and len(edges) <= 15)

    def test_create_all_edges_with_segment(self):
        nodes = {'A' : [00, 1], 'B' : [10, 3], 'C' : [10, 3], 'D' : [10, 3], 'E' : [10, 3], 'Universe' : [-1, -1]}
        
        edges = RandomFaceGraphCreator._create_all_edges(nodes)
        
        self.assertTrue(len(edges) >= 8 and len(edges) <= 12)

    def test_create_all_edges_all_segments(self):
        nodes = {'A' : [00, 1], 'B' : [00, 1], 'C' : [00, 1], 'D' : [00, 1], 'E' : [00, 1], 'Universe' : [-1, -1]}
        
        expected = []
        edges = RandomFaceGraphCreator._create_all_edges(nodes)
        
        self.assertEqual(expected, edges)

    '''
    
    _get_other_points tests

    '''

    def test_get_other_points_all_others(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}

        expected = ['B', 'C', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)


    def test_get_other_points_one_left(self):
        position = 3
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}

        expected = ['Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    def test_get_other_points_none_left(self):
        position = 4
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}

        expected = []
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    def test_get_other_points_one_full(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 4, 'D': 0, 'Universe' : 0}

        expected = ['B', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    def test_get_other_points_all_full(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 4, 'C' : 4, 'D': 4, 'Universe' : 999}

        expected = ['Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    def test_get_other_points_has_segment(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [00, 1], 'D': [20, 4], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}

        expected = ['B','D','Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    def test_get_other_points_has_segment(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [00, 1], 'C' : [00, 1], 'D': [00, 1], 'Universe' : [-1, -1]}
        counts = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}

        expected = ['Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, counts)

        self.assertEqual(expected, other_points)

    '''
    
    _is_valid_to_connect tests
    
    '''

    def test_is_valid_to_connect_allowed(self):
        size = 4
        count = 3

        self.assertTrue(RandomFaceGraphCreator._is_valid_to_connect(size, count))

    def test_is_valid_to_connect_line_segment(self):
        size = 1
        count = 0

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size, count))

    def test_is_valid_to_connect_universe(self):
        size = -1
        count = 99

        self.assertTrue(RandomFaceGraphCreator._is_valid_to_connect(size, count))

    def test_is_valid_to_connect_full(self):
        size = 4
        count = 4

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size, count))

if __name__ == '__main__':
    unittest.main()