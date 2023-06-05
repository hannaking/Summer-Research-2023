# Parses a lattice object into a networkx graph. The new graph is used to visualize the geometry figure structured by the lattice.
#
# attributes:
#   - _lattice        : the Lattice object this GeometryGraph is based on
#   - _geometry_graph : the networkx MultiGraph object
#
# functions:
#   - build graph
#   - nodes
#   - show
#   - get graph
#   - number of nodes
#   - number of edge
#   - get perimeter

from distutils.command.build import build
from platform import node
import networkx as nx
import matplotlib.pyplot as plt

from node    import Node

#@---------------------@#
#@----- Constants -----@#
#@---------------------@#

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class GeometryGraph:
    def __init__(self, lattice):

        self._lattice = lattice
        self._geometry_graph = nx.MultiGraph()
        # MultiGraph - An undirected graph class that can store multiedges (multiple edges between two nodes).
        #              Holds undirected edges. Self loops are allowed.

        self._build_graph()

    # make the nx graph for display
    # loop through edge nodes and make edge (on networkx graph) between edge node's children
    #
    # no return
    def _build_graph(self):
        # get the edges from the lattice
        edges = self._lattice._nodes_list[EDGE_LATTICE_LAYER]
        
        
        for edge in edges:
            # each edge can only have two vertex children, so it's fine to hard-code 0 and 1
            child_0 = edge.get_children()[0]
            child_1 = edge.get_children()[1]

            # if you add an nx edge using an nx node that doesn't exist, it is created
            self._geometry_graph.add_edge(child_0, child_1)

    # returns an iterator over the graph nodes
    def nodes(self):
        return self._geometry_graph.nodes()

    # displays the figure
    # labels matching the node labels will display for vertices and edges
    # the graph is drawn with a spring layout
    #
    # no return
    def show(self):
        pos = nx.spring_layout(self._geometry_graph)
        nx.draw(self._geometry_graph, with_labels=True, pos=pos, node_color='pink', alpha=0.9)

        # make edge label dictionary
        edge_labels = {}

        for edge in self._lattice._nodes_list[EDGE_LATTICE_LAYER]:
            key = (edge.get_children()[0], edge.get_children()[1])
            edge_labels[key] = edge._label

        nx.draw_networkx_edge_labels(self._geometry_graph, pos, edge_labels=edge_labels, font_color='red')
        plt.show()

    # returns network x graph object of figure
    def get_graph(self):
        return self._geometry_graph

    # returns the number of nodes in the graph
    def number_of_nodes(self):
        return self._geometry_graph.number_of_nodes()

    # returns the number of edges in the graph
    def number_of_edges(self):
        return self._geometry_graph.number_of_edges()

    # get a nx graph of the exterior edges only of a figure
    # peerimeter is a seperate graph to prevent loss of information from original figure graph
    # an edge is a perimeter edge if it is only a part of one shape
    #
    # returns nx graph of perimeter of the figure
    def get_perimeter(self):
        perimeter_graph = nx.Graph()

        # make sure vertices are built first
        edges = self._lattice._nodes_list[EDGE_LATTICE_LAYER]
        
        
        for edge in edges:
            
            if self._lattice.edge_glued(edge):
                continue

            #each edge has only two children, so it's fine to hard-code 0 and 1    
            child_0 = edge.get_children()[0]
            child_1 = edge.get_children()[1]

            perimeter_graph.add_edge(child_0, child_1)

        return perimeter_graph