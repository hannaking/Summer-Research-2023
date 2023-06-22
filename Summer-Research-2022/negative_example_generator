import itertools
import os
import random as rand
from to_stellar_graph import ToStellarGraph
import networkx as nx
import networkx.algorithms.isomorphism as iso
import pandas as pd

class NegativeExampleGen():

    @staticmethod
    def generate():
        graphs = NegativeExampleGen.read_all_positive_graphs()
        print(graphs)
        #possible_negative_graphs = ()
        #for graph in graphs:
        #    possible_negative_graphs.append(NegativeExampleGen.generate_all_possible_for_graph(graph))

    def generate_all_possible_for_graph(graph:nx.MultiGraph) -> list[nx.MultiGraph]:
        pass

    def subtract_graphs_from_set(base_graphs:nx.MultiGraph, subtract_graphs:nx.MultiGraph):
        pass

    def read_all_positive_graphs():
        graphs = []

        directory = 'Summer-Research-2022/Json shapes'
        if os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith('.json'):
                        with open(os.path.join(dirpath, filename)) as f:
                            graph, label = ToStellarGraph.from_json(f.name)
                            graphs.append(graph.to_networkx())
        else:
            print("File does not exist.")
        return graphs
    
    def is_matching(graph1, graph2):
        GM = nx.isomorphism.GraphMatcher(graph1, graph2, node_match=lambda n1, n2:n1==n2)
        return GM.is_isomorphic()

NegativeExampleGen.generate()