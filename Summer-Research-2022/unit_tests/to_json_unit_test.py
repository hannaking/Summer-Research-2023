import sys
import networkx as nx

import unittest

sys.path.insert(0, './Summer-Research-2022/')

from to_json import ToJson

class ToJsonTest(unittest.TestCase):

    '''
    
    helper functions

    '''

    def create_one_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4]},
                                   'default')
        return g
    
    def create_many_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('A', 'D')
        g.add_edge('B', 'C')
        g.add_edge('B', 'D')
        g.add_edge('C', 'D')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4],
                                   'C' : [13, 3],
                                   'D' : [30, 5]},
                                   'default')
        return g

    def create_multiedge_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4],
                                   'C' : [13, 3]},
                                   'default')
        return g

    def create_multiple_multiedges_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'B')
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        g.add_edge('B', 'C')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4],
                                   'C' : [13, 3]},
                                   'default')
        return g

    def create_edgeless_graph(self):
        g = nx.MultiGraph()
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4],
                                   'C' : [13, 3]},
                                   'default')
        return g

    def create_empty_graph(self):
        g = nx.MultiGraph()
        return g

    def create_extra_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_node('C')
        g.add_node('D')
        nx.set_node_attributes(g, {'A' : [23, 4],
                                   'B' : [27, 4],
                                   'C' : [13, 3],
                                   'D' : [30, 5]},
                                   'default')
        return g

    """
    
    one edge tests
    
    """
    
    def test_from_networkx_one(self):
        g = self.create_one_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        }\
\n    ],\
\n    \"edges\": [\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"B\",\
\n            \"count\": 1\
\n        }\
\n    ]\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)
        
    def test_get_nodes_one(self):
        g = self.create_one_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)
    
    def test_get_edges_one(self):
        g = self.create_one_graph()
        expected = [{"point 1" : "A", "point 2": "B", "count": 1}]
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_one(self):
        g = self.create_one_graph()
        expected = {('A', 'B') : 1}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)

    '''
    
    many edges tests
    
    '''

    def test_from_networkx_many(self):
        g = self.create_many_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"C\",\
\n            \"shape\": \"Isosceles Triangle\",\
\n            \"sides\": 3\
\n        },\
\n        {\
\n            \"ID\": \"D\",\
\n            \"shape\": \"Regular Pentagon\",\
\n            \"sides\": 5\
\n        }\
\n    ],\
\n    \"edges\": [\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"B\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"D\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"B\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"B\",\
\n            \"point 2\": \"D\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"C\",\
\n            \"point 2\": \"D\",\
\n            \"count\": 1\
\n        }\
\n    ]\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_many(self):
        g = self.create_many_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4},
                    {"ID" : "C", "shape" : "Isosceles Triangle", "sides" : 3},
                    {"ID" : "D", "shape" : "Regular Pentagon", "sides" : 5}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_many(self):
        g = self.create_many_graph()
        expected = [{"point 1" : "A", "point 2": "B", "count": 1},
                    {"point 1" : "A", "point 2": "C", "count": 1},
                    {"point 1" : "A", "point 2": "D", "count": 1},
                    {"point 1" : "B", "point 2": "C", "count": 1},
                    {"point 1" : "B", "point 2": "D", "count": 1},
                    {"point 1" : "C", "point 2": "D", "count": 1}]
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_many(self):
        g = self.create_many_graph()
        expected = {('A', 'B') : 1, ('A', 'C') : 1, ('A', 'D') : 1,
                    ('B', 'C') : 1, ('B', 'D') : 1, ('C', 'D') : 1}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)
    
    '''
    
    multiedge tests
    
    '''

    def test_from_networkx_multiedge(self):
        g = self.create_multiedge_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"C\",\
\n            \"shape\": \"Isosceles Triangle\",\
\n            \"sides\": 3\
\n        }\
\n    ],\
\n    \"edges\": [\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"B\",\
\n            \"count\": 2\
\n        },\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"B\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 1\
\n        }\
\n    ]\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_multiedge(self):
        g = self.create_multiedge_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4},
                    {"ID" : "C", "shape" : "Isosceles Triangle", "sides" : 3}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_multiedge(self):
        g = self.create_multiedge_graph()
        expected = [{"point 1" : "A", "point 2": "B", "count": 2},
                    {"point 1" : "A", "point 2": "C", "count": 1},
                    {"point 1" : "B", "point 2": "C", "count": 1}]
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_multiedge(self):
        g = self.create_multiedge_graph()
        expected = {('A','B') : 2, ('A','C') : 1, ('B','C') : 1}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)
    
    '''
    
    multiple multiedges tests
    
    '''

    def test_from_networkx_multiple_multiedges(self):
        g = self.create_multiple_multiedges_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"C\",\
\n            \"shape\": \"Isosceles Triangle\",\
\n            \"sides\": 3\
\n        }\
\n    ],\
\n    \"edges\": [\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"B\",\
\n            \"count\": 3\
\n        },\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 1\
\n        },\
\n        {\
\n            \"point 1\": \"B\",\
\n            \"point 2\": \"C\",\
\n            \"count\": 2\
\n        }\
\n    ]\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_multiple_multiedges(self):
        g = self.create_multiple_multiedges_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4},
                    {"ID" : "C", "shape" : "Isosceles Triangle", "sides" : 3}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_multiple_multiedges(self):
        g = self.create_multiple_multiedges_graph()
        expected = [{"point 1" : "A", "point 2": "B", "count": 3},
                    {"point 1" : "A", "point 2": "C", "count": 1},
                    {"point 1" : "B", "point 2": "C", "count": 2}]
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_multiple_multiedges(self):
        g = self.create_multiple_multiedges_graph()
        expected = {('A', 'B') : 3, ('A','C') : 1, ('B', 'C') : 2}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)
    
    '''
    
    edgeless tests
    
    '''

    def test_from_networkx_edgeless(self):
        g = self.create_edgeless_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"C\",\
\n            \"shape\": \"Isosceles Triangle\",\
\n            \"sides\": 3\
\n        }\
\n    ],\
\n    \"edges\": []\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_edgeless(self):
        g = self.create_edgeless_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4},
                    {"ID" : "C", "shape" : "Isosceles Triangle", "sides" : 3}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_edgeless(self):
        g = self.create_edgeless_graph()
        expected = []
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_edgeless(self):
        g= self.create_edgeless_graph()
        expected = {}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)

    '''
    
    empty graph tests
    
    '''

    def test_from_networkx_empty(self):
        g = self.create_empty_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [],\
\n    \"edges\": []\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_empty(self):
        g = self.create_empty_graph()
        expected = []
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_empty(self):
        g = self.create_empty_graph()
        expected = []
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_empty(self):
        g = self.create_empty_graph()
        expected = {}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)

    '''
    
    extra nodes tests
    
    '''

    def test_from_networkx_extra(self):
        g = self.create_extra_graph()
        expected = \
 "{\
\n    \"source\": \"Test\",\
\n    \"textbook\": [false],\
\n    \"nodes\": [\
\n        {\
\n            \"ID\": \"A\",\
\n            \"shape\": \"Parallelogram\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"B\",\
\n            \"shape\": \"Dart\",\
\n            \"sides\": 4\
\n        },\
\n        {\
\n            \"ID\": \"C\",\
\n            \"shape\": \"Isosceles Triangle\",\
\n            \"sides\": 3\
\n        },\
\n        {\
\n            \"ID\": \"D\",\
\n            \"shape\": \"Regular Pentagon\",\
\n            \"sides\": 5\
\n        }\
\n    ],\
\n    \"edges\": [\
\n        {\
\n            \"point 1\": \"A\",\
\n            \"point 2\": \"B\",\
\n            \"count\": 1\
\n        }\
\n    ]\
\n}"
        self.maxDiff = None
        json_data = ToJson.from_networkx(g, 'default', 'Test', False)
        self.assertEqual(expected, json_data)

    def test_get_nodes_extra(self):
        g = self.create_extra_graph()
        expected = [{"ID" : "A", "shape" : "Parallelogram", "sides" : 4},
                    {"ID" : "B", "shape" : "Dart", "sides" : 4},
                    {"ID" : "C", "shape" : "Isosceles Triangle", "sides" : 3},
                    {"ID" : "D", "shape" : "Regular Pentagon", "sides" : 5}]
        nodes = ToJson._get_nodes(g, 'default')

        self.assertEqual(expected, nodes)

    def test_get_edges_extra(self):
        g = self.create_extra_graph()
        expected = [{"point 1" : "A", "point 2": "B", "count": 1}]
        edges = ToJson._get_edges(g)

        self.assertEqual(expected, edges)

    def test_get_edge_quantities_extra(self):
        g = self.create_extra_graph()
        expected = {('A', 'B') : 1}
        quantities = ToJson._get_edge_quantities(g)

        self.assertEqual(quantities, expected)


if __name__ == '__main__':
    unittest.main()