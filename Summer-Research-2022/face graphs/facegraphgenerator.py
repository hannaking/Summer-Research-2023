

from lattice import Lattice
from node import Node

import itertools as its
import networkx  as nx

SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2

SEGMENT_TYPES       = ["Segment"]
TRIANGLE_TYPES      = ["IsoscelesRight", "Right", "Equilateral", "Isosceles"]
QUADRALATERAL_TYPES = ["Square", "Rectangle", "Rhombus", "Parallelogram", "Kite", "RightTrapezoid", "IsoscelesTrapezoid" "Dart"]
PENTAGON_TYPES      = ["RegularPentagon"]
HEXAGON_TYPES       = ["RegularHexagon"]
SEPTAGON_TYPES      = ["RegularSeptagon"]
OCTOGON_TYPES       = ["RegularOctogon"]

SIDES_SHAPE_MAP = {1: SEGMENT_TYPES,  3: TRIANGLE_TYPES, 4: QUADRALATERAL_TYPES,
                  5: PENTAGON_TYPES, 6: HEXAGON_TYPES,  7: SEPTAGON_TYPES, 8: OCTOGON_TYPES}

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
            combo_shapes.append(SIDES_SHAPE_MAP[size])

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