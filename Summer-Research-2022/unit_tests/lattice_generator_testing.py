import unittest
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from lattice_test       import LatticeTest
from lattice_generator  import *
from shape_helpers      import *

class TestLatticeGenerator(unittest.TestCase):

    def test_init_not_a_list(self):
        with self.assertRaises(TypeError):
            LatticeGenerator(1)

    def test_init_empty_list(self):
        ss1 = LatticeGenerator([])

        for list in ss1._shape_list:
            self.assertEqual(len(list), 0)

    def test_init_list_too_big(self):
        with self.assertRaises(ValueError):
            # pretty huge list
            LatticeGenerator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37])

    def test_init_triangle(self):
        ss1 = LatticeGenerator([0, 1])

        self.assertEqual(len(ss1._shape_list), 7)
        self.assertEqual(len(ss1._shape_list[0]), 0)
        self.assertEqual(len(ss1._shape_list[1]), 1)

        # confirm shape is a triangle by counting vertices
        self.assertEqual(len(ss1._shape_list[1][0]._geo_graph.nodes()), 3)

        for list in ss1._shape_list:
            for item in list:
                self.assertTrue(isinstance(item, Lattice))

    def test_init_two_triangles(self):
        ss1 = LatticeGenerator([0, 2])

        self.assertEqual(len(ss1._shape_list), 7)
        self.assertEqual(len(ss1._shape_list[0]), 0)
        self.assertEqual(len(ss1._shape_list[1]), 2)

        # confirm shapes are a triangle by counting vertices
        self.assertEqual(len(ss1._shape_list[1][0]._geo_graph.nodes()), 3)
        self.assertEqual(len(ss1._shape_list[1][1]._geo_graph.nodes()), 3)

        for list in ss1._shape_list:
            for item in list:
                self.assertTrue(isinstance(item, Lattice))

    #@-------------------------@#

    #@
    #@       see lattice_isomorphism_testing.py for matrix stuff
    #@

    #@----- Glue Vertices -----@#
    #@-------------------------@#

    def test_glue_vertices_triangle_and_segment(self):
        ss1 = LatticeGenerator([1, 1])

        segment     = ss1._shape_list[0][0]
        triangle    = ss1._shape_list[1][0]

        queue = [segment, triangle]

        list = ss1._glue_vertices(triangle, queue)

        # assert that all 3 combinations are in the list
        self.assertEqual(len(list), 2)
        
        # assert that the segment is glued to a different vertex each time
        # this also asserts that each vertex in the tri is glued to
        # while looping through the list, we can also assert that each item is a Lattice object

        visited_nodes = []
        for figure in list:

            self.assertTrue(isinstance(figure, Lattice))
            glued_node = figure.get_glued_node()

            self.assertTrue(glued_node not in visited_nodes)
            visited_nodes.append(glued_node)

    def test_glue_vertices_triangle_and_triangle(self):
        ss1 = LatticeGenerator([0, 2])

        triangle1 = ss1._shape_list[1][0]
        triangle2 = ss1._shape_list[1][1]

        # put one of each unique shape into queue
        queue = [triangle1, triangle2]

        list = ss1._glue_vertices(triangle1, queue)

        # assert that all 3 combinations are in the list
        self.assertEqual(len(list), 3)

        # assert that the segment is glued to a different vertex each time
        # this also asserts that each vertex in the tri is glued to
        # while looping through the list, we can also assert that each item is a Lattice object

        visited_nodes = []
        for figure in list:
                
            self.assertTrue(isinstance(figure, Lattice))
            glued_node = figure.get_glued_node()

            #figure._geo_graph.show()

            self.assertTrue(glued_node not in visited_nodes)
            visited_nodes.append(glued_node)

    def test_glue_vertices_triangle_and_quad_and_octagon(self):
        ss1 = LatticeGenerator([0, 1, 1, 0, 0, 0, 1])

        triangle = ss1._shape_list[1][0]
        octagon  = ss1._shape_list[6][0]
        quad     = ss1._shape_list[2][0]

        queue = [triangle, octagon, quad]

        list = ss1._glue_vertices(octagon, queue)

        # assert that all 16 combinations are in the list
        self.assertEqual(len(list), 7)

        visited_nodes = []
        for figure in list:
            self.assertTrue(isinstance(figure, Lattice))
            glued_node = figure.get_glued_node()

            #figure._geo_graph.show()

            self.assertTrue(glued_node not in visited_nodes)
            visited_nodes.append(glued_node)

    #@----------------------@#
    #@----- Glue Edges -----@#
    #@----------------------@#

    #@ Find Valid Pairs @#
    #@------------------@#

    def test_find_valid_pairs_two_triangles(self):
        ss1 = LatticeGenerator([0, 2])

        triangle1 = ss1._shape_list[1][0]
        triangle2 = ss1._shape_list[1][1]

        pairs = ss1._find_valid_pairs(triangle1, triangle2)
        
        labels = []
        for pair in pairs:
            pair_labels = []
            
            for node in pair:
                pair_labels.append(node._label)

            labels.append(set(pair_labels))

        expected = [
            set(["3V", "2V"]),
            set(["2V", "4V"]),
            set(["3V", "4V"])
        ]

        self.assertCountEqual(expected, labels)

        for pair in pairs:
            self.assertTrue(pair[0] in triangle1._nodes_list[VERTEX_LATTICE_LAYER])
            self.assertTrue(pair[1] in triangle1._nodes_list[VERTEX_LATTICE_LAYER])

    def test_find_valid_pairs_quad_and_tri(self):
        ss1 = LatticeGenerator([0, 1, 1, 0, 0, 0, 1])

        triangle = ss1._shape_list[1][0]
        quad     = ss1._shape_list[2][0]

        pairs = ss1._find_valid_pairs(quad, triangle)

        labels = []
        for pair in pairs:
            pair_labels = []
            
            for node in pair:
                pair_labels.append(node._label)

            labels.append(set(pair_labels))

        expected = [
            set(["3V", "2V"]),
            set(["2V", "4V"]),
            set(["3V", "4V"]),
            set(["2V", "5V"]),
            set(["3V", "5V"]),
            set(["4V", "5V"])
        ]

        self.assertCountEqual(expected, labels)

        for pair in pairs:
            self.assertTrue(pair[0] in quad._nodes_list[VERTEX_LATTICE_LAYER])
            self.assertTrue(pair[1] in quad._nodes_list[VERTEX_LATTICE_LAYER])

    #@ Glue Each Pair @#
    #@----------------@#

    def test_glue_each_pair_two_triangles(self):
        ss1 = LatticeGenerator([0, 2])

        triangle1 = ss1._shape_list[1][0]
        triangle2 = ss1._shape_list[1][1]

        # print("now doing all triangle-triangle glue each pairs")
        glued_pairs = ss1._glue_each_pair(triangle1, triangle2)

        self.assertEqual(len(glued_pairs), 3)

    def test_glue_each_pair_quad_and_tri(self):
        ss1 = LatticeGenerator([])

        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        # print("now doing all quad-triangle glue each pairs")
        glued_pairs = ss1._glue_each_pair(triangle, quad)

        self.assertEqual(len(glued_pairs), 6)

#----------------------------individually gluing all possible pairs outside of the sweatshop---------------------

    def test_all_of_them_in_sequence(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)
#-----------------------------------------------------
        v1 = "2V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 2 
#-----------------------------------------------------
        v1 = "2V"
        v2 = "5V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 5
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #5 2
#-----------------------------------------------------
        v1 = "2V"
        v2 = "4V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 4
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #4 2 
#-----------------------------------------------------
        v1 = "5V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #5 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 5 
#-----------------------------------------------------
        v1 = "4V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #4 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 4 
#-----------------------------------------------------
        v1 = "5V"
        v2 = "4V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #5 4
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #4 5 


#-------------------------------------------------- Glue Along Every Edge -------------------------------------------------#

    def test_glue_along_every_edge_two_triangles(self):
        ss1 = LatticeGenerator([0, 2])

        triangle1 = ss1._shape_list[1][0]
        triangle2 = ss1._shape_list[1][1]

        glued_pairs = ss1._glue_along_every_edge(triangle1, [triangle2])

        self.assertEqual(len(glued_pairs), 3)

    def test_glue_along_every_edge_quad_and_tri(self):
        ss1 = LatticeGenerator([])

        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        glued_pairs = ss1._glue_along_every_edge(triangle, [quad])

        self.assertEqual(len(glued_pairs), 6)

    def test_glue_along_every_edge_tri_and_quad(self):
        ss1 = LatticeGenerator([])

        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        glued_pairs = ss1._glue_along_every_edge(quad, [triangle])

        self.assertEqual(len(glued_pairs), 3)

    def test_glue_along_every_edge_tri_and_bowtie(self):
        ss1 = LatticeGenerator([])

        bowtie = ShapeHelpers.bowtie()
        triangle = LatticeTest(3)

        glued_pairs = ss1._glue_along_every_edge(triangle, [bowtie])

        self.assertEqual(len(glued_pairs), 10)

        #@ Debug
        # glued_pairs = Isomorphism.filter_isomorphic(glued_pairs)
        # for pair in glued_pairs:
        #     pair._geo_graph.show()


#----------------------------------------------------- Glue Shapes -------------------------------------------------

    def test_glue_individually_2v_3v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "2V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 2 

        # print("Individually: 2v 3v")
        # v1v2.show()

        # print("Individually: 3v 2v")
        # v2v1.show()

    def test_glue_individually_4v_3v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "4V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #4 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 4 

        # print("Individually: 4v 3v")
        # v1v2.show()

        # print("Individually: 3v 4v")
        # v2v1.show()

    def test_glue_individually_5v_3v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "5V"
        v2 = "3V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #5 3
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #3 5 

        # print("Individually: 5v 3v")
        # v1v2.show()

        # print("Individually: 3v 5v")
        # v2v1.show()

    def test_glue_individually_2v_4v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "2V"
        v2 = "4V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 4
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #4 2 

        # print("Individually: 2v 4v")
        # v1v2.show()

        # print("Individually: 4v 2v")
        # v2v1.show()

    def test_glue_individually_5v_4v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "5V"
        v2 = "4V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #5 4
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #4 5 

        # print("Individually: 5v 4v")
        # v1v2.show()

        # print("Individually: 4v 5v")
        # v2v1.show()

    def test_glue_individually_2v_5v(self):
        triangle = LatticeTest(3)
        quad     = LatticeTest(4)

        v1 = "2V"
        v2 = "5V"

        pairs = [
            [quad.get_node_from_label(v1), quad.get_node_from_label(v2)],
            [quad.get_node_from_label(v2), quad.get_node_from_label(v1)]
        ]

        v1v2 = quad.fill_gap(pairs[0][0], triangle, pairs[0][1])   #2 5
        v2v1 = quad.fill_gap(pairs[1][0], triangle, pairs[1][1])   #5 2

        # print("Individually: 2v 5v")
        # v1v2.show()

        # print("Individually: 5v 2v")
        # v2v1.show()

    #----------------------------------------------------- Glue All -------------------------------------------------

    def test_glue_shapes_tri(self):
        ss = LatticeGenerator([])
        
        test_matrix_tuple = (LatticeTest(3), [0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 6)

        expected_count = [0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_tri_quad(self):
        ss = LatticeGenerator([])

        test_matrix_tuple = (LatticeTest(3), [0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 6)
        
        expected_count = [0, 0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_bowtie_tri(self):
        ss = LatticeGenerator([])
        
        bowtie = ShapeHelpers.bowtie()
        test_matrix_tuple = (bowtie, [0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 15)

        expected_count = [0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_bowtie_quad(self):
        ss = LatticeGenerator([])
        
        bowtie = ShapeHelpers.bowtie()
        test_matrix_tuple = (bowtie, [0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 15)

        expected_count = [0, 0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_segment(self):
        ss = LatticeGenerator([])

        segment = LatticeTest(2)
        test_matrix_tuple = (segment, [0, 1])

        # the input segment is also included in the list
        # will be filtered out later with isomorphism checking
        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 3) #onto each of two points on the segment

        expected_count = [0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_tri_octagon(self):
        ss = LatticeGenerator([])

        tri = LatticeTest(3)
        test_matrix_tuple = (tri, [0, 0, 0, 0, 0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 6)

        expected_count = [0, 0, 0, 0, 0, 0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_quad_octagon(self):
        ss = LatticeGenerator([])

        quad = LatticeTest(4)
        test_matrix_tuple = (quad, [0, 0, 0, 0, 0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 10)

        expected_count = [0, 0, 0, 0, 0, 0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_tri_hexagon(self):
        ss = LatticeGenerator([])

        tri = LatticeTest(3)
        test_matrix_tuple = (tri, [0, 0, 0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 6)

        expected_count = [0, 0, 0, 0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_octagon_tri(self):
        ss = LatticeGenerator([])

        octagon = LatticeTest(8)
        test_matrix_tuple = (octagon, [0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 24)

        expected_count = [0, 0]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    def test_glue_all_tri_tri_quad(self):
        ss = LatticeGenerator([])

        tri = LatticeTest(3)
        test_matrix_tuple = (tri, [0, 1, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 12) #because only one layer at a time, so only two-shape combos

        expected_count_1 = [0, 0, 1]
        expected_count_2 = [0, 1, 0]
        count1 = 0
        count2 = 0
        for shape in glued_shapes:
            if shape[1] == expected_count_1: count1 += 1
            if shape[1] == expected_count_2: count2 += 1

        self.assertEqual(count1, 6)
        self.assertEqual(count2, 6)

    #test with a value >1 in the []
    def test_glue_all_two_tris(self):
        ss = LatticeGenerator([])

        tri = LatticeTest(3)
        test_matrix_tuple = (tri, [0, 2])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        self.assertEqual(len(glued_shapes), 6)

        expected_count = [0, 1]
        for shape in glued_shapes:
            self.assertEqual(shape[1], expected_count)

    #----------------------------------------------------- Add All Uniquely -------------------------------------------------

    def test_add_all_uniquely_tri(self):
        ss = LatticeGenerator([])

        tri = LatticeTest(3)
        test_matrix_tuple = (tri, [0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        lm = LatticeMatrix(2)
        lm.add_all_uniquely(1, glued_shapes)

        self.assertEqual(len(lm._lattice_matrix[1]), 2)

    def test_add_all_uniquely_tri_quad(self):
        ss = LatticeGenerator([])

        test_matrix_tuple = (LatticeTest(3), [0, 0, 1])

        glued_shapes = ss.glue_all(test_matrix_tuple)

        lm = LatticeMatrix(2)
        lm.add_all_uniquely(1, glued_shapes)

        self.assertEqual(len(lm._lattice_matrix[1]), 2)

    def test_add_all_uniquely_quad_tri_extra_layer(self):
        ss = LatticeGenerator([])

        # Layer 0
        #---------
        test_matrix_tuple = (Lattice(3), [0, 2])

        lm = LatticeMatrix(3)
        lm.add_all_uniquely(0, [test_matrix_tuple])

        # Layer 1
        #---------
        glued_shapes = []
        for shape in lm._lattice_matrix[0]:
            glued_shapes.extend(ss.glue_all(shape))

        #@ assertion @#
        for shape in glued_shapes:
            self.assertEqual(len(shape[0]._nodes_list[SHAPE_LATTICE_LAYER]), 2)
        #@-----------@#

        lm.add_all_uniquely(1, glued_shapes)

        #@ assertion @#
        self.assertEqual(len(lm._lattice_matrix[1]), 2)
        #@-----------@#

        # Layer 2
        #---------
        glued_shapes_2 = []
        for shape_tuple in lm._lattice_matrix[1]:
            glued_shapes_2.extend(ss.glue_all(shape_tuple))

        #@ assertion @#
        for shape in glued_shapes_2:
            self.assertEqual(len(shape[0]._nodes_list[SHAPE_LATTICE_LAYER]), 3)
        #@-----------@#

        lm.add_all_uniquely(2, glued_shapes_2)
        
        #@ assertion @#
        self.assertEqual(len(lm._lattice_matrix[2]), 6)
        #@-----------@#

    #----------------------------------------------------- Glue Matrix Layer One-------------------------------------------------

    def test_glue_matrix_layer_one_tri(self):
        ss = LatticeGenerator([])

        test_matrix_tuple = (Lattice(3), [0, 2])

    #----------------------------------------------------- Glue Shapes -------------------------------------------------

    # def test_glue_shapes_three_quads(self):

    #     ss = LatticeGenerator([0, 3])

    #     shapes = ss.glue_shapes()

    #     #print(len(shapes))

    #     ohno_shape = shapes._lattice_matrix[2][5][0]

    #     print('start of ohno shape')

    #     new_pvim = PolygonVertexIncidenceMatrix(ohno_shape._nodes_list)

    #     Isomorphism._process_matrix(new_pvim)

    #     # #4v1 5v1

    def test_glue_shapes_two_tris(self):
        ss = LatticeGenerator([0, 3, 0])

        shapes = ss.glue_shapes()

        for layer in shapes._lattice_matrix:

            for shape in layer:

                shape[0]._geo_graph.show()

        #self.assertEqual(len(shapes), 3)

    # def test_glue_shapes_three_tris(self):
    #     ss = LatticeGenerator([0, 3])

    #     shapes = ss.glue_shapes()

    #     self.assertEqual(len(shapes), 9)

    # def test_glue_shapes_tri_quad(self):
    #     ss = LatticeGenerator([0, 1, 1])

    #     shapes = ss.glue_shapes()

    #     self.assertEqual(len(shapes), 5)

    # def test_glue_shapes_two_quads(self):
    #     ss = LatticeGenerator([0, 0, 2])

    #     shapes = ss.glue_shapes()

    #     self.assertEqual(len(shapes), 4)

    # def test_glue_shapes_three_quads(self):
    #     ss = LatticeGenerator([0, 0, 3])

    #     shapes = ss.glue_shapes()


if __name__ == "__main__":
    unittest.main()