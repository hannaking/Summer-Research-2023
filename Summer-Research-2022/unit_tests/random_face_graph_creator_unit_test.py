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
        node_degrees = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['B', 'C', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)


    def test_get_other_points_one_left(self):
        position = 3
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_none_left(self):
        position = 4
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = []
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_one_full(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 4, 'B' : 0, 'C' : 4, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 4, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['B', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_all_full(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 4, 'B' : 4, 'C' : 4, 'D': 4, 'Universe' : 12}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 4,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 4,
                        ('C', 'D') : 0, ('C', 'Universe') : 4,
                        ('D', 'Universe') : 4}

        expected = ['Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_has_segment(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [00, 1], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['B','D','Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_has_segments(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [00, 1], 'D': [00, 1], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 0, 'B' : 0, 'C' : 0, 'D': 0, 'Universe' : 0}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 0, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['B', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_over_edges_u(self):
        position = 0
        nodes = {'A' : [40, 6], 'B' : [20, 4], 'C' : [20, 4], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 5, 'B' : 1, 'C' : 3, 'D': 0, 'Universe' : 1}
        edge_degrees = {('A', 'B') : 1, ('A', 'C') : 3, ('A', 'D') : 0, ('A', 'Universe') : 1,
                        ('B', 'C') : 0, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 0,
                        ('D', 'Universe') : 0}

        expected = ['B', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    def test_get_other_points_over_edges_u(self):
        position = 0
        nodes = {'A' : [20, 4], 'B' : [20, 4], 'C' : [40, 5], 'D': [20, 4], 'Universe' : [-1, -1]}
        node_degrees = {'A' : 3, 'B' : 1, 'C' : 5, 'D': 0, 'Universe' : 1}
        edge_degrees = {('A', 'B') : 0, ('A', 'C') : 3, ('A', 'D') : 0, ('A', 'Universe') : 0,
                        ('B', 'C') : 1, ('B', 'D') : 0, ('B', 'Universe') : 0,
                        ('C', 'D') : 0, ('C', 'Universe') : 1,
                        ('D', 'Universe') : 0}

        expected = ['B', 'D', 'Universe']
        other_points = RandomFaceGraphCreator._get_other_points(position, nodes, node_degrees, edge_degrees)

        self.assertEqual(expected, other_points)

    '''
    
    _is_valid_to_connect tests
    
    '''

    def test_is_valid_to_connect_allowed(self):
        size_u = 4
        size_v = 4
        node_degree = 3
        edge_degree = 0

        self.assertTrue(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

    def test_is_valid_to_connect_line_segment(self):
        size_u = 1
        size_v = 1
        node_degree = 0
        edge_degree = 0

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

    def test_is_valid_to_connect_universe(self):
        size_u = 4
        size_v = -1
        node_degree = 99
        edge_degree = 0

        self.assertTrue(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

    def test_is_valid_to_connect_full(self):
        size_u = 4
        size_v = 4
        node_degree = 4
        edge_degree = 0

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

    def test_is_valid_to_connect_over_edge_u(self):
        size_u = 6
        size_v = 4
        node_degree = 0
        edge_degree = 3

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

    def test_is_valid_to_connect_over_edge_v(self):
        size_u = 4
        size_v = 6
        node_degree = 0
        edge_degree = 3

        self.assertFalse(RandomFaceGraphCreator._is_valid_to_connect(size_u, size_v, node_degree, edge_degree))

if __name__ == '__main__':
    unittest.main()