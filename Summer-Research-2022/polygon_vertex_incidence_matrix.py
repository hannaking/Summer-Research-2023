# pvim = polygon vertex incidence matrix
# each row is a vertex, each column is a shape in the figure
# so each row tells you which shapes that vertex is a part of and each col tells you which vertices are in that shape
#
# creates the pvim from a _nodes_list (list of lists)
#
# attributes:
#    _matrix : the actual underlying list of lists

# functions:
#  - get_row, a helper for initializing the matrix
#  - swap rows
#  - swap columns
#  - row sum
#  - col sum
#  - dimensions of matrix
#  - __str__ override

from node import Node

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class PolygonVertexIncidenceMatrix:
    # takes a _nodes_list instead of a Lattice to avoid circular import and to simplify
    def __init__(self, node_list):
        self._matrix = []

        # fill matrix
        for v_node in node_list[VERTEX_LATTICE_LAYER]:
            self._matrix.append(self._get_row(v_node, node_list))


    # get matrix row for a vertex node
    # matrix row contains True if that vertex is present in the shape for that column and False otherwise
    # indexes of the polygon columns are in the same order as the shapes are in the nodes list
    #
    # v_node    - Node object, a vertex node in the node list
    # node_list - _nodes_list from a Lattice. 2D list where each list in the list represents
    #             one lattice layer and contains the Node objects present on that lattice layer
    #
    # returns a list of True / False values (True if v_node is in the corresponding shape, False otherwise), which is one row in the pvim
    #
    # throws exception if v_node is not a Node object
    # throws exception if v_node is not on the vertex layer of the _nodes_list
    def _get_row(self, v_node, node_list):
        if not isinstance(v_node, Node):
            raise Exception("v_node is not a node")

        if v_node not in node_list[VERTEX_LATTICE_LAYER]:
            raise Exception("v_node is not a vertex node on the node_list")

        row = []
        # for the number of shape-level nodes, add a False entry to the row to get it to the right length
        for _ in node_list[SHAPE_LATTICE_LAYER]: 
            row.append(False)

        # for each shape-node v_node is tied to through the parents lists,
        # change the appropriate index in the new row to True
        # indexes of the polygon columns are in the same order as the shapes are in the nodes list
        for parent in v_node.get_parents():
            for grandparent in parent.get_parents():
                row[node_list[SHAPE_LATTICE_LAYER].index(grandparent)] = True

        return row


    # its fine if you swap a row with itself because nothing will change
    # used in both_tied_break in isomorphism.py
    # swap the specified rows using slice assignment
    #
    # row1_index - index of a row to be swapped
    # row2_index - index of the other row to be swapped
    #
    # throws exception if row1_index or row2_index are negative
    # throws exception if row1_index or row2_index are greater than the length of the matrix (exceeds number of vertices)
    def row_swap(self, row1_index, row2_index):
        if row1_index < 0 or row2_index < 0:
            raise Exception("One or both of the row indices are negative. Not allowed!")

        if row1_index > len(self._matrix) or row2_index > len(self._matrix):
            raise Exception("One or both of the row indices are greater than the valid index")

        self._matrix[row1_index], self._matrix[row2_index] = self._matrix[row2_index], self._matrix[row1_index]


    # swaps all values in two columns using slice assignment
    # for each list in the matrix, swap the two elements at the specified column indexes
    # attempting to swap a column with itself is fine, nothing will change
    #
    # col1_index - index of a column to be swapped
    # col2_index - index of the other column to be swapped
    #
    # throws exception if col1_index or col2_index are negative
    # throws exception if col1_index or col2_index are greater than the length of a matrix row (exceeds number of shapes)
    def col_swap(self, col1_index, col2_index):
        if col1_index < 0 or col2_index < 0:
            raise Exception("One or both of the col indices are negative. Not allowed!")

        if col1_index > len(self._matrix[0]) or col2_index > len(self._matrix[0]):
            raise Exception("One or both of the col indices are greater than the valid index")

        for item in self._matrix:
            item[col1_index], item[col2_index] = item[col2_index], item[col1_index]


    # sum the row (as if True = 1 and False = 0)
    #
    # row_index - index of the row you want the sum of
    #
    # returns the total number of True values in the specified row
    def row_sum(self, row_index):
        sum = 0
        for item in self._matrix[row_index]:
            if item:
                sum = sum + 1
        return sum


    # sum the column (as if True = 1 and False = 0)
    # for each row, if the column index in that row is True, add one to the sum
    #
    # col_index - index of the column you want the sum of
    #
    # returns the total number of True values in the specified column
    def col_sum(self, col_index):
        sum = 0
        for row in self._matrix:
            if row[col_index]:
                sum = sum + 1
        return sum


    # returns [row, col] dimensions
    # rows = number of vertices in lattice
    # cols = number of shapes in lattice
    def dimensions(self):
        dimensions = []
        dimensions.append(len(self._matrix))
        # every row has the same # of entries, so just use the first row to get the # of cols
        dimensions.append(len(self._matrix[0]))
        return dimensions


    # returns a nicely formatted string representation of the matrix in the PVIM object
    # looks like this:
    #                  [True, True]
    #                  [True, True]
    #                  [True, False]
    def __str__(self):
        string = ""
        for row in self._matrix:
            string = string + str(row) + "\n"

        return string