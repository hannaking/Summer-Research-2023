# unit test for PolygonVertexIncidenceMatrix
# cleaned + commented 7/14

import sys
import unittest

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')
 
from polygon_vertex_incidence_matrix import PolygonVertexIncidenceMatrix
from lattice_test import LatticeTest
from shape_helpers import ShapeHelpers

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

CTRUE = True # used to help me see the matrix easier. constants have a (slightly) different
#              color and this also makes True the same length as False so the cells line up

class TestPolygonVertexIncidenceMatrix(unittest.TestCase):
# functions:
#  - get_row, a helper for initializing the matrix
#  - swap rows
#  - swap columns
#  - row sum
#  - col sum
#  - dimensions of matrix
#  - __str__ override

#----------------------------------------- get_row ------------------------------------------------
    # v_node not a Node
    # v_node not a vertex node in nodes list
    # simple shape (triangle) - row will always be [True] for simple shapes
    # glued edge, but the vertex is on one shape and not the other
    # glued vertex, but the vertex is on one shape and not the other
    # glued edge, but the vertex is on both shapes
    # glued vertex, but the vertex is on both shapes
    #
    # have to initialize to use _get_row, so ignore the pvim for these tests.
    # init is technically not tested yet at this point
    def test_get_row_not_node(self):
        l1 = LatticeTest(3)
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        with self.assertRaises(Exception):
            matrix._get_row("not-a-node-merely-a-string", l1._nodes_list)
        
    def test_get_row_not_vertex_node(self):
        l1 = LatticeTest(3)
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        with self.assertRaises(Exception):
            matrix._get_row(l1._top_node, l1._nodes_list)

    def test_get_row_simple_shape(self):
        l1 = LatticeTest(3)
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        v_node = l1._bot_node.get_parents()[0]

        expected    = [CTRUE]
        row         = matrix._get_row(v_node, l1._nodes_list)

        self.assertEqual(row, expected)

    def test_get_row_glued_edge_but_on_only_one_shape(self):
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        edge1 = l1._top_node.get_children()[0].get_children()[0]
        edge2 = l2._top_node.get_children()[0].get_children()[0]

        shape = l1.glue_edge(edge1, l2, edge2)
        glued_edge = shape._testing_node_2
        lone_vertex = None
        
        for v in shape._nodes_list[VERTEX_LATTICE_LAYER]:
            if v not in glued_edge.get_children():
                lone_vertex = v

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        expected    = [CTRUE, False]
        found_row   = matrix._get_row(lone_vertex, shape._nodes_list)

        self.assertCountEqual(expected, found_row)

    def test_get_row_glued_vertex_but_on_only_one_shape(self):
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        vertex1 = l1._bot_node.get_parents()[0]
        vertex2 = l2._bot_node.get_parents()[0]
        
        shape = l1.glue_vertex(vertex1, l2, vertex2)
        glued_vertex = shape._testing_node_2
        lone_vertex = None
        
        for v in shape._nodes_list[VERTEX_LATTICE_LAYER]:
            if v is not glued_vertex:
                lone_vertex = v

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        expected = [CTRUE, False]
        found_row = matrix._get_row(lone_vertex, shape._nodes_list)

        self.assertCountEqual(expected, found_row)
        
    def test_get_row_glued_edge_on_both(self):
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        edge1 = l1._top_node.get_children()[0].get_children()[0]
        edge2 = l2._top_node.get_children()[0].get_children()[0]

        shape = l1.glue_edge(edge1, l2, edge2)
        glued_edge = shape._testing_node_2
        vertex = None
        
        for v in shape._nodes_list[VERTEX_LATTICE_LAYER]:
            if v in glued_edge.get_children():
                vertex = v

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        expected    = [CTRUE, CTRUE]
        found_row   = matrix._get_row(vertex, shape._nodes_list)

        self.assertCountEqual(expected, found_row)

    def test_get_row_glued_vertex_on_both(self):
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        vertex1 = l1._bot_node.get_parents()[0]
        vertex2 = l2._bot_node.get_parents()[0]
        
        shape = l1.glue_vertex(vertex1, l2, vertex2)
        glued_vertex = shape._testing_node_2

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        expected = [CTRUE, CTRUE]
        found_row = matrix._get_row(glued_vertex, shape._nodes_list)

        self.assertCountEqual(expected, found_row)

#--------------------------------------- initializing ---------------------------------------------
# info: in case we do more complex test cases, we must first figure out the order that the shape nodes are in
# (print them out to see), then build the expected indicence matrix using that order.
# this is because we need to match the expected to the order of the false, true, falses inside of the matrix
# it hasn't been processed so we need to go by what the shapes order is
    # line segment
    # triangle
    # glued vertex (bowtie)
    # one glued edge
    # snake
    # all edges glued onto (tri-quad-quad-quad)
    # ---
    def test_init_line_segment(self):
        seg = LatticeTest(2)

        expected = [
            [CTRUE],
            [CTRUE]
        ]
        got = PolygonVertexIncidenceMatrix(seg._nodes_list)

        # check dimensions are correct
        # assert we have correct num of rows
        self.assertEqual(len(got._matrix), len(expected)) 
        
        # assert we have correct num of columns
        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0])) 

        self.assertCountEqual(expected, got._matrix)
    
  #     /\
  #    /__\
    def test_init_triangle(self):
        tri = LatticeTest(3)

        expected = [
            [CTRUE],
            [CTRUE],
            [CTRUE]
        ]
        got = PolygonVertexIncidenceMatrix(tri._nodes_list)

        # check dimensions are correct
        # assert we have correct num of rows
        self.assertEqual(len(got._matrix), len(expected)) 
        
        # assert we have correct num of columns
        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0])) 

        self.assertCountEqual(expected, got._matrix)

  # *       *
  # |\     /|
  # | \   / |
  # |  \ /  |
  # |   *   |
  # |  / \  |
  # | /   \ |
  # |/     \|
  # *       *
    def test_init_glued_vertex_triangles(self):
        shape = ShapeHelpers.bowtie()

        expected = [
            [CTRUE, False],
            [CTRUE, False],
            [CTRUE, CTRUE],
            [False, CTRUE],
            [False, CTRUE]
        ]
        got = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # check dimensions are correct
        # assert we have correct num of rows
        self.assertEqual(len(got._matrix), len(expected)) 

        # assert we have correct num of columns
        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0])) 

        self.assertCountEqual(expected, got._matrix)
        
  #    *
  #   /|\
  #  / | \
  # *--*--*
    def test_init_glued_edge_triangles(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        expected = [
            [CTRUE, False],
            [CTRUE, CTRUE],
            [CTRUE, CTRUE],
            [False, CTRUE]
        ]
        got = PolygonVertexIncidenceMatrix(shape._nodes_list)
        
        # check dimensions are correct
        self.assertEqual(len(got._matrix), len(expected))

        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0]))
        
        self.assertCountEqual(expected, got._matrix)

  # .        .____.
  # |\      /|\   |
  # | \    / | \  |
  # |  \  /  |  \ |
  # |___\/___|   \|
    def test_init_glued_triangle_snake(self):
        shape = ShapeHelpers.snake()

        # in order shape 2, 1, 3
        expected = [ 
            [False, CTRUE, False],
            [False, CTRUE, False],
            [CTRUE, CTRUE, False],
            [CTRUE, False, False],
            [CTRUE, False, CTRUE],
            [False, False, CTRUE],
            [False, False, CTRUE],
        ]
        got = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # check dimensions are correct
        # assert we have correct num of rows
        self.assertEqual(len(got._matrix), len(expected)) 

        # assert we have correct num of columns
        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0])) 

        self.assertCountEqual(expected, got._matrix)

  #          *   *
  #         / \ / \
  #        /   *   \ 
  #       *\  / \ /*         
  #          *---*
  #          |   |
  #          *---*
    def test_init_glued_on_all_sides(self):
        shape = ShapeHelpers.tri_with_quad_on_each_edge()

        expected = [
            [False, CTRUE, False, False],
            [False, CTRUE, False, False],
            [CTRUE, CTRUE, CTRUE, False],
            [False, False, CTRUE, False],
            [False, False, CTRUE, False],
            [CTRUE, False, CTRUE, CTRUE],
            [False, False, False, CTRUE],
            [False, False, False, CTRUE],
            [CTRUE, CTRUE, False, CTRUE]         
        ]

        got = PolygonVertexIncidenceMatrix(shape._nodes_list)
        # check dimensions are correct
        # assert we have correct num of rows
        self.assertEqual(len(got._matrix), len(expected))

        # assert we have correct num of columns
        for i in got._matrix:
            self.assertEqual(len(i), len(expected[0]))

        self.assertCountEqual(expected, got._matrix)

#---------------------------------------- row_swap ------------------------------------------------
    # first two
    # last two
    # negative index
    # non-int index
    # out-of-range index
    # same index
    def test_row_swap_first_two_rows(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        matrix.row_swap(0, 1)

        expected = [
            [CTRUE, CTRUE],
            [CTRUE, CTRUE]
        ]

        got = matrix._matrix[0:2]
        
        self.assertEqual(expected, got)

    def test_row_swap_last_two_rows(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        matrix.row_swap(2, 3)

        expected = [
            [False, CTRUE],
            [CTRUE, False]
        ]
        
        got = matrix._matrix[2:4]
        
        self.assertEqual(expected, got)


    def test_row_swap_negative_int(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        with self.assertRaises(Exception):
            matrix.row_swap(-1, 0)


    def test_row_swap_not_an_int(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        with self.assertRaises(Exception):
            matrix.row_swap("1", 0)

    def test_row_swap_index_exceeds_row_size(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        
        with self.assertRaises(Exception):
            matrix.row_swap(1, 18912)

    def test_row_swap_same_row(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        
        matrix.row_swap(0, 0)

        expected = [[CTRUE, CTRUE]]

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)
        got = matrix._matrix[0:1]
        
        self.assertEqual(expected, got)
        
#---------------------------------------- col_swap ------------------------------------------------
    # first two
    # last two
    # negative int
    # non-int
    # out of range
    # same index
    def test_col_swap_first_two_cols(self):
        shape = ShapeHelpers.bowtie()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # before swap, it looks like:
        # [True, True]
        # [True, False]
        # [True, False]
        # [False, True]
        # [False, True]

        matrix.col_swap(0, 1)

        expected = [
            [CTRUE, CTRUE],
            [False, CTRUE],
            [False, CTRUE],
            [CTRUE, False],
            [CTRUE, False]
        ]

        got = matrix._matrix
        
        self.assertEqual(expected, got)

    def test_col_swap_last_two_cols(self):
        shape = ShapeHelpers.tri_with_quad_on_each_edge()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        # before swap:
        # [True, True, False, True]
        # [True, True, True, False]
        # [True, False, True, True]
        # [False, True, False, False]
        # [False, True, False, False]
        # [False, False, True, False]
        # [False, False, True, False]
        # [False, False, False, True]
        # [False, False, False, True]

        matrix.col_swap(2, 3)  # swap last two cols

        expected = [
            [CTRUE, CTRUE, CTRUE, False],
            [CTRUE, CTRUE, False, CTRUE],
            [CTRUE, False, CTRUE, CTRUE],
            [False, CTRUE, False, False],
            [False, CTRUE, False, False],
            [False, False, False, CTRUE],
            [False, False, False, CTRUE],
            [False, False, CTRUE, False],
            [False, False, CTRUE, False]
        ]

        got = matrix._matrix
        
        self.assertEqual(expected, got)

    def test_col_swap_negative_int(self):
        shape = shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        with self.assertRaises(Exception):
            matrix.col_swap(-1, 0)

    def test_col_swap_not_an_int(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        with self.assertRaises(Exception):
            matrix.col_swap(1, 'a')

    def test_col_swap_index_exceeds_col_size(self):
        shape = ShapeHelpers.glued_edge_tri_tri()
        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        with self.assertRaises(Exception):
            matrix.col_swap(1, 123094)

    def test_col_swap_same_col(self):
        shape = ShapeHelpers.glued_edge_tri_tri()

        before = PolygonVertexIncidenceMatrix(shape._nodes_list)

        after = PolygonVertexIncidenceMatrix(shape._nodes_list)
        after.col_swap(0, 0)

        self.assertTrue(before._matrix == after._matrix)

#-------------------------------------- row_sum -------------------------------------------#
    # triangle
    # quadrilateral
    # glued vertex quad tri tri
    # pizza
    # three quads filled with a fourth quad
    def test_row_sum_triangle(self):
        l1 = LatticeTest(3)

        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        number_of_rows = matrix.dimensions()[0]

        got = []
        for i in range(number_of_rows):
            got.append(matrix.row_sum(i))

        expected = [1, 1, 1]

        self.assertCountEqual(expected, got)

    def test_row_sum_quad(self):
        l1 = LatticeTest(4)

        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        number_of_rows = matrix.dimensions()[0]

        got = []
        for i in range(number_of_rows):
            got.append(matrix.row_sum(i))

        expected = [1, 1, 1, 1]

        self.assertCountEqual(expected, got)

    def test_row_sum_two_triangles_glued_to_quad_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        number_of_rows = matrix.dimensions()[0]

        got = []
        for i in range(number_of_rows):
            got.append(matrix.row_sum(i))

        expected = [1, 1, 1, 3, 1, 1, 1, 1]

        self.assertCountEqual(expected, got)

    def test_row_sum_pizza(self):
        filled_lattice = ShapeHelpers.pizza()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        number_of_rows = matrix.dimensions()[0]

        got = []
        for i in range(number_of_rows):
            got.append(matrix.row_sum(i))

        expected = [2, 2, 2, 2, 2, 2, 6]

        self.assertCountEqual(expected, got)
        
    def test_row_sum_four_rectangles_filled(self):
        filled_lattice = ShapeHelpers.filled_glued_edge_quad_quad_quad()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        number_of_rows = matrix.dimensions()[0]

        got = []
        for i in range(number_of_rows):
            got.append(matrix.row_sum(i))

        expected = [2, 2, 3, 3, 1, 2, 2, 1]

        self.assertCountEqual(expected, got)

#------------------------------------- col_sum --------------------------------------------#
    # triangle
    # quadrilateral
    # pizza
    # three quads filled with a fourth quad
    # line seg to quad by vertex
    def test_col_sum_triangle(self):
        l1 = LatticeTest(3)

        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [3]

        self.assertCountEqual(expected, got)

    def test_col_sum_quad(self):
        l1 = LatticeTest(4)

        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [4]

        self.assertCountEqual(expected, got)

    def test_col_sum_two_triangles_glued_to_shape_by_one_vertex(self):
        shape = ShapeHelpers.glued_vertex_tri_tri_quad()

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [4, 3, 3]

        self.assertCountEqual(expected, got)

    def test_col_sum_pizza(self):
        filled_lattice = ShapeHelpers.pizza()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [3, 3, 3, 3, 3, 3]

        self.assertCountEqual(expected, got)
        
    def test_col_sum_four_rectangles_filled(self):
        filled_lattice = ShapeHelpers.filled_glued_edge_quad_quad_quad()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [4, 4, 4, 4]

        self.assertCountEqual(expected, got)

    def test_col_sum_line_seg_by_vertex_to_quad(self):
        shape = ShapeHelpers.glued_vertex_segment_quad()

        matrix = PolygonVertexIncidenceMatrix(shape._nodes_list)

        number_of_cols = matrix.dimensions()[1]

        got = []
        for i in range(number_of_cols):
            got.append(matrix.col_sum(i))

        expected = [4, 2]

        self.assertCountEqual(expected, got)

#----------------------------------- dimensions -------------------------------------------#
    # triangle
    # quadrilateral
    # bowtie
    # pizza
    def test_dimensions_triangle(self):
        l1 = LatticeTest(3)
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        self.assertEqual(matrix.dimensions(), [3, 1])

    def test_dimensions_quadrilateral(self):
        l1 = LatticeTest(4)
        matrix = PolygonVertexIncidenceMatrix(l1._nodes_list)

        self.assertEqual(matrix.dimensions(), [4, 1])

    def test_dimensions_bowtie(self):
        bowtie = ShapeHelpers.bowtie()

        matrix = PolygonVertexIncidenceMatrix(bowtie._nodes_list)

        self.assertEqual(matrix.dimensions(), [5, 2])

    def test_dimensions_pizza(self):
        filled_lattice = ShapeHelpers.pizza()

        matrix = PolygonVertexIncidenceMatrix(filled_lattice._nodes_list)

        self.assertEqual(matrix.dimensions(), [7, 6])

if __name__ == "__main__":
    unittest.main()