# Lattice matrix is a class that contains every possible combination of shapes from the input data in LatticeGenerator.
# Each layer in the matrix contains geometric figures with different amounts of each shape.
# For example, layer 0 contains figures with one shape. Layer 1 contains figures with two shapes, and so on and so forth.
# 
# attributes:
#   - lattice_matrix: list of lists of lattices, each list contains lattices with the same number of shapes in them
#
# functions:
#   - add uniquely
#   - len override

from isomorphism import Isomorphism
from polygon_vertex_incidence_matrix import PolygonVertexIncidenceMatrix

#@------------------------@#
#@-------Constants--------@#
#@------------------------@#

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class LatticeMatrix:

    # number of layers in the matrix depends on the number of shapes in the shape list
    # there will be the same number of layers in the lattice matrix 
    # as there are shapes in the shapes list
    def __init__(self, shape_amount):
        self._lattice_matrix = []

        for _ in range(shape_amount):
            self._lattice_matrix.append([])

    # Determines if the input lattice is isomorphic to any lattice in the matrix. If not, it adds it to the matrix
    # checks each lattice from the tuple_list against the _lattice_matrix at index for isomorphism
    # adds it to the _lattice_matrix if it is not isomorphic to anything already in the _lattice_matrix
    #
    # index - int, the index of the row in the matrix where the lattice should be placed
    # tuple_list - a list of tuples representing the lattices to be added
    #
    # no return
    def add_all_uniquely(self, index, tuple_list):
        # for each tuple in tuple_list,
        for shape, count_array in tuple_list:
            # get the lattice out of the tuple
            matrix_shape_list = [item[0] for item in self._lattice_matrix[index]]
            # check the lattice against the lattices already in _lattice_matrix for isomorphism
            if not Isomorphism.isomorph_in_list(matrix_shape_list, shape):
                # if they aren't isomorphic, it is a unique figure. add it to the _lattice_matrix
                self._lattice_matrix[index].append((shape, count_array))
                continue

    # len override
    # returns int number of elements in matrix
    def __len__(self):
    
        count = 0
        for row in self._lattice_matrix:
            count += len(row)

        return count