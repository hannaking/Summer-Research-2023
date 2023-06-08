import sys
from turtle import Shape
import unittest

# from numpy import matrix
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from node                               import Node
from lattice_test                       import LatticeTest
from isomorphism                        import Isomorphism
from lattice_generator                  import LatticeGenerator
from polygon_vertex_incidence_matrix    import PolygonVertexIncidenceMatrix
from column_vector                      import ColumnVector
from shape_helpers                      import ShapeHelpers

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class TestLatticeIsomorphism(unittest.TestCase):
    #--------------------------------------sort rows------------------------------------
    #    *       *
    #    |\     /|
    #    | \   / |
    #    |  \ /  |
    #    |   X   |
    #    |  / \  |
    #    | /   \ |
    #    |/     \|
    #    *-------*
    def test_sort_rows_filled_bowtie(self):
        filled_lattice = ShapeHelpers.filled_bowtie()

        LatticeGenerator([0, 1]) # for testing purposes, it doesn't matter what we initialize sweatshop with
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)

        # we'll get the row sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        row_sums_sorted = []
        for i in range(len(sorted._matrix)):
            row_sums_sorted.append(sorted.row_sum(i))

        row_sums_expected = [3, 2, 2, 1, 1]

        self.assertEqual(row_sums_expected, row_sums_sorted)

    # __________________
    #|\_______________/|
    #| |             | |
    #| |             | |
    #|_|_____________|_|
    def test_sort_rows_four_filled_rectangles(self):
        filled_lattice = ShapeHelpers.filled_glued_edge_quad_quad_quad()
        
        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)

        # we'll get the row sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        row_sums_sorted = []
        for i in range(len(sorted._matrix)):
            row_sums_sorted.append(sorted.row_sum(i))

        row_sums_expected = [3, 3, 2, 2, 2, 2, 1, 1]

        self.assertEqual(row_sums_expected, row_sums_sorted)

    #   #     *-------*
    #   #    / \     / \
    #   #   /   \   /   \
    #   #  /     \ /     \
    #   # *-------*-------*
    #   #  \     / \     /
    #   #   \   /   \   /
    #   #    \ /     \ /
    #   #     *-------*
    def test_sort_rows_pizza(self):
        filled_lattice = ShapeHelpers.pizza()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)

        # we'll get the row sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        row_sums_sorted = []
        for i in range(len(sorted._matrix)):
            row_sums_sorted.append(sorted.row_sum(i))

        row_sums_expected = [6, 2, 2, 2, 2, 2, 2]

        self.assertEqual(row_sums_expected, row_sums_sorted)

    def test_sort_rows_fish(self):
        fish = ShapeHelpers.complex_fish()

        matrix = PolygonVertexIncidenceMatrix(fish._nodes_list)

        # shuffle rows
        matrix._matrix = matrix._matrix[::-1]

        sorted = Isomorphism._sort_rows(matrix)

        row_sums_sorted = []
        for i in range(len(sorted._matrix)):
            row_sums_sorted.append(sorted.row_sum(i))

        row_sums_expected = [3, 2, 1, 1, 1, 1]

        self.assertEqual(row_sums_expected, row_sums_sorted)

    #--------------------------------sort cols-------------------------------#
    def test_sort_cols_filled_rectangle(self):
        filled_lattice = ShapeHelpers.filled_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_cols(matrix)

        # we'll get the col sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        col_sums_sorted = []
        for i in range(len(sorted._matrix[0])):
            col_sums_sorted.append(sorted.col_sum(i))

        col_sums_expected = [4, 3]

        self.assertEqual(col_sums_expected, col_sums_sorted)

    #   *
    #   |\  *-----*
    #   | \ |     |
    #   |  \|     |
    #   *---*-----*
    #      /|
    #     / |
    #    /  |
    #   *---*
    def test_sort_cols_two_triangles_glued_to_shape_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_cols(matrix)

        # we'll get the col sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        col_sums_sorted = []
        for i in range(len(sorted._matrix[0])):
            col_sums_sorted.append(sorted.col_sum(i))

        col_sums_expected = [4, 3, 3]

        self.assertEqual(col_sums_expected, col_sums_sorted)

    #       *-----* 
    #       |     |
    #       |     |
    # *-----*-----*
    def test_sort_cols_line_segment_glued_to_shape(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_cols(matrix)

        # we'll get the col sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        col_sums_sorted = []
        for i in range(len(sorted._matrix[0])):
            col_sums_sorted.append(sorted.col_sum(i))

        col_sums_expected = [4, 2]

        self.assertEqual(col_sums_expected, col_sums_sorted)

    def test_sort_cols_same_shape_glued_edge(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_cols(matrix)

        # we'll get the col sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        col_sums_sorted = []
        for i in range(len(sorted._matrix[0])):
            col_sums_sorted.append(sorted.col_sum(i))

        col_sums_expected = [3, 3]

        self.assertEqual(col_sums_expected, col_sums_sorted)

    def test_sort_cols_square_triangle_triangle(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_cols(matrix)

        # we'll get the col sums of everything in the sorted list and ensure that
        # these sums are in the correct order
        col_sums_sorted = []
        for i in range(len(sorted._matrix[0])):
            col_sums_sorted.append(sorted.col_sum(i))

        col_sums_expected = [4, 3, 3]

        self.assertEqual(col_sums_expected, col_sums_sorted)

    #-------------------------------------get row vectors------------------------------------#

    def test_get_row_vector_triangle(self):
        l1 = LatticeTest(3)

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        vectors = []
        for row in matrix._matrix:                                    
            vectors.append(Isomorphism._get_row_vector(row, matrix))

        expected = [
            [3],
            [3],
            [3]
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_row_vector_line_segment_glued_to_shape(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        vectors = []
        for row in matrix._matrix:                                    
            vectors.append(Isomorphism._get_row_vector(row, matrix))

        expected = [
            [2],
            [4, 2],
            [4],
            [4],
            [4]
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_row_vector_two_triangles_glued_to_shape_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        vectors = []
        for row in matrix._matrix:                                    
            vectors.append(Isomorphism._get_row_vector(row, matrix))

        expected = [
            [4],
            [4],
            [4],
            [4, 3, 3],
            [3],
            [3],
            [3],
            [3]
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_row_vector_same_shape_glued_edge(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        vectors = []
        for row in matrix._matrix:                                    
            vectors.append(Isomorphism._get_row_vector(row, matrix))

        expected = [
            [3],
            [3, 3],
            [3, 3],
            [3]
        ]

        self.assertCountEqual(expected, vectors)

    # *----*
    # |    | \
    # *----*--*
    def test_get_row_vector_diff_shapes(self):
        shape = ShapeHelpers.glued_edge_quad_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        vectors = []
        for row in matrix._matrix:                                    
            vectors.append(Isomorphism._get_row_vector(row, matrix))

        expected = [
            [4],
            [4],
            [4, 3],
            [4, 3],
            [3]
        ]

        self.assertCountEqual(expected, vectors)

    #--------------------------------------break row ties--------------------------------------#
    # FOR ALL OF THESE:
    #  because we can't predict how the columns will be ordered, we had it print out what
    # it was getting, then check if it was valid, then changed our test to it.

    # *       *
    # |\     /|
    # | \   / |
    # |  \ /  |
    # |   X   |
    # |  / \  |
    # | /   \ |
    # |/     \|
    # *-------*
    def test_break_row_ties_filled_bowtie(self):
        filled_lattice = ShapeHelpers.filled_bowtie()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True , True , True ],
            [True, False , True ],
            [False, True , True ],
            [True, False, False ],
            [False , True, False]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    # *----*----*----*
    # |    |    |    |
    # *----*----*----*
    #       \  /
    #        \/
    def test_break_row_ties_seesaw(self):
        filled_lattice = ShapeHelpers.seesaw()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True, False, True],
            [True, False, True, True],
            [True, True, False, False],
            [True, False, True, False],
            [False, True, False, False],
            [False, True, False, False],
            [False, False, True, False],
            [False, False, True, False],
            [False, False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    #   .____.____.
    #  /|    |    |
    #  \|____|____|
    #   |    |
    #   |____|
    def test_break_row_ties_blimp(self):
        filled_lattice = ShapeHelpers.blimp()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True, True, False],
            [True, True, False, True],
            [True, False, True, False],
            [True, False, False, True],
            [False, True, False, False],
            [False, True, False, False],
            [False, False, True, False],
            [False, False, True, False],
            [False, False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    # *       *
    # |\     /|
    # | \   / |
    # |  \ /  |
    # |   *   |
    # |  / \  |
    # | /   \ |
    # |/     \|
    # *       *
    def test_break_row_ties_bowtie(self):
        filled_lattice = ShapeHelpers.bowtie()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True],
            [True, False],
            [True, False],
            [False, True],
            [False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    # *---------*
    # |         |\
    # |         | \
    # |         |  \
    # |         |   \
    # |         |    \
    # *---------*-----*
    def test_break_row_ties_glued_edge_quad_tri(self):
        filled_lattice = ShapeHelpers.glued_edge_quad_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True],
            [True, True],
            [True, False],
            [True, False],
            [False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    #       *-----* 
    #       |     |
    #       |     |
    # *-----*-----*
    def test_break_row_ties_glued_vertex_segment_quad(self):
        filled_lattice = ShapeHelpers.glued_vertex_segment_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True],
            [True, False],
            [True, False],
            [True, False],
            [False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    #   *
    #   |\  *-----*
    #   | \ |     |
    #   |  \|     |
    #   *---*-----*
    #      /|
    #     / |
    #    /  |
    #   *---*
    def test_break_row_ties_glued_vertex_tri_tri_quad(self):
        filled_lattice = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # for i in ties_broken._matrix:
        #     print(i)

        # because we can't predict how the columns will be ordered, we had it print out what
        # it was getting, then check if it was valid, then changed our test to it.
        expected = [
            [True, True, True],
            [True, False, False],
            [True, False, False],
            [True, False, False],
            [False, True, False],
            [False, True, False],
            [False, False, True],
            [False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

#     #-----------------------------get col vectors-----------------------------#
    def test_get_col_vector_triangle(self):
        l1 = LatticeTest(3)

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [1, 1, 1]
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_col_vector_line_segment_glued_to_shape(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [2, 1, 1, 1],
            [2, 1],
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_col_vector_two_triangles_glued_to_shape_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [3, 1, 1, 1],
            [3, 1, 1],
            [3, 1, 1]
        ]
        self.assertCountEqual(expected, vectors)

    def test_get_col_vector_same_shape_glued_edge(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [2, 2, 1],
            [2, 2, 1]
        ]

        self.assertCountEqual(expected, vectors)

    # *----*
    # |    | \
    # *----*--*
    def test_get_col_vector_diff_shapes(self):
        shape = ShapeHelpers.glued_edge_quad_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [2, 2, 1, 1],
            [2, 2, 1]
        ]

        self.assertCountEqual(expected, vectors)

    def test_get_col_vector_funky_shape_2(self):
        shape = ShapeHelpers.funky_shape()
        #--gluing done--#

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        pvim = Isomorphism._break_row_ties(sorted)

        vectors = []
        num_columns = len(pvim._matrix[0])
        for i in range(num_columns):
                vectors.append(Isomorphism._get_col_vector(i, pvim)._vector)

        expected = [
            [4, 4, 3, 2],
            [4, 3, 2],
            [4, 4, 3],
            [4, 3, 3],
            [4, 3, 3],
            [4, 2, 2],
            [3, 3, 1]
        ]

        self.assertCountEqual(expected, vectors)

#     #T-----------------------------break col ties-----------------------------#
    # #@ to test: four filled rectangles, pizza
    # #@ for now, their asserts are commented out
    def test_break_col_ties_funky_shape_2(self):
        shape = ShapeHelpers.funky_shape()
        #--gluing done--#

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)
        
        # print("before:")
        # for i in ties_broken._matrix:
        #     print(i)
        
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        # print("after:")
        # for i in ties_broken._matrix:
        #     print(i)

        CTrue = True

        expected = [
            [CTrue, CTrue, False, False, CTrue, CTrue, False],
            [CTrue, CTrue, CTrue, CTrue, False, False, False],
            [CTrue, False, False, CTrue, False, False, CTrue],
            [False, CTrue, CTrue, False, CTrue, False, False],
            [False, False, CTrue, CTrue, False, False, CTrue],
            [CTrue, False, False, False, False, CTrue, False],
            [False, False, False, False, CTrue, CTrue, False],
            [False, False, False, False, False, False, CTrue]
        ]     # 0     1      2      3      4      5      6

        self.assertEqual(expected, ties_broken._matrix)

    
    def test_break_col_ties_pizza(self): 
        shape = ShapeHelpers.pizza()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        # print("PIZZA MATRIX!!!!")
        # for i in matrix._matrix:
        #     print(i)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)
        
        # print("pizza:")
        # for i in ties_broken._matrix:
        #     print(i)

        ties_broken = Isomorphism._break_col_ties(ties_broken)

        # print("pizza:")
        # for i in ties_broken._matrix:
        #     print(i)

        CTrue = True

        expected = [
            [CTrue, CTrue, CTrue, CTrue, CTrue, CTrue],
            [CTrue, CTrue, False, False, False, False],
            [CTrue, False, False, CTrue, False, False],
            [False, CTrue, CTrue, False, False, False],
            [False, False, CTrue, False, False, CTrue],
            [False, False, False, CTrue, CTrue, False],
            [False, False, False, False, CTrue, CTrue]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    def test_break_col_ties_filled_bowtie(self): 
        shape = ShapeHelpers.filled_bowtie()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # print("filled bowtie:")
        # for i in ties_broken._matrix:
        #     print(i)

        ties_broken = Isomorphism._break_col_ties(ties_broken)

        # print("post col ties bowtie:")
        # for i in ties_broken._matrix:
        #     print(i)

        expected = [
            [True, True, True],
            [True, True, False],
            [True, False, True],
            [False, True, False],
            [False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    def test_break_col_ties_four_filled_rectangles(self): #@ change
        shape = ShapeHelpers.filled_glued_edge_quad_quad_quad()
        
        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)
    

        ties_broken = Isomorphism._break_col_ties(ties_broken)

        CTrue = True
        expected = [
            [CTrue, CTrue, CTrue, False],
            [CTrue, CTrue, False, CTrue],
            [CTrue, False, CTrue, False],
            [CTrue, False, False, CTrue],
            [False, CTrue, CTrue, False],
            [False, CTrue, False, CTrue],
            [False, False, CTrue, False],
            [False, False, False, CTrue]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    def test_break_col_ties_star(self):
        shape = ShapeHelpers.pentagram()
        
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)
    
        # print("before")
        # for i in ties_broken._matrix:
        #     print(i)

        # doesn't change anything
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        # print("after")
        # for i in ties_broken._matrix:
        #     print(i)

        Trues = True
        expected = [
            [True, True, False, False, True, False],
            [True, True, True, False, False, False],
            [True, False, True, True, False, False],
            [True, False, False, True, False, True],
            [True, False, False, False, True, True],
            [False, True, False, False, False, False],
            [False, False, True, False, False, False],
            [False, False, False, True, False, False],
            [False, False, False, False, True, False],
            [False, False, False, False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

    #TODO: add assertion
    def test_break_col_ties_snake(self):

        shape = ShapeHelpers.snake()
        
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # print("before")
        # for i in ties_broken._matrix:
        #     print(i)

        # no change
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        expected = [
            [True, True, False],
            [True, False, True],
            [True, False, False],
            [False, True, False],
            [False, True, False],
            [False, False, True],
            [False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)
        
    def test_glue_one_vertex_tri_tri_tri(self):
        
        shape = ShapeHelpers.glue_one_vertex_tri_tri_tri()

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)

        # print("before")
        # for i in ties_broken._matrix:
        #     print(i)

        # no change
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        expected = [
            [True, True, True],
            [True, False, False],
            [True, False, False],
            [False, True, False],
            [False, True, False],
            [False, False, True],
            [False, False, True]
        ]

        self.assertEqual(expected, ties_broken._matrix)

#     #-------------------------------------get max length--------------------------------------#
    def test_get_max_length_all_same_length(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1, 1, 1], 0),
            ColumnVector([2, 2, 2], 1),
            ColumnVector([3, 3, 3], 2)
        ]
        expected = 3
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_first_is_longest(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1, 1, 1], 0),
            ColumnVector([2], 1),
            ColumnVector([3], 2)
        ]
        expected = 3
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_first_is_not_longest(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1], 0),
            ColumnVector([2, 2, 2], 1),
            ColumnVector([3, 3, 3], 2)
        ]
        expected = 3
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_middle_is_longest(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1], 0),
            ColumnVector([2, 2, 2, 2, 6, 4, 2, 7], 1),
            ColumnVector([3], 2)
        ]
        expected = 8
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_last_is_longest(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1], 0),
            ColumnVector([2], 1),
            ColumnVector([3, 3, 3, 3, 3, 3, 3, 3], 2)
        ]
        expected = 8
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_all_diff_length(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1, 5, 3], 0),
            ColumnVector([4, 6, 8, 6, 4, 3, 3], 1),
            ColumnVector([2, 3, 3, 3, 2], 2),
            ColumnVector([4, 3, 2, 5], 3)
        ]
        expected = 7
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

    def test_get_max_length_keeps_getting_bigger(self):
        LatticeGenerator([0])

        col_vectors = [
            ColumnVector([1], 0),
            ColumnVector([2, 2], 1),
            ColumnVector([3, 3, 3], 2),
            ColumnVector([4, 4, 4, 4], 3),
            ColumnVector([5, 5, 5, 5, 5], 4)
        ]
        expected = 5
        actual = Isomorphism._get_max_length(col_vectors)

        self.assertEqual(expected, actual)

#     #----------------------------get next group----------------------------------------------#
    def test_get_next_group_all_same_length(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([2, 2, 2], 1)
        c = ColumnVector([3, 3, 3], 2)

        column_vectors = [
            a,
            b,
            c
        ]
        length_to_find = 3

        actual = Isomorphism._get_next_group(column_vectors, length_to_find)

        expected = [
            a,
            b,
            c
        ]

        self.assertCountEqual(expected, actual)

    def test_get_next_group_all_different_lengths(self):
        LatticeGenerator([0])

        a = ColumnVector([1], 0)
        b = ColumnVector([2, 2], 1)
        c = ColumnVector([3, 3, 3], 2)

        column_vectors = [
            a,
            b,
            c
        ]
        length_to_find = 3

        actual = Isomorphism._get_next_group(column_vectors, length_to_find)

        expected = [
            c
        ]

        self.assertCountEqual(expected, actual)

    def test_get_next_group_two_different_groups_find_length_2(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([1, 1], 1)
        c = ColumnVector([2, 2, 2], 2)
        d = ColumnVector([2, 2], 3)
        e = ColumnVector([3, 3, 3], 4)
        f = ColumnVector([3, 3], 5)

        column_vectors = [
            a,
            b,
            c,
            d,
            e,
            f
        ]
        length_to_find = 2

        actual = Isomorphism._get_next_group(column_vectors, length_to_find)

        expected = [
            b,
            d,
            f
        ]

        self.assertEqual(expected, actual)

    def test_get_next_group_two_different_groups_find_length_3(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([1, 1], 1)
        c = ColumnVector([2, 2, 2], 2)
        d = ColumnVector([2, 2], 3)
        e = ColumnVector([3, 3, 3], 4)
        f = ColumnVector([3, 3], 5)

        column_vectors = [
            a,
            b,
            c,
            d,
            e,
            f
        ]
        length_to_find = 3

        actual = Isomorphism._get_next_group(column_vectors, length_to_find)

        expected = [
            a,
            c,
            e
        ]

        self.assertEqual(expected, actual)

#     #----------------------------------------get groups------------------------------------#
    def test_get_groups_one_group(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([2, 2, 2], 1)
        c = ColumnVector([3, 3, 3], 2)
        column_vectors = [
            a,
            b,
            c
        ]

        actual = Isomorphism._get_groups(column_vectors)

        expected = [
            [   a,
                b,
                c
            ]
        ]

        self.assertCountEqual(expected[0], actual[0])

    def test_get_groups_two_groups(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([2, 2, 2], 1)
        c = ColumnVector([1, 1], 2)
        d = ColumnVector([2, 2], 3)

        column_vectors = [
            a,
            b,
            c,
            d
        ]

        actual = Isomorphism._get_groups(column_vectors)

        expected = [
            [   a,
                b
            ],

            [
                c,
                d
            ]
        ]

        # i don't want to compare column_vector objects so i'm just going to get
        # the vector instance variables from actual and expected so i can compare those
        actual_vectors = []
        for group in actual:
            for vector in group:
                actual_vectors.append(vector._vector)

        expected_vectors = []
        for group in expected:
            for vector in group:
                expected_vectors.append(vector._vector)
            
        for group in actual_vectors:
            group.sort()
        for group in expected_vectors:
            group.sort()
            self.assertTrue(group in actual_vectors)

    def test_get_groups_three_groups(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1], 0)
        b = ColumnVector([2, 2, 2], 1)
        c = ColumnVector([1], 2)
        d = ColumnVector([1, 1], 3)
        e = ColumnVector([2], 4)
        f = ColumnVector([2, 2], 5)


        column_vectors = [
            a,
            b,
            c,
            d,
            e,
            f
        ]

        actual = Isomorphism._get_groups(column_vectors)

        expected = [
            [   a,
                b
            ],

            [
                c,
                e
            ],

            [
                d,
                f
            ]
        ]

        # i don't want to compare column_vector objects so i'm just going to get
        # the vector instance variables from actual and expected so i can compare those
        actual_vectors = []
        for group in actual:
            for vector in group:
                actual_vectors.append(vector._vector)

        expected_vectors = []
        for group in expected:
            for vector in group:
                expected_vectors.append(vector._vector)
            
        for group in actual_vectors:
            group.sort()
        for group in expected_vectors:
            group.sort()
            self.assertTrue(group in actual_vectors)

    def test_get_groups_four_groups(self):
        LatticeGenerator([0])

        a = ColumnVector([1, 1, 1, 1], 0)
        b = ColumnVector([1, 1, 1], 1)
        c = ColumnVector([2, 2, 2], 2)
        d = ColumnVector([1], 3)
        e = ColumnVector([2, 2, 2, 2], 4)
        f = ColumnVector([1, 1], 5)
        g = ColumnVector([2], 6)
        h = ColumnVector([2, 2], 7)
        i = ColumnVector([3, 3, 3, 3], 8)
        
        column_vectors = [
            a, 
            b,
            c,
            d,
            e,
            f,
            g,
            h,
            i
        ]

        actual = Isomorphism._get_groups(column_vectors)

        expected = [
            [   b,
                c
            ],

            [
                d,
                g
            ],

            [
                f,
                h
            ],

            [
                a,
                e,
                i
            ]
        ]

        # i don't want to compare column_vector objects so i'm just going to get
        # the vector instance variables from actual and expected so i can compare those
        actual_vectors = []
        for group in actual:
            for vector in group:
                actual_vectors.append(vector._vector)

        expected_vectors = []
        for group in expected:
            for vector in group:
                expected_vectors.append(vector._vector)
            
        for group in actual_vectors:
            group.sort()
        for group in expected_vectors:
            group.sort()
            self.assertTrue(group in actual_vectors)
#     #-------------------------------compare vectors--------------------------------#
    def test_compare_vectors_vector_u_not_a_colvector(self):
        LatticeGenerator([0])
        vector_u = "not a column vector"
        vector_v = ColumnVector([1, 1, 1], 0)
        with self.assertRaises(TypeError):
            Isomorphism._compare_vectors(vector_u, vector_v)

    def test_compare_vectors_vector_v_not_a_colvector(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 1], 0)
        vector_v = "not a column vector"
        with self.assertRaises(TypeError):
            Isomorphism._compare_vectors(vector_u, vector_v)

    def test_compare_vectors_vector_u_and_vector_v_are_different_length(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 1], 0)
        vector_v = ColumnVector([1, 1], 0)
        with self.assertRaises(ValueError):
            Isomorphism._compare_vectors(vector_u, vector_v)

    def test_compare_vectors_vector_u_and_vector_v_are_equal(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 1], 0)
        vector_v = ColumnVector([1, 1, 1], 0)
        actual = Isomorphism._compare_vectors(vector_u, vector_v)
        expected = False
        self.assertEqual(expected, actual)

    def test_compare_vectors_vector_u_is_greater_than_vector_v(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 1], 0)
        vector_v = ColumnVector([1, 1, 0], 0)
        actual = Isomorphism._compare_vectors(vector_u, vector_v)
        expected = True
        self.assertEqual(expected, actual)

    def test_compare_vectors_vector_u_is_less_than_vector_v(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 0], 0)
        vector_v = ColumnVector([1, 1, 1], 0)
        actual = Isomorphism._compare_vectors(vector_u, vector_v)
        expected = False
        self.assertEqual(expected, actual)

    def test_compare_vectors_vector_u_is_greater_than_vector_v_with_different_length(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1, 1], 0)
        vector_v = ColumnVector([1, 1], 0)
        with self.assertRaises(ValueError):
            Isomorphism._compare_vectors(vector_u, vector_v)

    def test_compare_vectors_vector_u_is_less_than_vector_v_with_different_length(self):
        LatticeGenerator([0])
        vector_u = ColumnVector([1, 1], 0)
        vector_v = ColumnVector([1, 1, 1], 0)
        with self.assertRaises(ValueError):
            Isomorphism._compare_vectors(vector_u, vector_v)

    #------------------------------sort group--------------------------------------------#
    def test_sort_group_two_ties_length_1(self): #simplest test case (i think, lmao?)
        LatticeGenerator([0])

        pvim = PolygonVertexIncidenceMatrix([[1], [Node(1)], [1], [1], [1]]) #does not matter what we init pvim as because i will change matrix myself
        # keep in mind this matrix does not represent a real shape
        pvim._matrix = [
            [False, True , True ],
            [True , False, False],
            [False, False, True ]
        #   [1]     [2]    (2)
        ]

        Isomorphism._sort_rows(pvim)
        Isomorphism._sort_cols(pvim)
        Isomorphism._break_row_ties(pvim)

        # [True, False, True]
        # [True, False, False]
        # [False, True, False]
        # (2, 1)  (1)   (2)

        # get the column vectors in a list
        column_vectors = [] # (these are column_vector objects)
        for i in range(len(pvim._matrix[0])):
            column_vectors.append(Isomorphism._get_col_vector(i, pvim))
        
        group = Isomorphism._get_next_group(column_vectors, 1) #@

        # sort the group
        sorted_pvim = Isomorphism._sort_group(group, pvim)

        expected = [
            [True , True, False ],
            [True, False , False],
            [False, False, True ]
        #   [2, 1)  (2)    (1)
        ]
            
        self.assertEqual(expected, sorted_pvim._matrix)

    def test_sort_group_two_ties_length_2(self):
        LatticeGenerator([0])

        pvim = PolygonVertexIncidenceMatrix([[1], [Node(1)], [1], [1], [1]]) #does not matter what we init pvim as because i will change matrix myself
        # keep in mind this matrix does not represent a real shape
        pvim._matrix = [
            [False, True , False, False],
            [True , True , False, False],
            [True , False, True , True ],
            [False, False, True , False],
            [True , False, False, False]
        #   (2, 3, 1)  (1, 2)  (3, 1)  (3)
        ]

        Isomorphism._sort_rows(pvim)
        Isomorphism._sort_cols(pvim)
        Isomorphism._break_row_ties(pvim)

        # [True , False, True , True ]
        # [True , True , False, False]
        # [True , False, False, False]
        # [False, True , False, False]
        # [False, False, True , False]
        # (3, 2, 1)  (2, 1)  (3, 1)  (3)

        # get the column vectors in a list
        column_vectors = [] # (these are column_vector objects)
        for i in range(len(pvim._matrix[0])):
            column_vectors.append(Isomorphism._get_col_vector(i, pvim))
        
        group = Isomorphism._get_next_group(column_vectors, 2) #@

        # sort the group
        sorted_pvim = Isomorphism._sort_group(group, pvim)

        expected = [
            [True, True, False , True],
            [True , False, True , False],
            [True , False , False, False ],
            [False, False , True, False],
            [False , True, False, False]
        #   (3, 2, 1)  (3, 1)  (2, 1)  (3)
        ]

        self.assertEqual(expected, sorted_pvim._matrix)

    def test_sort_group_five_ties(self):
        LatticeGenerator([0])

        pvim = PolygonVertexIncidenceMatrix([[1], [Node(1)], [1], [1], [1]]) #does not matter what we init pvim as because i will change matrix myself
        # keep in mind this matrix does not and cannot represent a real shape
        pvim._matrix = [
            [True , True , True , False,     False, False, False],
            [True , False, False, True ,     True , True , False],
            [False, True , False, True ,     False, False, False],
            [False, False, True , True ,     True , True , True ]
        #   [3,4]   [3,2]  [3,5]  [4, 2, 5]  [4,5]  [4,5]  [5]
        ]

        Isomorphism._sort_rows(pvim)
        Isomorphism._sort_cols(pvim)
        Isomorphism._break_row_ties(pvim)

        # print("after steps 1, 1.1, 1.4, 1.5, 2, 2.5, 3 thing")
        # for i in pvim._matrix:
        #     print(i)

        # [True ,    False,  False,  True ,  True ,  True , True ]
        # [True ,    True ,  False,  False,  True ,  True , False]
        # [False,    True ,  True ,  True ,  False,  False, False]
        # [True ,    False,  True ,  False,  False,  False, False]
        # (5, 4, 2)  (4, 3)  (3, 2)  (5, 3)  (5, 4)  (5, 4)  (5)

        # get the column vectors in a list
        column_vectors = [] # (these are column_vector objects)
        for i in range(len(pvim._matrix[0])):
            column_vectors.append(Isomorphism._get_col_vector(i, pvim))
        
        group = Isomorphism._get_next_group(column_vectors, 2)
        # sort the group
        sorted_group_pvim = Isomorphism._sort_group(group, pvim)

        # print("after group sort five ties")
        # for i in sorted_group_pvim._matrix:
        #     print(i)

        expected = [
            [True ,    True ,  True ,  True ,  False,  False,  True],
            [True ,    True ,  True ,  False,  True ,  False,  False],
            [False,    False,  False,  True ,  True ,  True ,  False],
            [True ,    False,  False,  False,  False,  True ,  False ]
        #   (5, 4, 2)  (5, 4)  (5, 4)  (5, 3)  (4, 3)  (3, 2)  (5)
        ]

        self.assertEqual(expected, sorted_group_pvim._matrix)

    def test_sort_group_bowtie(self):
        LatticeGenerator([0])

        pvim = PolygonVertexIncidenceMatrix([[1], [Node(1)], [1], [1], [1]]) #does not matter what we init pvim as because i will change matrix myself
        # keep in mind this matrix does not and cannot represent a real shape
        pvim._matrix = [
            [True , True , True],
            [True , False, True], 
            [False, True , True],
            [True, False, False],
            [False, True, False]
        ]
        #   [3,2,1] [3,2,1] [3,2,2]

        Isomorphism._sort_rows(pvim)
        Isomorphism._sort_cols(pvim)
        Isomorphism._break_row_ties(pvim)

        # print("after steps 1, 1.1, 1.4, 1.5, 2, 2.5, 3 thing")
        # for i in pvim._matrix:
        #     print(i)

        # get the column vectors in a list
        column_vectors = [] # (these are column_vector objects)
        for i in range(len(pvim._matrix[0])):
            column_vectors.append(Isomorphism._get_col_vector(i, pvim))
        
        group = Isomorphism._get_next_group(column_vectors, 3)
        # sort the group
        sorted_group_pvim = Isomorphism._sort_group(group, pvim)

        # print("after group sort five ties")
        # for i in sorted_group_pvim._matrix:
        #     print(i)

        expected = [
            [True ,   True ,  True],
            [True ,   True ,  False],
            [True ,   False,  True],
            [False,   True ,  False],
            [False,   False,  True]
        #   (3, 2, 2)  (3, 2, 1)  (3, 2, 1)
        ]

        self.assertEqual(expected, sorted_group_pvim._matrix)


        ###                                                   ###     
        ###           STEP 5 STUFF HERE!!!!!                  ###
        ###                EVENTUALLY                         ###                           eowfhoweeeeeeeeeeeeeeeeifhweoifhwoe
        ###     I THINK IS CURRENTLY NEAR THE BOTTOM?         ###
        ###                                                   ###


#     #-------------------------------get row index vectors-------------------------------#
    def test_get_row_index_vectors_triangle(self):
        l1 = LatticeTest(3)

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0],
            [0],
            [0]
        ]

        self.assertEqual(expected, vectors)

    def test_get_row_index_vectors_line_segment_glued_to_quad(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()

        LatticeGenerator([1, 0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0, 1],
            [0],
            [0],
            [0],
            [1]
        ]

        self.assertEqual(expected, vectors)

    def test_get_row_index_vectors_two_triangles_glued_to_quad_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0, 1, 2],
            [0],
            [0],
            [0],
            [1],
            [1],
            [2],
            [2],
        ]

        self.assertEqual(expected, vectors)

    def test_get_row_index_vectors_same_shape_glued_edge(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0, 1],
            [0, 1],
            [0],
            [1]
        ]

        self.assertEqual(expected, vectors)


    def test_get_row_index_vectors_diff_shapes(self):
        shape = ShapeHelpers.glued_edge_quad_tri()

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)
        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0, 1],
            [0, 1],
            [0],
            [0],
            [1],
        ]

        self.assertEqual(expected, vectors)

    def test_get_row_index_vectors_funky_shape(self):
        shape = ShapeHelpers.funky_shape()
        #--gluing done--#

        LatticeGenerator([0, 1])
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        sorted = Isomorphism._sort_rows(matrix)
        sorted = Isomorphism._sort_cols(sorted)

        ties_broken = Isomorphism._break_row_ties(sorted)
        ties_broken = Isomorphism._break_col_ties(ties_broken)

        vectors = []
        for row in ties_broken._matrix:                                    
            vectors.append(Isomorphism._get_row_index_vector(row))

        expected = [
            [0, 1, 4, 5],
            [0, 1, 2, 3],
            [0, 3, 6],
            [1, 2, 4],
            [2, 3, 6],
            [0, 5],
            [4, 5],
            [6]
        ]

        self.assertEqual(expected, vectors)

# # # ------------------------------ step 6 but its also down below? ------------------------------------------
# #     # *       *
# #     # |\     /|
# #     # | \   / |
# #     # |  \ /  |
# #     # |   X   |
# #     # |  / \  |
# #     # | /   \ |
# #     # |/     \|
# #     # *-------*
# #     def test_break_row_index_ties_filled_bowtie(self):
# #         filled_lattice = ShapeHelpers.filledbowtie()

# #         matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)

# #         # because we can't predict how the columns will be ordered, we had it print out what
# #         # it was getting, then check if it was valid, then changed our test to it.
# #         expected = [
# #             [True , True , True ],
# #             [True, True, False],
# #             [True, False, True ],
# #             [False, True, False],
# #             [False, False, True]
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

# #     def test_break_row_index_ties_line_segment_glued_to_shape(self):
# #         shape = ShapeHelpers.glued_vertex_segment_quad()

# #         LatticeGenerator([0, 1])
# #         matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)

# #         expected = [
# #             [True , True ],
# #             [True , False],
# #             [True , False],
# #             [True , False],
# #             [False, True ]
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

# #     def test_break_row_index_ties_square_triangle_triangle(self):
# #         l1 = LatticeTest(4)
# #         vertex_node1 = l1._bot_node.get_parents()[0]
# #         l2 = LatticeTest(3)
# #         vertex_node2 = l2._bot_node.get_parents()[0]
# #         l3 = LatticeTest(3)
# #         vertex_node3 = l3._bot_node.get_parents()[0]

# #         post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2)

# #         next_vertex = post_glued1.get_node_from_label("3V1")
# #         shape = post_glued1.glue_vertex(next_vertex, l3, vertex_node3)

# #         LatticeGenerator([0, 1])
# #         matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)

# #         # for i in ties_broken._matrix:
# #         #     print(i)

# #         expected = [
# #             [True , True , False],
# #             [False, True , True ],
# #             [True , False, False],
# #             [True , False, False],
# #             [True , False, False],
# #             [False, True , False],
# #             [False, False, True ],
# #             [False, False, True ],
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

# #     #    ____ /\
# #     #  /|    |  \
# #     # |\|____|  /
# #     # |     / \/
# #     # |    /
# #     # |   /
# #     # |  /
# #     # | /
# #     # |/
# #     def test_break_row_ties_funky_shape(self):
# #         shape = ShapeHelpers.goofy_shape()
        
# #         matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)

# #         # for i in ties_broken._matrix:
# #         #     print(i)

# #         expected = [
# #             [True , True , True , False],
# #             [False, True , True , True ],
# #             [True , True, False , False],
# #             [False, True , False, True ],
# #             [False, False, True , True ],
# #             [True , False, False, False],
# #             [True , False, False, False],
# #             [True , False, False, False],
# #             [False, False , True, False]
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

# #     def test_break_row_ties_funky_shape_2(self):
# #         l1 = LatticeTest(3)
# #         l2 = LatticeTest(3)
# #         l3 = LatticeTest(3)
# #         l4 = LatticeTest(3)
# #         l5 = LatticeTest(3)
# #         l6 = LatticeTest(3)
# #         l7 = LatticeTest(4)

# #         e1 = l1._nodes_list[EDGE_LATTICE_LAYER][0]
# #         e2 = l2._nodes_list[EDGE_LATTICE_LAYER][0]
# #         shape = l1.glue_edge(e1, l2, e2)

# #         e1 = shape.get_node_from_label("7E1")
# #         e2 = l3._nodes_list[EDGE_LATTICE_LAYER][0]
# #         shape = shape.glue_edge(e1, l3, e2)
        
# #         e1 = shape.get_node_from_label("7E1")
# #         e2 = l4._nodes_list[EDGE_LATTICE_LAYER][0]
# #         shape = shape.glue_edge(e1, l4, e2)

# #         e1 = shape.get_node_from_label("6E000")
# #         e2 = l5._nodes_list[EDGE_LATTICE_LAYER][0]
# #         shape = shape.glue_edge(e1, l5, e2)

# #         e1 = shape.get_node_from_label("7E10")
# #         e2 = l6._nodes_list[EDGE_LATTICE_LAYER][0]
# #         shape = shape.glue_edge(e1, l6, e2)

# #         v1 = shape.get_node_from_label("4V10")
# #         v2 = shape.get_node_from_label("4V100")
# #         shape = shape.fill_gap(v1, l7, v2)
# #         #--gluing done--#
# #         LatticeGenerator([0, 1])
# #         matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)

# #         expected = [
# #             [True, True, True, False, False, True, False],
# #             [True, False, True, True, True, False, False],
# #             [True, False, False, False, True, False, True],
# #             [False, True, True, True, False, False, False],
# #             [False, False, False, True, True, False, True],
# #             [True, False, False, False, False, True, False],
# #             [False, True, False, False, False, True, False],
# #             [False, False, False, False, False, False, True]
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

# #     def test_break_row_ties_two_triangles_glued_to_shape_by_one_vertex(self):
# #         shape = ShapeHelpers.glued_vertex_tri_tri_quad()

# #         matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

# #         sorted = Isomorphism._sort_rows(matrix)
# #         sorted = Isomorphism._sort_cols(sorted)
# #         ties_broken = Isomorphism._break_row_ties(sorted)
# #         ties_broken = Isomorphism._break_col_ties(ties_broken)
# #         ties_broken = Isomorphism._similarity_col_sort(ties_broken)


# #         expected = [
# #             [True, True, True],
# #             [True, False, False],
# #             [True, False, False],
# #             [True, False, False],
# #             [False, True, False],
# #             [False, True, False],
# #             [False, False, True],
# #             [False, False, True]
# #         ]

# #         self.assertEqual(expected, ties_broken._matrix)

    
# #----------------------------------------------- Check Isomorphism -----------------------------------------------------
    #  different dimensions                   x
    #  simple shapes isomorphic               x
    #  simple shapes not isomorphic           x
    #  post-vertex glue isomorphic            x
    #  post-vertex-glue not isomorphic        x
    #  post edge glue isomorphic              x
    #  post edge glue not isomorphic          x
    #  post fill isomorphic                   x
    #  post fill not isomorphic               x
    #? special case ismorphism                x


    def test_check_isomorphism_triangle_segment(self):
        triangle = LatticeTest(3) #matrix is 3x1
        segment  = LatticeTest(2) #matrix is 2x1

        pvim1 = PolygonVertexIncidenceMatrix(triangle._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(segment._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))
    
    def test_check_isomorphism_triangle_triangle(self):
        triangle1 = LatticeTest(3)
        triangle2 = LatticeTest(3)

        pvim1 = PolygonVertexIncidenceMatrix(triangle1._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(triangle2._nodes_list)

        self.assertTrue(Isomorphism._check_isomorphism(pvim1, pvim2))

    def test_check_isomorphism_triangle_quad(self):
        triangle    = LatticeTest(3)
        quad        = LatticeTest(4)

        pvim1 = PolygonVertexIncidenceMatrix(triangle._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(quad._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))

    def test_check_isomorphism_triangle_hex(self):
        triangle    = LatticeTest(3)
        hex         = LatticeTest(6)

        pvim1 = PolygonVertexIncidenceMatrix(triangle._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(hex._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))

    def test_check_isomorphism_bowtie_bowtie(self):
        bowtie1 = ShapeHelpers.bowtie()
        bowtie2 = ShapeHelpers.bowtie()

        pvim1 = PolygonVertexIncidenceMatrix(bowtie1._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(bowtie2._nodes_list)

        self.assertTrue(Isomorphism._check_isomorphism(pvim1, pvim2))


    def test_check_isomorphism_bowtie_quad(self):
        bowtie  = ShapeHelpers.bowtie()
        quad    = LatticeTest(4)

        pvim1 = PolygonVertexIncidenceMatrix(bowtie._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(quad._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))

    
    def test_check_isomorphism_post_glued_edge_quad_tri_tri(self):
        shape1  = ShapeHelpers.glued_edge_quad_tri()
        tri     = LatticeTest(3)

        pvim1 = PolygonVertexIncidenceMatrix(shape1._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(tri._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))


    def test_check_isomorphism_post_glued_edge_quad_tri_true(self):
        shape1 = ShapeHelpers.glued_edge_quad_tri()
        shape2 = ShapeHelpers.glued_edge_quad_tri()

        pvim1 = PolygonVertexIncidenceMatrix(shape1._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(shape2._nodes_list)

        self.assertTrue(Isomorphism._check_isomorphism(pvim1, pvim2))


    def test_check_isomorphism_filled_bowtie_bowtie(self):
        filled_bowtie = ShapeHelpers.filled_bowtie()
        bowtie        = ShapeHelpers.bowtie()

        pvim1 = PolygonVertexIncidenceMatrix(filled_bowtie._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(bowtie._nodes_list)
        
        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))


    def test_check_isomorphism_filled_bowtie_bowtie_true(self):
        filled_bowtie1 = ShapeHelpers.filled_bowtie()
        filled_bowtie2 = ShapeHelpers.filled_bowtie()

        pvim1 = PolygonVertexIncidenceMatrix(filled_bowtie1._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(filled_bowtie2._nodes_list)

        self.assertTrue(Isomorphism._check_isomorphism(pvim1, pvim2))

    def test_check_isomorphism_filled_bowtie_fish(self):
        filled_bowtie = ShapeHelpers.filled_bowtie()
        fish          = ShapeHelpers.glued_edge_tri_tri_glued_vertex_tri()

        pvim1 = PolygonVertexIncidenceMatrix(filled_bowtie._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(fish._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))

    def test_check_isomorphism_snake_tri_tri_tri(self):
        snake = ShapeHelpers.snake()
        tris  = ShapeHelpers.glue_one_vertex_tri_tri_tri()

        pvim1 = PolygonVertexIncidenceMatrix(snake._nodes_list)
        pvim2 = PolygonVertexIncidenceMatrix(tris._nodes_list)

        self.assertFalse(Isomorphism._check_isomorphism(pvim1, pvim2))

# #------------------------------------------- step 6 ------------------------------------------------------
#     # simple shape
#     # no change required
#     # pizza
#     # chain of three triangles
#     # shoelace

#     def test_check_row_index_vectors_tri(self):
#         tri = LatticeTest(3)
#         tri_pvim = PolygonVertexIncidenceMatrix(tri._nodes_list)

#         Isomorphism._sort_rows(tri_pvim)
#         Isomorphism._sort_cols(tri_pvim)
#         Isomorphism._break_row_ties(tri_pvim)
#         Isomorphism._break_col_ties(tri_pvim)
#         Isomorphism._similarity_col_sort(tri_pvim)

#         Isomorphism._check_row_index_vectors(tri_pvim)

#         expected = [
#             [True],
#             [True],
#             [True]
#         ]

#         self.assertEqual(expected, tri_pvim._matrix)

#     def test_check_row_index_vectors_quad_tri_edge(self):
#         shape = ShapeHelpers.glued_edge_quad_tri()

#         pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

#         Isomorphism._sort_rows(pvim)
#         Isomorphism._sort_cols(pvim)
#         Isomorphism._break_row_ties(pvim)
#         Isomorphism._break_col_ties(pvim)
#         Isomorphism._similarity_col_sort(pvim)

#         Isomorphism._check_row_index_vectors(pvim)

#         CTrue = True
#         expected = [
#             [CTrue, CTrue],
#             [CTrue, CTrue],
#             [CTrue, False],
#             [CTrue, False],
#             [False, CTrue]
#         ]

#         self.assertEqual(expected, pvim._matrix)

#     def test_check_row_vectors_pizza(self):
#         pizza = ShapeHelpers.pizza()
#         pizza_pvim = PolygonVertexIncidenceMatrix(pizza._nodes_list)
        
#         Isomorphism._sort_rows(pizza_pvim)
#         Isomorphism._sort_cols(pizza_pvim)
#         Isomorphism._break_row_ties(pizza_pvim)
#         Isomorphism._break_col_ties(pizza_pvim)

#         Isomorphism._similarity_col_sort(pizza_pvim)
#         Isomorphism._check_row_index_vectors(pizza_pvim)

#         print(pizza_pvim)

#         CTrue = True
#         expected = [
#             [CTrue, CTrue, CTrue, False, False, False],
#             [CTrue, CTrue, False, CTrue, False, False],
#             [CTrue, False, CTrue, False, CTrue, False],
#             [CTrue, False, False, CTrue, False, CTrue],
#             [CTrue, False, False, False, CTrue, CTrue],
#             [False, CTrue, False, False, False, False],
#             [False, False, CTrue, False, False, False],
#             [False, False, False, CTrue, False, False],
#             [False, False, False, False, CTrue, False],
#             [False, False, False, False, False, CTrue],
#         ]

#         self.assertEqual(expected, pizza_pvim._matrix)

#     def test_check_row_index_vectors_shoelace_bow(self):
#         lace_bow = ShapeHelpers.glue_one_vertex_tri_tri_seg_seg()

#         lace_bow_pvim = PolygonVertexIncidenceMatrix(lace_bow._nodes_list)

#         Isomorphism._sort_rows(lace_bow_pvim)
#         Isomorphism._sort_cols(lace_bow_pvim)
#         Isomorphism._break_row_ties(lace_bow_pvim)
#         Isomorphism._break_col_ties(lace_bow_pvim)
#         Isomorphism._similarity_col_sort(lace_bow_pvim)

#         Isomorphism._check_row_index_vectors(lace_bow_pvim)

#         CTrue = True
#         expected = [
#             [CTrue, CTrue, CTrue, CTrue],
#             [CTrue, False, False, False],
#             [CTrue, False, False, False],
#             [False, CTrue, False, False],
#             [False, CTrue, False, False],
#             [False, False, CTrue, False],
#             [False, False, False, CTrue]
#         ]

#         self.assertEqual(expected, lace_bow_pvim._matrix)

#     def test_check_row_index_vectors_three_triangle_chain(self):
#         snake = ShapeHelpers.snake()
#         snake_pvim = PolygonVertexIncidenceMatrix(snake._nodes_list)

#         Isomorphism._sort_rows(snake_pvim)
#         Isomorphism._sort_cols(snake_pvim)
#         Isomorphism._break_row_ties(snake_pvim)
#         Isomorphism._break_col_ties(snake_pvim)
#         Isomorphism._similarity_col_sort(snake_pvim)

#         Isomorphism._check_row_index_vectors(snake_pvim)

#         CTrue = True
#         expected = [
#             [CTrue, CTrue, False],
#             [CTrue, False, CTrue],
#             [CTrue, False, False],
#             [False, CTrue, False],
#             [False, CTrue, False],
#             [False, False, CTrue],
#             [False, False, CTrue]
#         ]

#         self.assertEqual(expected, snake_pvim._matrix)

#     #------------------------------------------- Isomorph In List ---------------------------------------------
#     #empty list                                    x
#     #one item in list, isomorphic                  x
#     #one item in list, not isomorphic              x
#     #normal size list, something in is isomorphic  x
#     #normal size list, not isomorphic              x
#     #try with a glued shape as well                x
#     def test_isomorph_in_list_empty_list(self):
#         self.assertFalse(Isomorphism.isomorph_in_list([], LatticeTest(3)))

#     def test_isomorph_in_list_one_item_isomorphic(self):
#         l1 = LatticeTest(3)
#         tl = LatticeTest(3)

#         self.assertTrue(Isomorphism.isomorph_in_list([l1], tl))
    
#     def test_isomorph_in_list_one_item_not_isomorphic(self):
#         l1 = LatticeTest(4)
#         tl = LatticeTest(3)

#         self.assertFalse(Isomorphism.isomorph_in_list([l1], tl))

#     def test_isomorph_in_list_normal_size_list_isomorphic(self):
#         l1_list = [
#             LatticeTest(2),
#             LatticeTest(3),
#             LatticeTest(4),
#             LatticeTest(5),
#             LatticeTest(6),
#             LatticeTest(7)
#         ]
#         tl = LatticeTest(6)

#         self.assertTrue(Isomorphism.isomorph_in_list(l1_list, tl))

#     def test_isomorph_in_list_normal_size_list_not_isomorphic(self):
#         l1_list = [
#             LatticeTest(2),
#             LatticeTest(3),
#             LatticeTest(4),
#             LatticeTest(5),
#             LatticeTest(6),
#             LatticeTest(7)
#         ]
#         tl = LatticeTest(8)
        
#         self.assertFalse(Isomorphism.isomorph_in_list(l1_list, tl))

#     def test_isomorph_in_list_post_glued_in(self):
#         l1_list = [
#             LatticeTest(2),
#             LatticeTest(3),
#             ShapeHelpers.bowtie(),
#             LatticeTest(5),
#             LatticeTest(6)
#         ]
#         tl = ShapeHelpers.bowtie()

#         self.assertTrue(Isomorphism.isomorph_in_list(l1_list, tl))

#     def test_isomorph_in_list_post_glued_not_isomorphic(self):
#         l1_list = [
#             LatticeTest(2),
#             LatticeTest(3),
#             ShapeHelpers.bowtie(),
#             LatticeTest(5),
#             LatticeTest(6)
#         ]
#         tl = ShapeHelpers.pentagram()

#         self.assertFalse(Isomorphism.isomorph_in_list(l1_list, tl))

# #------------------------------------------- get col index vector ---------------------------------------------
    # simple shape (quad)
    # glued vertex
    # glued edge
    # filled
    # pizza
    # star
    # fish (glued_edge_tri_tri_glued_vertex_tri)
    def test_get_col_index_vector_quad(self):
        quad = LatticeTest(4)
        quad_pvim = PolygonVertexIncidenceMatrix(quad._nodes_list)

        Isomorphism._sort_rows(quad_pvim)
        Isomorphism._sort_cols(quad_pvim)
        Isomorphism._break_row_ties(quad_pvim)
        Isomorphism._break_col_ties(quad_pvim)
        # [True]
        # [True]
        # [True]
        # [True]

        expected = [0, 1, 2, 3]
        vector = Isomorphism._get_col_index_vector(0, quad_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_bowtie_first_col(self):
        bowtie = ShapeHelpers.bowtie()
        bowtie_pvim = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

        Isomorphism._sort_rows(bowtie_pvim)
        Isomorphism._sort_cols(bowtie_pvim)
        Isomorphism._break_row_ties(bowtie_pvim)
        Isomorphism._break_col_ties(bowtie_pvim)
        # [True, True]
        # [True, False]
        # [True, False]
        # [False, True]
        # [False, True]

        expected = [0, 1, 2]
        vector = Isomorphism._get_col_index_vector(0, bowtie_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_bowtie_second_col(self):
        bowtie = ShapeHelpers.bowtie()
        bowtie_pvim = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

        Isomorphism._sort_rows(bowtie_pvim)
        Isomorphism._sort_cols(bowtie_pvim)
        Isomorphism._break_row_ties(bowtie_pvim)
        Isomorphism._break_col_ties(bowtie_pvim)
        # [True, True]
        # [True, False]
        # [True, False]
        # [False, True]
        # [False, True]

        expected = [0, 3, 4]
        vector = Isomorphism._get_col_index_vector(1, bowtie_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_glued_edge_quad_tri_first_col(self):
        shape = ShapeHelpers.glued_edge_quad_tri()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)
        # [True, True]
        # [True, True]
        # [True, False]
        # [True, False]
        # [False, True]

        expected = [0, 1, 2, 3]
        vector = Isomorphism._get_col_index_vector(0, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_glued_edge_quad_tri_second_col(self):
        shape = ShapeHelpers.glued_edge_quad_tri()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)
        # [True, True]
        # [True, True]
        # [True, False]
        # [True, False]
        # [False, True]

        expected = [0, 1, 4]
        vector = Isomorphism._get_col_index_vector(1, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_vector_filled_bowtie_first_col(self):
        shape = ShapeHelpers.filled_bowtie()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)
        # [True, True, True]
        # [True, True, False]
        # [True, False, True]
        # [False, True, False]
        # [False, False, True]

        expected = [0, 1, 2]
        vector = Isomorphism._get_col_index_vector(0, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_vector_filled_bowtie_second_col(self):
        shape = ShapeHelpers.filled_bowtie()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)
        # [True, True, True]
        # [True, True, False]
        # [True, False, True]
        # [False, True, False]
        # [False, False, True]

        expected = [0, 1, 3]
        vector = Isomorphism._get_col_index_vector(1, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_vector_filled_bowtie_third_col(self):
        shape = ShapeHelpers.filled_bowtie()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)
        # [True, True, True]
        # [True, True, False]
        # [True, False, True]
        # [False, True, False]
        # [False, False, True]

        expected = [0, 2, 4]
        vector = Isomorphism._get_col_index_vector(2, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_pizza(self):
        shape = ShapeHelpers.pizza()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)

        # [True, True, True, True, True, True]
        # [True, True, False, False, False, False]
        # [True, False, False, True, False, False]
        # [False, True, True, False, False, False]
        # [False, False, True, False, False, True]
        # [False, False, False, True, True, False]
        # [False, False, False, False, True, True]
        #
        # different than i would do on paper but it passes 1 through 4 so its fine

        # col 0
        expected = [0, 1, 2]
        vector = Isomorphism._get_col_index_vector(0, shape_pvim)

        self.assertEqual(expected, vector)

        # col 1
        expected = [0, 1, 3]
        vector = Isomorphism._get_col_index_vector(1, shape_pvim)

        self.assertEqual(expected, vector)

        # col 2
        expected = [0, 3, 4]
        vector = Isomorphism._get_col_index_vector(2, shape_pvim)

        self.assertEqual(expected, vector)

        # col 3
        expected = [0, 2, 5]
        vector = Isomorphism._get_col_index_vector(3, shape_pvim)

        self.assertEqual(expected, vector)

        # col 4
        expected = [0, 5, 6]
        vector = Isomorphism._get_col_index_vector(4, shape_pvim)

        self.assertEqual(expected, vector)

        # col 5
        expected = [0, 4, 6]
        vector = Isomorphism._get_col_index_vector(5, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_index_vector_star(self):
        shape = ShapeHelpers.pentagram()
        shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        Isomorphism._sort_rows(shape_pvim)
        Isomorphism._sort_cols(shape_pvim)
        Isomorphism._break_row_ties(shape_pvim)
        Isomorphism._break_col_ties(shape_pvim)

        print("star")
        for row in shape_pvim._matrix:
            print(row)
        # [True, True, True, False, False, False]
        # [True, True, False, False, True, False]
        # [True, False, True, True, False, False]
        # [True, False, False, True, False, True]
        # [True, False, False, False, True, True]
        # [False, True, False, False, False, False]
        # [False, False, True, False, False, Fasle]
        # [False, False, False, True, False, False]
        # [False, False, False, False, True, False]
        # [False, False, False, False, False, True]

        # col 0
        expected = [0, 1, 2, 3, 4]
        vector = Isomorphism._get_col_index_vector(0, shape_pvim)

        self.assertEqual(expected, vector)

        # col 1
        expected = [0, 1, 5]
        vector = Isomorphism._get_col_index_vector(1, shape_pvim)

        self.assertEqual(expected, vector)

        # col 2
        expected = [0, 2, 6]
        vector = Isomorphism._get_col_index_vector(2, shape_pvim)

        self.assertEqual(expected, vector)

        # col 3
        expected = [2, 3, 7]
        vector = Isomorphism._get_col_index_vector(3, shape_pvim)

        self.assertEqual(expected, vector)

        # col 4
        expected = [1, 4, 8]
        vector = Isomorphism._get_col_index_vector(4, shape_pvim)

        self.assertEqual(expected, vector)

        # col 5
        expected = [3, 4, 9]
        vector = Isomorphism._get_col_index_vector(5, shape_pvim)

        self.assertEqual(expected, vector)

    def test_get_col_vector_fish(self):
        fish = ShapeHelpers.glued_edge_tri_tri_glued_vertex_tri()
        fish_pvim = PolygonVertexIncidenceMatrix(fish._nodes_list)

        Isomorphism._sort_rows(fish_pvim)
        Isomorphism._sort_cols(fish_pvim)
        Isomorphism._break_row_ties(fish_pvim)
        Isomorphism._break_col_ties(fish_pvim)
        # [True, True, False]
        # [True, True, False]
        # [True, False, True]
        # [False, True, False]
        # [False, False, True]
        # [False, False, True]

        # col 0
        expected = [0, 1, 2]
        vector = Isomorphism._get_col_index_vector(0, fish_pvim)

        self.assertEqual(expected, vector)

        # col 1
        expected = [0, 1, 3]
        vector = Isomorphism._get_col_index_vector(1, fish_pvim)

        self.assertEqual(expected, vector)

        # col 2
        expected = [2, 4, 5]
        vector = Isomorphism._get_col_index_vector(2, fish_pvim)

        self.assertEqual(expected, vector)

# #-------------------------------- get similarity vector ---------------------------------
#     # simple shape
#     # bowtie
#     # glued edge
#     # filled bowtie
#     # pizza
#     # star
#     def test_get_similarity_vector_simple_shape(self):
#         tri = LatticeTest(3)
#         tri_pvim = PolygonVertexIncidenceMatrix(tri._nodes_list)

#         Isomorphism._sort_rows(tri_pvim)
#         Isomorphism._sort_cols(tri_pvim)
#         Isomorphism._break_row_ties(tri_pvim)
#         Isomorphism._break_col_ties(tri_pvim)

#         expected = []
#         vector = Isomorphism._get_similarity_vector(0, tri_pvim)

#         self.assertEqual(expected, vector)

#     def test_get_similarity_vector_bowtie_first_col(self):
#         bowtie = ShapeHelpers.bowtie()
#         bowtie_pvim = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

#         Isomorphism._sort_rows(bowtie_pvim)
#         Isomorphism._sort_cols(bowtie_pvim)
#         Isomorphism._break_row_ties(bowtie_pvim)
#         Isomorphism._break_col_ties(bowtie_pvim)

#         expected = [1]
#         vector = Isomorphism._get_similarity_vector(0, bowtie_pvim)

#         self.assertEqual(expected, vector)

#     def test_get_similarity_vector_bowtie_second_col(self):
#         bowtie = ShapeHelpers.bowtie()
#         bowtie_pvim = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

#         Isomorphism._sort_rows(bowtie_pvim)
#         Isomorphism._sort_cols(bowtie_pvim)
#         Isomorphism._break_row_ties(bowtie_pvim)
#         Isomorphism._break_col_ties(bowtie_pvim)

#         expected = []
#         vector = Isomorphism._get_similarity_vector(1, bowtie_pvim)

#         self.assertEqual(expected, vector)

#     def test_get_similarity_vector_glued_edge_quad_tri(self):
#         glued_edge = ShapeHelpers.glued_edge_quad_tri()
#         glued_edge_pvim = PolygonVertexIncidenceMatrix(glued_edge._nodes_list)

#         Isomorphism._sort_rows(glued_edge_pvim)
#         Isomorphism._sort_cols(glued_edge_pvim)
#         Isomorphism._break_row_ties(glued_edge_pvim)
#         Isomorphism._break_col_ties(glued_edge_pvim)

#         # col 0
#         expected = [2]
#         vector = Isomorphism._get_similarity_vector(0, glued_edge_pvim)

#         self.assertEqual(expected, vector)

#         # col 1
#         expected = []
#         vector = Isomorphism._get_similarity_vector(1, glued_edge_pvim)

#         self.assertEqual(expected, vector)

#     def test_get_similarity_vector_filled_bowtie(self):
#         filled_bowtie = ShapeHelpers.filled_bowtie()
#         filled_bowtie_pvim = PolygonVertexIncidenceMatrix(filled_bowtie._nodes_list)

#         Isomorphism._sort_rows(filled_bowtie_pvim)
#         Isomorphism._sort_cols(filled_bowtie_pvim)
#         Isomorphism._break_row_ties(filled_bowtie_pvim)
#         Isomorphism._break_col_ties(filled_bowtie_pvim)

#         # col 0
#         expected = [2, 2]
#         vector = Isomorphism._get_similarity_vector(0, filled_bowtie_pvim)

#         self.assertEqual(expected, vector)

#         # col 1
#         expected = [1]
#         vector = Isomorphism._get_similarity_vector(1, filled_bowtie_pvim)

#         self.assertEqual(expected, vector)

#         # col 2
#         expected = []
#         vector = Isomorphism._get_similarity_vector(2, filled_bowtie_pvim)

#         self.assertEqual(expected, vector)

#     def test_get_similarity_vector_pizza(self):
#         pizza = ShapeHelpers.pizza()
#         pizza_pvim = PolygonVertexIncidenceMatrix(pizza._nodes_list)

#         Isomorphism._sort_rows(pizza_pvim)
#         Isomorphism._sort_cols(pizza_pvim)
#         Isomorphism._break_row_ties(pizza_pvim)
#         Isomorphism._break_col_ties(pizza_pvim)

#         # col 0
#         expected = [2, 1, 2, 1, 1]
#         vector = Isomorphism._get_similarity_vector(0, pizza_pvim)

#         self.assertEqual(expected, vector)

#         # col 1
#         expected = [2, 1, 1, 1]
#         vector = Isomorphism._get_similarity_vector(1, pizza_pvim)

#         self.assertEqual(expected, vector)

#         # col 2
#         expected = [1, 1, 2]
#         vector = Isomorphism._get_similarity_vector(2, pizza_pvim)

#         self.assertEqual(expected, vector)

#         # col 3
#         expected = [2, 1]
#         vector = Isomorphism._get_similarity_vector(3, pizza_pvim)

#         self.assertEqual(expected, vector)

#         # col 4
#         expected = [2]
#         vector = Isomorphism._get_similarity_vector(4, pizza_pvim)

#         self.assertEqual(expected, vector)

#         # col 5
#         expected = []
#         vector = Isomorphism._get_similarity_vector(5, pizza_pvim)

#     def test_get_similarity_vector_star(self):
#         star = ShapeHelpers.pentagram()
#         star_pvim = PolygonVertexIncidenceMatrix(star._nodes_list)

#         Isomorphism._sort_rows(star_pvim)
#         Isomorphism._sort_cols(star_pvim)
#         Isomorphism._break_row_ties(star_pvim)
#         Isomorphism._break_col_ties(star_pvim)

#         # col 0
#         expected = [2, 2, 2, 2, 2]
#         vector = Isomorphism._get_similarity_vector(0, star_pvim)

#         self.assertEqual(expected, vector)

#         # col 1
#         expected = [1, 0, 1, 0]
#         vector = Isomorphism._get_similarity_vector(1, star_pvim)

#         self.assertEqual(expected, vector)

#         # col 2
#         expected = [1, 0, 0]
#         vector = Isomorphism._get_similarity_vector(2, star_pvim)

#         self.assertEqual(expected, vector)

#         #col 3
#         expected = [0, 1]
#         vector = Isomorphism._get_similarity_vector(3, star_pvim)

#         self.assertEqual(expected, vector)

#         # col 4
#         expected = [1]
#         vector = Isomorphism._get_similarity_vector(4, star_pvim)

#         self.assertEqual(expected, vector)

#         # col 5
#         expected = []
#         vector = Isomorphism._get_similarity_vector(5, star_pvim)

#         self.assertEqual(expected, vector)
    
# #-----------------------get next sim group------------------------------------
#     # nothing in it
#     # one entry
#     # first group
#     # second group
#     # last group
#     # at end
#     def test_get_next_sim_group_empty(self):
#         sim_vector = []

#         expected = []
#         group = Isomorphism._get_next_sim_group(0, sim_vector, 0)

#         self.assertEqual(expected, group)

#     def test_get_next_sim_group_one_entry(self):
#         sim_vector = [1]

#         expected = [0]
#         group = Isomorphism._get_next_sim_group(0, sim_vector, 1)

#         self.assertEqual(expected, group)
    
#     def test_get_next_sim_group_first_group(self):
#         sim_vector = [3, 3, 2, 1, 1]

#         expected = [0, 1]
#         group = Isomorphism._get_next_sim_group(0, sim_vector, 3)

#         self.assertEqual(expected, group)

#     def test_get_next_sim_group_second_group(self):
#         sim_vector = [3, 3, 2, 1, 1]

#         expected = [2]
#         group = Isomorphism._get_next_sim_group(2, sim_vector, 2)

#         self.assertEqual(expected, group)

#     def test_get_next_sim_group_last_group(self):
#         sim_vector = [3, 3, 2, 1, 1]

#         expected = [3, 4]
#         group = Isomorphism._get_next_sim_group(3, sim_vector, 1)

#         self.assertEqual(expected, group)

#     def test_get_next_sim_group_at_end(self):
#         sim_vector = [3, 3, 2, 1, 1]

#         expected = []
#         group = Isomorphism._get_next_sim_group(4, sim_vector, 0)

#         self.assertEqual(expected, group)

# #---------------------------- get sim groups -------------------------------
#     # empty
#     # one group
#     # two groups
#     # three groups
#     def test_get_sim_groups_empty(self):
#         sim_vector = []

#         expected = []
#         groups = Isomorphism._get_sim_groups(sim_vector)

#         self.assertEqual(expected, groups)
    
#     def test_get_sim_groups_one_group(self):
#         sim_vector = [1]

#         expected = [[0]]
#         groups = Isomorphism._get_sim_groups(sim_vector)

#         self.assertEqual(expected, groups)

#     def test_get_sim_groups_two_groups(self):
#         sim_vector = [3, 3, 2]

#         expected = [[0, 1], [2]]
#         groups = Isomorphism._get_sim_groups(sim_vector)

#         self.assertEqual(expected, groups)

#     def test_get_sim_groups_three_groups(self):
#         sim_vector = [3, 3, 2, 1, 1]

#         expected = [[0, 1], [2], [3, 4]]
#         groups = Isomorphism._get_sim_groups(sim_vector)

#         self.assertEqual(expected, groups)

# #---------------------------- sort sim group -----------------------------
#     # simple shape (no change)
#     # fish ( what found the problem)
#     # bowtie    
#     # filled bowtie  
#     def test_sort_sim_group_quad(self):
#         quad = LatticeTest(4)
#         quad_pvim = PolygonVertexIncidenceMatrix(quad._nodes_list)

#         Isomorphism._sort_rows(quad_pvim)
#         Isomorphism._sort_cols(quad_pvim)
#         Isomorphism._break_row_ties(quad_pvim)
#         Isomorphism._break_col_ties(quad_pvim)

#         # [True]
#         # [True]
#         # [True]
#         # [True]

#         expected = [
#             [True],
#             [True],
#             [True],
#             [True]
#         ]
#         group = []
#         returned_pvim = Isomorphism._sort_sim_group(0, quad_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#     def test_sort_sim_group_fish(self):
#         shape = ShapeHelpers.glued_edge_tri_tri_glued_vertex_tri()
#         shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

#         Isomorphism._sort_rows(shape_pvim)
#         Isomorphism._sort_cols(shape_pvim)
#         Isomorphism._break_row_ties(shape_pvim)
#         Isomorphism._break_col_ties(shape_pvim)

#         # [True, True, False]
#         # [True, True, false]
#         # [True, False, True]
#         # [False, True, False]
#         # [False, False, True]
#         # [False, False, True]
#         # [2, 1]  [0]     []

#         # col 0
#         expected = [
#             [True, True, False],
#             [True, True, False],
#             [True, False, True],
#             [False, True, False],
#             [False, False, True],
#             [False, False, True]
#         ]

#         group = [0]
#         returned_pvim = Isomorphism._sort_sim_group(0, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#         group = [1]
#         returned_pvim = Isomorphism._sort_sim_group(0, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#         # col 1
#         group = [0]
#         returned_pvim = Isomorphism._sort_sim_group(1, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#         # col 2
#         group = []
#         returned_pvim = Isomorphism._sort_sim_group(2, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#     def test_sort_sim_group_bowtie(self):
#         shape = ShapeHelpers.bowtie()
#         shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

#         Isomorphism._sort_rows(shape_pvim)
#         Isomorphism._sort_cols(shape_pvim)
#         Isomorphism._break_row_ties(shape_pvim)
#         Isomorphism._break_col_ties(shape_pvim)

#         # [True, True]
#         # [True, False]
#         # [True, False]
#         # [False, True]
#         # [False, True]
#         # [1]     []

#         # col 0
#         expected = [
#             [True, True],
#             [True, False],
#             [True, False],
#             [False, True],
#             [False, True]
#         ]

#         group = [0]
#         returned_pvim = Isomorphism._sort_sim_group(0, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#         # col 1
#         group = []
#         returned_pvim = Isomorphism._sort_sim_group(1, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#     def test_sort_sim_group_filled_bowtie(self):
#         shape = ShapeHelpers.filled_bowtie()
#         shape_pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

#         Isomorphism._sort_rows(shape_pvim)
#         Isomorphism._sort_cols(shape_pvim)
#         Isomorphism._break_row_ties(shape_pvim)
#         Isomorphism._break_col_ties(shape_pvim)

#         # from print
#         # [True, True, True]
#         # [True, True, False]
#         # [True, False, True]
#         # [False, True, False]
#         # [False, False, True]
#         # [2, 2]  [1]    []

#         # col 0
#         # no change
#         expected = [
#             [True, True, True],
#             [True, True, False],
#             [True, False, True],
#             [False, True, False],
#             [False, False, True] # fine bc we haven't gotten to step 6 yet
#         ]

#         group = [0, 1]
#         returned_pvim = Isomorphism._sort_sim_group(0, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#         # col 1
#         group = []
#         returned_pvim = Isomorphism._sort_sim_group(1, shape_pvim, group)

#         self.assertEqual(expected, returned_pvim._matrix)

#---------------------------- similarity col sort ---------------------------
    # triangle
    # bowtie
    # star
    # pizza
    # def test_similarity_col_sort_triangle(self):
    #     triangle = LatticeTest(3)
    #     triangle_pvim = PolygonVertexIncidenceMatrix(triangle._nodes_list)

    #     Isomorphism._sort_rows(triangle_pvim)
    #     Isomorphism._sort_cols(triangle_pvim)
    #     Isomorphism._break_row_ties(triangle_pvim)
    #     Isomorphism._break_col_ties(triangle_pvim)
    #     Isomorphism._similarity_col_sort(triangle_pvim)

    #     # [True],
    #     # [True],
    #     # [True]
    #     # []

    #     expected = [
    #         [True],
    #         [True],
    #         [True]
    #     ]

    #     self.assertEqual(expected, triangle_pvim._matrix)

    # def test_similarity_col_sort_bowtie(self):
    #     bowtie = ShapeHelpers.bowtie()
    #     bowtie_pvim = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

    #     Isomorphism._sort_rows(bowtie_pvim)
    #     Isomorphism._sort_cols(bowtie_pvim)
    #     Isomorphism._break_row_ties(bowtie_pvim)
    #     Isomorphism._break_col_ties(bowtie_pvim)

    #     print("----------------------BEFORE-------------------------")
    #     print(bowtie_pvim)

    #     Isomorphism._similarity_col_sort(bowtie_pvim)

    #     print("----------------------AFTER-------------------------")
    #     print(bowtie_pvim)

    #     expected = [
    #         [True, True],
    #         [True, False],
    #         [True, False],
    #         [False, True],
    #         [False, True]
    #     ]

    #     self.assertEqual(expected, bowtie_pvim._matrix)

    # def test_similarity_col_sort_star(self):
    #     star = ShapeHelpers.pentagram()
    #     star_pvim = PolygonVertexIncidenceMatrix(star._nodes_list)

    #     Isomorphism._sort_rows(star_pvim)
    #     Isomorphism._sort_cols(star_pvim)
    #     Isomorphism._break_row_ties(star_pvim)
    #     Isomorphism._break_col_ties(star_pvim)

    #     print("------------------------BEFORE--------------------")
    #     print(star_pvim)

    #     Isomorphism._similarity_col_sort(star_pvim)

    #     print("----------------------AFTER-------------------------")
    #     print(star_pvim)

    #     #self.assertEqual(expected, star_pvim._matrix)

    # def test_similarity_col_sort_pizza(self):
    #     pizza = ShapeHelpers.pizza()
    #     pizza_pvim = PolygonVertexIncidenceMatrix(pizza._nodes_list)

    #     Isomorphism._sort_rows(pizza_pvim)
    #     Isomorphism._sort_cols(pizza_pvim)
    #     Isomorphism._break_row_ties(pizza_pvim)
    #     Isomorphism._break_col_ties(pizza_pvim)
        
    #     print("------------------------BEFORE--------------------")
    #     print(pizza_pvim)

    #     Isomorphism._similarity_col_sort(pizza_pvim)

    #     print("----------------------AFTER-------------------------")
    #     print(pizza_pvim)


    #     # self.assertEqual(expected, pizza_pvim._matrix)

    # takes an array of col lengths
    # returns start and end (inclusive) indices for tied sections
    # no ties (all singles)
    # entire thing tied
    # >1 tie at end
    # empty list
    # mixed single and multi tied
    # def test_col_sum_get_groups_no_ties(self):
    #     groups = Isomorphism._col_sum_get_groups([2, 3, 4, 5, 6, 7, 8])
    #     expected = [[0, 0], [1, 1], [2,2], [3,3], [4,4], [5,5], [6,6]]
    #     self.assertEqual(expected, groups)

    # def test_col_sum_get_groups_one_tie(self):
    #     groups = Isomorphism._col_sum_get_groups([2, 2, 2, 2, 2])
    #     expected = [[0, 4]]
    #     self.assertEqual(expected, groups)

    # def test_col_sum_get_groups_end(self):
    #     groups = Isomorphism._col_sum_get_groups([2, 3, 4, 5, 6, 6, 6])
    #     expected = [[0, 0], [1, 1], [2,2], [3,3], [4,6]]
    #     self.assertEqual(expected, groups)

    # def test_col_sum_get_groups_empty(self):
    #     groups = Isomorphism._col_sum_get_groups([])
    #     expected = []
    #     self.assertEqual(expected, groups)

    # def test_col_sum_get_groups_mixed(self):
    #     groups = Isomorphism._col_sum_get_groups([2, 3, 3, 3, 6, 7, 7])
    #     expected = [[0, 0], [1, 3], [4,4], [5, 6]]
    #     self.assertEqual(expected, groups)
    
    # # takes an index and colsum list
    # # gives the end (inclusive) to a single group
    # # end index
    # # single in a group
    # # multiple in a group
    # def test_col_sum_get_next_group_end(self):
    #     group = Isomorphism._col_sum_get_next_group(4, [2, 3, 4, 5, 6])
    #     expected = 4
    #     self.assertEqual(expected, group)

    # def test_col_sum_get_next_group_single(self):
    #     group = Isomorphism._col_sum_get_next_group(2, [2, 3, 4, 5, 6])
    #     expected = 2
    #     self.assertEqual(expected, group)

    # def test_col_sum_get_next_group_multiple(self):
    #     group = Isomorphism._col_sum_get_next_group(0, [2, 2, 2, 2, 6])
    #     expected = 3
    #     self.assertEqual(expected, group)

    # # end index
    # # single in group
    # # multiple in group
    # def test_get_col_sum_ties_end(self):
    #     pass
    # def test_get_col_sum_ties_single(self):
    #     pass
    # def test_get_col_sum_ties_multiple(self):
    #     pass

    # # pass in...
    # # no ties (all singles)
    # # tie but it is less than 3 columns (tie between 2)
    # # tie in over >=3 cols
    # # tie not in over <3
    # def test_get_col_vector_ties_no_ties(self):
    #     pass
    # def test_get_col_vector_ties_tie_under_three(self):
    #     pass
    # def test_get_col_vector_ties_tie_in_over_three(self):
    #     pass
    # def test_get_col_vector_ties_tie_not_in_over_three(self):
    #     pass

    # # start > end
    # # end not in pvim
    # # start = end
    # # no movement required
    # # movement required
    # def test_similarity_col_sort_start_past_end(self):
    #     pass
    # def test_similarity_col_sort_end_iob(self):
    #     pass
    # def test_similarity_col_sort_start_iob(self):
    #     pass
    # def test_similarity_col_sort_start_equals_end(self):
    #     pass
    # def test_similarity_col_sort_normal_no_movement(self):
    #     pass
    # def test_similarity_col_sort_normal_yes_movement(self):
    #     pass

    # #def test_similarity_col_sort_manager(self):
    # #    pass






    # def test_stuff_to_print(self):
        # print("bowtie")
        # shape = ShapeHelpers.bowtie()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("filled bowtie")
        # shape = ShapeHelpers.filled_bowtie()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("quad edge glue tri")
        # shape = ShapeHelpers.glued_edge_quad_tri()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("quad vertex glue segment")
        # shape = ShapeHelpers.glued_vertex_segment_quad()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("two triangles edge glued together")
        # shape = ShapeHelpers.glued_edge_tri_tri()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("two triangles vertex glued to the same vertex of a quad")
        # shape = ShapeHelpers.glued_vertex_tri_tri_quad()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("three triangles glued at the same vertex")
        # shape = ShapeHelpers.glue_one_vertex_tri_tri_tri()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("shoelace bow")
        # shape = ShapeHelpers.glue_one_vertex_tri_tri_seg_seg()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("5 pointed star made of 5 tri and 1 pentagon")
        # shape = ShapeHelpers.pentagram()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("funky shape")
        # shape = ShapeHelpers.funky_shape()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("glue edge three quads in a row, then fill gap to curl in")
        # shape = ShapeHelpers.filled_glued_edge_quad_quad_quad()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")
        
        # print("pizza")
        # shape = ShapeHelpers.pizza()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("goofy shape")
        # shape = ShapeHelpers.goofy_shape()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("fill gap on single quad with a quad")
        # shape = ShapeHelpers.filled_quad()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("fish with vertical")
        # shape = ShapeHelpers.glued_edge_tri_tri_glued_vertex_tri()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("fish with horizontal")
        # shape = ShapeHelpers.complex_fish()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("snake")
        # shape = ShapeHelpers.snake()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")

        # print("tri with quad edge glued to each edge")
        # shape = ShapeHelpers.tri_with_quad_on_each_edge()
        # pvim = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # Isomorphism._process_matrix(pvim)

        # print("---------------------------------------------------")


if __name__ == "__main__":
    unittest.main()