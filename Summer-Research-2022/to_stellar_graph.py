# Converts a networkx graph, a pandas dataframe or a json file into a stellar graph.
#
# Supports features and multigraphs.

import pandas as pd
import networkx as nx
import stellargraph as sg

from stellargraph import StellarGraph
from ToPandas import ToPandas

class ToStellarGraph():

    # converts a networkx graphs with features into a corresponding stellar graph
    #
    # graph - the full networkx graph including features
    # features - the name of the features included in the networkx graph
    #
    # returns the corrisponding stellar graph
    @classmethod
    def from_networkx(self, graph:(nx.MultiGraph | nx.Graph), features:str) -> sg.StellarGraph:
        if not bool(graph.edges):
            nodes = pd.DataFrame(nx.get_node_attributes(graph, features)).transpose()
            edges = nx.to_pandas_edgelist(graph)
            return ToStellarGraph._from_pandas(nodes, edges)
        return StellarGraph.from_networkx(graph, node_features=features)

    # converts a properly formatted JSON file into a corresponding stellar graph
    #
    # jsonFile - the relative path from the project head to the JSON file
    #
    # returns the corrisponding stellar graph
    @classmethod
    def from_json(self, jsonFile:str):
        label, edges, nodes = ToPandas.ToPanda(jsonFile)
        return ToStellarGraph._from_pandas(nodes, edges), label
    
    # converts a pandas dataframe with node and edge data into a corresponding stellar graph
    #
    # nodes - the node data including names and features
    # edges - the edge data indicating connections between nodes
    #
    # returns the corrisponding stellar graph
    @classmethod
    def _from_pandas(self, nodes:pd.DataFrame, edges:pd.DataFrame):
        return sg.StellarGraph(nodes, edges)