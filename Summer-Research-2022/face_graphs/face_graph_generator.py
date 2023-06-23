# turns a lattice into a face graph to be fed into the network
#
# face graphs maintain information about the faces of a figure generated from a lattice,
# the sizes of the shapes in that figure, and the edgeiglued connections (which includes edges connected by fill gap)
# 
# Example Conversions
#
# 1. Single Triangle
#      Face Graph
#         O       <-- holds an id, size, and type
#                              0   3         Equilateral (or any of the other possibilities)
# 2. Vertex Glued Triangles
#      Face Graph
#         O  O    <-- each holds an id, size, and type
#                                   0   3         Equilateral (or any of the other possibilities) 
#                                   1   3         Right (or any of the other possibilities)
#       no edges!
# 3. Edge Glued Triangles
#      Face Graph
#         O---O    <-- each holds an id, size, and type
#                                   0   3         Equilateral (or any of the other possibilities) 
#       connected!                  1   3         Right (or any of the other possibilities)
#       the edge tells us that the two shapes share one side
# 4. Filled Gap Quad and Triangle
#      Face Graph
#         O---O    <-- each holds an id, size, and type
#          \_/                       0   3         Equilateral (or any of the other possibilities) 
#       connected twice!             1   4         Dart
#       the two edges tell us that the two shapes share two sides
#       fill gap is why this must be a multigraph


from lattice import Lattice
from lattice_test import LatticeTest
from node import Node

import itertools as its
import networkx  as nx
import matplotlib.pyplot as plt

# constants
SEGMENT_TYPES = ["Segment"]
TRIANGLE_TYPES = ["IsoscelesRight", "Right", "Equilateral", "Isosceles"]
QUADRILATERAL_TYPES = ["Square", "Rectangle", "Rhombus", "Parallelogram", "Kite", "RightTrapezoid", "IsoscelesTrapezoid", "Dart"]
PENTAGON_TYPES = ["RegularPentagon"]
HEXAGON_TYPES = ["RegularHexagon"]
HEPTAGON_TYPES = ["RegularHeptagon"]
OCTAGON_TYPES = ["RegularOctagon"]

ALL_TYPES = [SEGMENT_TYPES, TRIANGLE_TYPES, QUADRILATERAL_TYPES, PENTAGON_TYPES, HEXAGON_TYPES, HEPTAGON_TYPES, OCTAGON_TYPES]

SIDES_SHAPE_MAP = {1: SEGMENT_TYPES,  3: TRIANGLE_TYPES, 4: QUADRILATERAL_TYPES,
                   5: PENTAGON_TYPES, 6: HEXAGON_TYPES,  7: HEPTAGON_TYPES, 8: OCTAGON_TYPES}

class FaceGraphGenerator:
    """
    The Face Graph Generator class creates a networkX MultiGraph representation of a lattice.  Each node is the face of a shape and is
     labeled with the type of shape it is.  Each segment represents a shared edge between two faces.
    
    """
    def __init__(self, lattice  = None):
        
        # to store networkX graphs you will generate
        self.graphs = []

        # get the sizes of the shapes (number of edges per shape)
        # there isn't a predetermined order rule, but this order will be consistent
        # in this lattice and in the face graphs based on it
        sizes = []
        for node in lattice._list_of_shapes:
            sizes.append(len(node.get_children()))        

        # get every shape type possible for this figure
        combo_shapes = []
        for size in sizes:
            combo_shapes.extend(SIDES_SHAPE_MAP[size])

        # combine them in every way and
        # keep only the ones that line up with the shape sizes
        good = []
        # for every combo
        for combo in list(its.product(combo_shapes, repeat = len(sizes))):
            combo_sizes = []
            # look at each item individually
            for item in combo:
                # find what size shape it is for
                for i in range(0, len(ALL_TYPES)):
                    if item in ALL_TYPES[i]:
                        # i + 2 because indexing starts at 0, else i + 1 because a segment is size 1 not 2
                        combo_sizes.append(i + 2 if i > 0 else i + 1)
            # if the sizes for this combo match the actual sizes
            if combo_sizes == sizes:
                # keep it
                good.append(combo)
        useful_combos = list(set(good))

        # for every combination of shapes
        for combo in useful_combos:
            # add the newly created graphs
            self.graphs.append(self.build(lattice, sizes, combo))        

    # transforms a properly formatted list of lattices into face graphs
    # 
    # format: list containining lists of lattice types that are paired in a tuple
    #         with its input
    #
    # returns a set of face graphs
    @staticmethod
    def from_lattices(lattices:(list[list[tuple[Lattice]]] | list[list[tuple[LatticeTest]]])):
        face_graphs = set()

        for lattice_types in lattices:
            for lattice_pair in lattice_types:
                if(lattice_pair[1] == [0, 0, 0, 0, 0, 0, 0]):
                    faceGenerator = FaceGraphGenerator(lattice_pair[0])
                    for face_graph in faceGenerator.graphs:
                        # for graph in face_graphs:
                            # if not FaceGraphGenerator.is_same(face_graph, graph):
                        face_graphs.add(face_graph)

        return face_graphs
    
    # @staticmethod
    # def is_same(graph1, graph2):
    #     GM = nx.isomorphism.GraphMatcher(graph1, graph2)
    #     if not GM.is_isomorphic():
    #         return False
    #     GM.mapping
        
    #     for n1, n2 in GM.mapping.items():
    #         if graph1.nodes()[n1] != graph2.nodes()[n2]:
    #             return False
        
    #     return True

    # Creates one face graph
    # 
    # lattice - Lattice object to build the face graph from
    # sizes - list of ints, the size of a shape in the lattice in the correct order
    # types - list of strings, the types of faces for this particular face graph. in order of the lattice
    #
    # returns a networkX MultiGraph representing one face graph
    def build(self, lattice, sizes, types):
        graph = nx.MultiGraph()
        # build all nodes from the shape layer
        for i in range(0, len(lattice._list_of_shapes)):
            graph.add_node(i, type=types[i], size=sizes[i])
        
        # go to edge layer and
        for edge in lattice._list_of_edges:
            # get parents, which tell you which shapes are connected by this edge
            if len(edge.get_parents()) == 2:
                # add that edge to the graph / connect those two nodes
                graph.add_edge(lattice._list_of_shapes.index(edge.get_parents()[0]),
                               lattice._list_of_shapes.index(edge.get_parents()[1]))
        #nx.draw(graph)
        #plt.show()
        return graph