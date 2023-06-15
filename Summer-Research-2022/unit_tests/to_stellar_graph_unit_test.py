import sys


import numpy as np
import pandas as pd
import networkx as nx
import stellargraph as sg

import unittest

sys.path.insert(0, './Summer-Research-2022/')

from to_stellar_graph import ToStellarGraph
from ToPandas import ToPandas

class TestToStellarGraph(unittest.TestCase):
    
    """

    no muti-edges
    
    """
    
    #
    # check for changing a graph from networkx to stellar graph
    #
    def test_from_networkx_simple(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'D')
        g.add_edge('B', 'C')
        g.add_edge('C', 'D')
        nx.set_node_attributes(g, {'A' : [13, 3],
                                   'B' : [13, 3],
                                   'C' : [13, 3],
                                   'D' : [13, 3]},
                                   'shape')

        graph = ToStellarGraph.from_networkx(g, 'shape')

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), g.nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), list(nx.get_node_attributes(g, 'shape').values())))
        self.assertTrue(np.array_equiv(graph.edges(), [(edge[0], edge[1]) for edge in g.edges]))
        self.assertTrue(np.array_equiv(graph.edge_features(), list(nx.get_edge_attributes(g, 'shape').values())))

    #
    # check for changing a multigraph from json to stellar graph
    #
    def test_from_json_simple(self):
        graph, label = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/TestShape.json')
        
        nodes = ['A', 'B', 'C', 'D']
        node_features = [[13, 3], [13, 3], [13, 3], [13, 3]]
        edges = [('A', 'B'), ('A', 'D'), ('B', 'C'), ('C', 'D')]
        edge_features = []
        c_label = pd.DataFrame([1])

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertEqual(type(label), pd.DataFrame)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))
        self.assertTrue(label.equals(c_label))

    #
    # check for changing a non-multigraph from pandas to stellar graph
    #
    def test_from_pandas_simple(self):
        nodes = pd.DataFrame({'shape' : [13, 13, 13, 13],
                              'sides' : [3,  3,  3,  3 ]},
                              index = ['A', 'B', 'C', 'D'])
        edges = pd.DataFrame({'source' : ["A", "A", "B", "C"],
                              'target' : ["B", "D", "C", "D"]})
        
        graph = ToStellarGraph._from_pandas(nodes, edges)

        nodes = ['A', 'B', 'C', 'D']
        node_features = [[13, 3], [13, 3], [13, 3], [13, 3]]
        edges = [('A', 'B'), ('A', 'D'), ('B', 'C'), ('C', 'D')]
        edge_features = []

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))
    
    """
    
    yes muti-edges
    
    """

    #
    # check for changing a multigraph from networkx to stellar graph
    #
    def test_from_networkx_multi(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'B')
        nx.set_node_attributes(g, {'A' : [24, 4],
                                   'B' : [27, 4]},
                                   'shape')

        graph = ToStellarGraph.from_networkx(g, 'shape')

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), g.nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), list(nx.get_node_attributes(g, 'shape').values())))
        self.assertTrue(np.array_equiv(graph.edges(), [(edge[0], edge[1]) for edge in g.edges]))
        self.assertTrue(np.array_equiv(graph.edge_features(), list(nx.get_edge_attributes(g, 'shape').values())))

    #
    # check for changing a multigraph from json to stellar graph
    #
    def test_from_json_multi(self):
        graph, label = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Quadrilaterals/KiteAndDart.json')
        
        nodes = ['A', 'B']
        node_features = [[24, 4], [27, 4]]
        edges = [('A', 'B'), ('A', 'B')]
        edge_features = []
        c_label = pd.DataFrame([1])

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertEqual(type(label), pd.DataFrame)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))
        self.assertTrue(label.equals(c_label))

    #
    # check for changing a multigraph from pandas to stellar graph
    #
    def test_from_pandas_multi(self):
        nodes = pd.DataFrame({'shape' : [24, 27],
                              'sides' : [4,  4 ]},
                              index = ['A', 'B'])
        edges = pd.DataFrame({'source' : ["A", "A"],
                              'target' : ["B", "B"]})
        
        graph = ToStellarGraph._from_pandas(nodes, edges)

        nodes = ['A', 'B']
        node_features = [[24, 4], [27, 4]]
        edges = [('A', 'B'), ('A', 'B')]
        edge_features = []
        
        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))

    """
    
    doesn't have edges
    
    """

    #
    # check for changing a graph without edges from networkx to stellar graph
    #
    def test_from_networkx_edgeless(self):
        g = nx.MultiGraph()
        g.add_node('A')
        g.add_node('B')
        nx.set_node_attributes(g, {'A' : [11, 3],
                                   'B' : [11, 3]},
                                   'shape')
        
        graph = ToStellarGraph.from_networkx(g, 'shape')
        
        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), g.nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), list(nx.get_node_attributes(g, 'shape').values())))
        self.assertTrue(np.array_equiv(graph.edges(), [(edge[0], edge[1]) for edge in g.edges]))
        self.assertTrue(np.array_equiv(graph.edge_features(), list(nx.get_edge_attributes(g, 'shape').values())))

    #
    # check for changing a graph without edges from json to stellar graph
    #
    def test_from_json_edgeless(self):
        graph, label = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Vertext_Triangles.json')
        
        nodes = ['A', 'B']
        node_features = [[11, 3], [11, 3]]
        edges = []
        edge_features = []
        c_label = pd.DataFrame([1])

        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertEqual(type(label), pd.DataFrame)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))
        self.assertTrue(label.equals(c_label))

    #
    # check for changing a graph without edges from pandas to stellar graph
    #
    def test_from_pandas_edgeless(self):
        nodes = pd.DataFrame({'shape' : [11, 11],
                              'sides' : [3,  3 ]},
                              index = ['A', 'B'])
        edges = pd.DataFrame({'source' : [],
                              'target' : []})
        
        graph = ToStellarGraph._from_pandas(nodes, edges)

        nodes = ['A', 'B']
        node_features = [[11, 3], [11, 3]]
        edges = []
        edge_features = []
        
        self.assertEqual(type(graph), sg.StellarGraph)
        self.assertTrue(np.array_equiv(graph.nodes(), nodes))
        self.assertTrue(np.array_equiv(graph.node_features(), node_features))
        self.assertTrue(np.array_equiv(graph.edges(), edges))
        self.assertTrue(np.array_equiv(graph.edge_features(), edge_features))

    



if __name__ == '__main__':
    unittest.main()