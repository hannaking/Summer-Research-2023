

from lattice import Lattice
from node import Node

import itertools as its
import networkx  as nx

SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2

SEGMENT_TYPES = ["Segment"]
TRIANGLE_TYPES = ["IsoscelesRight", "Right", "Equilateral", "Isosceles"]
QUADRALATERAL_TYPES = ["Square", "Rectangle", "Rhombus", "Parallelogram", "Kite", "RightTrapezoid", "IsoscelesTrapezoid" "Dart"]

class FaceGraphGenerator:
    """
    The Face Graph Generator class creates a Graph representation of a lattice.  Each point is the face of a shape and is labeled
    with the type of shape it is.  Each segment represent a vertex glue between tw
    
    """
    def __init__(self, lattice=None):
        # to store networkX graphs you will generate
        self.graphs = []

        # get the sizes of the shapes (number of edges per shape)
        sizes = []
        for node in lattice.get_nodes(SHAPE_LATTICE_LAYER):
            sizes.append(len(node.get_children()))        

        # get every combination of shape types
        combo_shapes = []
        for size in sizes:
            if size == 1:
                combo_shapes.append(SEGMENT_TYPES)
            if size == 3:
                combo_shapes.append(TRIANGLE_TYPES)
            if size == 4:
                combo_shapes.append(QUADRALATERAL_TYPES)

        # for every combination of shapes
        for combo in list(its.product(*combo_shapes)):
            # add the newly created graphs
            self.graphs.append(self.build(lattice, sizes, combo))

    def build(self, lattice, sizes, types):
        graph = nx.Graph()
        for i in range(0, len(lattice.get_nodes(SHAPE_LATTICE_LAYER))):
            graph.add_node(i, type=types[i], size=sizes[i])
        
        for edge in lattice.get_nodes(EDGE_LATTICE_LAYER):
            if len(edge.get_parents()) == 2:
                graph.add_edge(lattice.get_nodes(SHAPE_LATTICE_LAYER).index(edge.get_parents()[0]),
                               lattice.get_nodes(SHAPE_LATTICE_LAYER).index(edge.get_parents()[1]))

        nx.draw(graph)
        return graph