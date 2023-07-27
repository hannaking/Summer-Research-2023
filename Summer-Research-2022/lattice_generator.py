import itertools
import queue
import copy
from isomorphism import Isomorphism
import networkx as nx
import matplotlib.pyplot as plt

from lattice                            import Lattice
from polygon_vertex_incidence_matrix    import PolygonVertexIncidenceMatrix
from lattice_matrix                     import LatticeMatrix

#@---------------------
#@----- Constants -----
#@---------------------

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class LatticeGenerator:
    """
    The Lattice Generator class creates all lattice representations of figures that could represent a 
    list of shape quantities formatted as [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]

    """

    def __init__(self, shape_amounts):

        if not isinstance(shape_amounts, list):
            raise TypeError("shape_amounts must be a list")

        if len(shape_amounts) > 7:
            raise ValueError("Too many shapes given")
        
        # shape_amounts = [[], [], [], [], [], [], []]
        # shape list format -> [lines, tris, quads, ..., octagons]
        self._shape_list = [[], [], [], [], [], [], []]
                        #    2   3   4   5   6   7   8   sides
        # each element is an integer representing the number of that shape type which should be included
        # then it gets turned into a list of lists of lattice objects
        for i in range(len(shape_amounts)):
            for _ in range(shape_amounts[i]):
                vertices = i + 2
                self._shape_list[i].append(Lattice(vertices))

        self._shape_amounts = [len(x) for x in self._shape_list]

        self._shape_templates = [
            Lattice(2),
            Lattice(3),
            Lattice(4),
            Lattice(5),
            Lattice(6),
            Lattice(7),
            Lattice(8)
        ]

        # the assembly line
        self._figure_matrix = []               #! final list of lists thing on the board

    #@--------------------------@#
    #@----- Helper Methods -----@#
    #@--------------------------@#

    def _glue_vertices(self, shape, queue):

        temp_list = []

        # glue every item in the queue to the current shape
        for item in queue:
            for vertex in item._nodes_list[VERTEX_LATTICE_LAYER]:

                    # make sure you don't glue to yourself
                    if item is shape:
                        continue

                    # do the actual gluing and then add the item to the temp list
                    t_shape = item.glue_vertex(vertex, shape, shape._nodes_list[VERTEX_LATTICE_LAYER][0])
                    temp_list.append(t_shape)

        # unfiltered list: contains isomorphic shapes
        return temp_list

    # shape will be a simple shape that should be glued to each item in the queue
    # this order is very important
    def _glue_along_every_edge(self, shape, queue):

        if len(shape._nodes_list[SHAPE_LATTICE_LAYER]) > 1:
            return

        temp_list = []

        # loop through every item in the queue
        for item in queue:

            # dont glue to yourself
            if item is shape:
                continue

            glued_list = self._glue_each_pair(shape, item)

            temp_list.extend(glued_list)

        return temp_list

    # glues the shape to each pair of given vertices
    # returns a list of the glued shapes
    def _glue_each_pair(self, shape, item):
        
        # list that will return all glued shapes
        temp_list = []

        # find all valid pairs on base shape (item) (there should be no repeats)
        pairs = self._find_valid_pairs(item, shape)

        # now, glue each pair of vertices in the pairs list
        for pair in pairs:
            
            # print(pair[0], pair[1])
            # shape._geo_graph.show()

            x = item.get_node_from_label(str(pair[0]))
            y = item.get_node_from_label(str(pair[1]))

            new_shape = item.fill_gap(x, shape, y)

            temp_list.append(new_shape)

        return temp_list

    # finds pairs of valid vertices for gluing
    # returns a list of uniqpairs of vertices
    # item is only being passed for the purpose of checking the pair path length
    # does not exceed the size of the item
    def _find_valid_pairs(self, shape, item):

        # get perimeter of shape as to not find pairs that are interior to the shape
        perimeter = shape._geo_graph.get_perimeter()

        # find all possible pairs of vertices that can be glued
        item_length = len(item._nodes_list[VERTEX_LATTICE_LAYER])
        pairs = []
        for vertex_u in perimeter.nodes:
            for vertex_v in perimeter.nodes:

                # if str(vertex_u) == "4V000" and str(vertex_v) == "3V10":
                #     shape._geo_graph.show()
                #     shape.show()
                #     nx.draw_spring(perimeter, with_labels=True)
                #     plt.show()

                # prevent gluing to oneself
                if vertex_u is vertex_v:
                    continue
                
                #look at shortest path of the current pair and append to pairs if it is shorter than shape_length
                try:
                    if len(nx.shortest_path(perimeter, vertex_u, vertex_v)) <= item_length:
                        pairs.append([vertex_u, vertex_v])
                except:
                    continue
        #remove all pairs that are repeats, but in a different order
        no_duplicate_pairs = []
        for pair in pairs:
            if pair not in no_duplicate_pairs and [pair[1], pair[0]] not in no_duplicate_pairs:
                no_duplicate_pairs.append(pair)

        #print("no duplicate pairs len:", len(no_duplicate_pairs))
        # for pair in no_duplicate_pairs:
        #     print(str(pair[0]) + " " + str(pair[1]))
        #print("----------------------------------------------------")

        return no_duplicate_pairs
        
    # returns a list of shapes that are made by gluing
    # all shapes in the queue to the given shape
    def glue_quick(self, shape, queue):
        vertex_glue = self._glue_vertices(shape, queue)
        edge_glue = self._glue_along_every_edge(shape, queue)

        return vertex_glue + edge_glue

    # glues one of each remaining shapes in the list of shapes in the tuple
    # and returns a list of the glued shapes
    def glue_all(self, matrix_tuple):
        shape = matrix_tuple[0]
        count = matrix_tuple[1]

        result = []

        for i in range(len(count)):
            if count[i] > 0:
                new_shapes = self.glue_quick(self._shape_templates[i], [shape])

                # create new tuples
                for new_shape in new_shapes:
                    new_count = copy.deepcopy(count)
                    new_count[i] -= 1

                    result.append((new_shape, new_count))

        return result

    # constrains the lattice matrix to only matricies that have the correct number of shapes
    def constrain_to_final(self, matrix, num_shapes):
        '''
        flattens the Lattice matrix, removes associated the integer list and
        aquires only the Lattices that have a given number of total shape nodes

        matrix - the full Lattice matrix
        
        num_shapes - the number of shape nodes desired on the final Lattices

        returns the finalized list of Lattices
        '''
        final = []
        for layer in matrix:
            for lattice, _ in layer:
                if len(lattice._list_of_shapes) == num_shapes:
                    final.append(lattice)
        return final


    # glue shapes in shape list in every possible way
    # maximum shapes in a figure will be one more than the number of shapes in the shape list
    def glue_shapes(self):
        '''
        creates a matrix of Lattice representaions

        returns the Lattice matrix
        '''

        # sum shape array
        upper_bound = sum(self._shape_amounts)
        current_lvl = 1

        # initialize LatticeMatrix
        matrix = LatticeMatrix(upper_bound)

        # populate first shape layer
        # adds one of each simple shape in the shape list to the matrix
        # also adds the list of remaining shapes to be glued as a part of a tuple
        self._glue_matrix_layer_one(matrix)

        # loop through each shape in the previous matrix layer, then add glue_all each shape and append to current matrix layer
        while current_lvl < upper_bound:

            # get previous matrix layer
            previous_layer = matrix._lattice_matrix[current_lvl - 1]

            # glue all shapes in the previous layer
            glued_shapes = []

            for shape in previous_layer:
                glued_shapes.extend(self.glue_all(shape))

            # add glued shapes to current layer
            matrix.add_all_uniquely(current_lvl, glued_shapes)

            # increment current level
            current_lvl += 1

        return matrix

    # returns nothing because it should just change the matrix object
    def _glue_matrix_layer_one(self, matrix): #TODO: needs testing
        for i in range(len(self._shape_list)):

            shapes = self._shape_list[i]
            if len(shapes) == 0:
                continue

            current_shape = shapes[0]

            current_shape_amounts = copy.deepcopy(self._shape_amounts)
            current_shape_amounts[i] -= 1

            matrix._lattice_matrix[0].append( (current_shape, current_shape_amounts) )