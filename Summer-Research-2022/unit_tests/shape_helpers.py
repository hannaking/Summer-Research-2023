import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from lattice_test import LatticeTest

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class ShapeHelpers():

    # *----*----*----*
    # |    |    |    |
    # *----*----*----*
    #       \  /
    #        \/
    @staticmethod 
    def seesaw():
        sq1 = LatticeTest(4)

        next_shape = LatticeTest(4)
        e1 = sq1._nodes_list[EDGE_LATTICE_LAYER][0]
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue1 = sq1.glue_edge(e1, next_shape, e2)

        next_shape = LatticeTest(4)
        e1 = glue1.get_node_from_label("8E0")
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue2 = glue1.glue_edge(e1, next_shape, e2)

        next_shape = LatticeTest(3)
        e1 = glue2.get_node_from_label("9E00")
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue3 = glue2.glue_edge(e1, next_shape, e2)

        return glue3

    #   .____.____.
    #  /|    |    |
    #  \|____|____|
    #   |    |
    #   |____|
    @staticmethod
    def blimp():
        sq1 = LatticeTest(3)

        next_shape = LatticeTest(4)
        e1 = sq1._nodes_list[EDGE_LATTICE_LAYER][0]
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue1 = sq1.glue_edge(e1, next_shape, e2)

        next_shape = LatticeTest(4)
        e1 = glue1.get_node_from_label("9E1")
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue2 = glue1.glue_edge(e1, next_shape, e2)

        next_shape = LatticeTest(4)
        e1 = glue2.get_node_from_label("8E10")
        e2 = next_shape._nodes_list[EDGE_LATTICE_LAYER][0]
        glue3 = glue2.glue_edge(e1, next_shape, e2)

        return glue3



    # *       *
    # |\     /|
    # | \   / |
    # |  \ /  |
    # |   *   |
    # |  / \  |
    # | /   \ |
    # |/     \|
    # *       *

    @staticmethod
    def bowtie():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(3)
        vertex_node2 = l2._bot_node.get_parents()[0]
        
        return l1.glue_vertex(vertex_node1, l2, vertex_node2)


    # *       *
    # |\     /|
    # | \   / |
    # |  \ /  |
    # |   X   |
    # |  / \  |
    # | /   \ |
    # |/     \|
    # *-------*

    @staticmethod
    def filled_bowtie():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(3)
        vertex_node2 = l2._bot_node.get_parents()[0]

        bowtie = l1.glue_vertex(vertex_node1, l2, vertex_node2)

        tri = LatticeTest(3)
        
        n1 = None
        n2 = None
        
        for i in bowtie._nodes_list[VERTEX_LATTICE_LAYER]:
            if i._label == "3V0":
                n1 = i
            if i._label == "3V1":
                n2 = i

        return bowtie.fill_gap(n1, tri, n2)


    # *---------*
    # |         |\
    # |         | \
    # |         |  \
    # |         |   \
    # |         |    \
    # *---------*-----*

    @staticmethod
    def glued_edge_quad_tri():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        edge1 = vertex_node1.get_parents()[0]

        l2 = LatticeTest(4)
        vertex_node2 = l2._bot_node.get_parents()[0]
        edge2 = vertex_node2.get_parents()[0]
        
        return l1.glue_edge(edge1, l2, edge2)

    #
    #       *-----* 
    #       |     |
    #       |     |
    # *-----*-----*

    @staticmethod
    def glued_vertex_segment_quad():
        l1 = LatticeTest(4)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(2)
        vertex_node2 = l2._bot_node.get_parents()[0]

        return l1.glue_vertex(vertex_node1, l2, vertex_node2)

    #            *
    #           / \
    #          /   \
    #         /     \
    # *------*-------*
    def glued_vertex_segment_tri():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(2)
        vertex_node2 = l2._bot_node.get_parents()[0]

        return l1.glue_vertex(vertex_node1, l2, vertex_node2)


    #     *
    #    /|\
    #   / | \
    #  /  |  \
    # *---*---*

    @staticmethod
    def glued_edge_tri_tri():
        l1 = LatticeTest(3)
        e1 = l1._nodes_list[EDGE_LATTICE_LAYER][0]

        l2 = LatticeTest(3)
        e2 = l2._nodes_list[EDGE_LATTICE_LAYER][0]
        
        return l1.glue_edge(e1, l2, e2)


    #   *
    #   |\  *-----*
    #   | \ |     |
    #   |  \|     |
    #   *---*-----*
    #      /|
    #     / |
    #    /  |
    #   *---*

    @staticmethod
    def glued_vertex_tri_tri_quad():
        l1 = LatticeTest(4)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(3)
        vertex_node2 = l2._bot_node.get_parents()[0]
        l3 = LatticeTest(3)
        vertex_node3 = l3._bot_node.get_parents()[0]

        post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2)
        new_node = post_glued1._testing_node_2
        
        return post_glued1.glue_vertex(new_node, l3, vertex_node3)

    #   *       *
    #   |\     /|
    #   | \   / |
    #   |  \ /  |
    #   *---*---*
    #      /|
    #     / |
    #    /  |
    #   *---*

    @staticmethod
    def glue_one_vertex_tri_tri_tri():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(3)
        vertex_node2 = l2._bot_node.get_parents()[0]
        l3 = LatticeTest(3)
        vertex_node3 = l3._bot_node.get_parents()[0]

        post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2)
        new_node = post_glued1._testing_node_2
        
        return post_glued1.glue_vertex(new_node, l3, vertex_node3)

    #   *       *
    #   |\     /|
    #   | \   / |
    #   |  \ /  |
    #   *---*---*
    #      / \
    #     /   \
    #    /     \
    #   *       *

    @staticmethod
    def glue_one_vertex_tri_tri_seg_seg():
        l1 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        l2 = LatticeTest(3)
        vertex_node2 = l2._bot_node.get_parents()[0]
        l3 = LatticeTest(2)
        vertex_node3 = l3._bot_node.get_parents()[0]
        l4 = LatticeTest(2)
        vertex_node4 = l4._bot_node.get_parents()[0]

        post_glued = l1.glue_vertex(vertex_node1, l2, vertex_node2)
        new_node = post_glued._testing_node_2
        
        post_glued = post_glued.glue_vertex(new_node, l3, vertex_node3)
        new_node = new_node = post_glued._testing_node_2
        
        return post_glued.glue_vertex(new_node, l4, vertex_node4)
  
  
    #        **
    #       /` \
    # .----/----\----.
    #  `'./      \.'`
    #    /`'.''.'`\
    #   /,-`    `-,\
    #  *`          `*

    @staticmethod
    def pentagram():
        pent = LatticeTest(5)
        t1 = LatticeTest(3)
        t2 = LatticeTest(3)
        t3 = LatticeTest(3)
        t4 = LatticeTest(3)
        t5 = LatticeTest(3)

        e1 = pent._nodes_list[EDGE_LATTICE_LAYER][0]
        e2 = t1._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = pent.glue_edge(e1, t1, e2)

        e1 = shape.get_node_from_label("8E0")
        e2 = t2._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, t2, e2)

        e1 = shape.get_node_from_label("9E00")
        e2 = t3._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, t3, e2)

        e1 = shape.get_node_from_label("11E000")
        e2 = t4._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, t4, e2)

        e1 = shape.get_node_from_label("10E0000")
        e2 = t5._nodes_list[EDGE_LATTICE_LAYER][0]

        return shape.glue_edge(e1, t5, e2)
        

    #                 *
    #                /|\ \
    #               / | \  \ 
    #              /  |  \   \
    #             /   |   \    \
    #            /    |    \     \
    #           *-----*-----*-----*
    #          /|    /      |    /
    #         / |   /       |   /
    #        /  |  /        |  /
    #       /   | /         | /
    #      /    |/          |/
    #     *-----*-----------*

    @staticmethod
    def funky_shape():
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        l3 = LatticeTest(3)
        l4 = LatticeTest(3)
        l5 = LatticeTest(3)
        l6 = LatticeTest(3)
        l7 = LatticeTest(4)

        e1 = l1._nodes_list[EDGE_LATTICE_LAYER][0]
        e2 = l2._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = l1.glue_edge(e1, l2, e2)

        e1 = shape.get_node_from_label("7E1")
        e2 = l3._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, l3, e2)
        
        e1 = shape.get_node_from_label("7E1")
        e2 = l4._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, l4, e2)

        e1 = shape.get_node_from_label("6E000")
        e2 = l5._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, l5, e2)

        e1 = shape.get_node_from_label("7E10")
        e2 = l6._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, l6, e2)

        v1 = shape.get_node_from_label("4V10")
        v2 = shape.get_node_from_label("4V100")

        return shape.fill_gap(v1, l7, v2)


    # __________________
    #|\_______________/|
    #| |             | |
    #| |             | |
    #|_|_____________|_|

    @staticmethod
    def filled_glued_edge_quad_quad_quad():
        l1 = LatticeTest(4)
        e1 = l1._bot_node.get_parents()[0].get_parents()[0]

        l2 = LatticeTest(4)
        e2 = l2._bot_node.get_parents()[0].get_parents()[0]
        
        two_squares = l1.glue_edge(e1, l2, e2)

        l3 = LatticeTest(4)
        e3 = l3._bot_node.get_parents()[0].get_parents()[0]
        next_edge_to_glue = two_squares.get_node_from_label("8E0")

        three_squares = two_squares.glue_edge(next_edge_to_glue, l3, e3)

        l4 = LatticeTest(4)
        start_vertex = three_squares.get_node_from_label("5V10")
        end_vertex = three_squares.get_node_from_label("4V1")

        return three_squares.fill_gap(start_vertex, l4, end_vertex)


    #     *-------*
    #    / \     / \
    #   /   \   /   \
    #  /     \ /     \
    # *-------*-------*
    #  \     / \     /
    #   \   /   \   /
    #    \ /     \ /
    #     *-------*

    @staticmethod
    def pizza():
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        l3 = LatticeTest(3)
        l4 = LatticeTest(3)
        l5 = LatticeTest(3)
        l6 = LatticeTest(3) # last one is the filling shape!

        # glue the first two shapes
        e1 = l1._bot_node.get_parents()[0].get_parents()[0]
        e2 = l2._bot_node.get_parents()[0].get_parents()[0]
        glued_edges = l1.glue_edge(e1, l2, e2)

        # glue the third shape
        e3 = l3._bot_node.get_parents()[0].get_parents()[0]
        glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E1"), l3, e3)

        # # glue the fourth shape
        e4 = l4._bot_node.get_parents()[0].get_parents()[0]
        glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("7E00"), l4, e4)
        
        # # glue the fifth shape
        e5 = l5._bot_node.get_parents()[0].get_parents()[0]
        glued_edges = glued_edges.glue_edge(glued_edges.get_node_from_label("6E1"), l5, e5)

        # # glue the sixth shape (filling shape)
        v1 = glued_edges.get_node_from_label("4V100")
        v2 = glued_edges.get_node_from_label("4V1")
        return glued_edges.fill_gap(v1, l6, v2)


    #    ____ /\
    #  /|    |  \
    # |\|____|  /
    # |     / \/
    # |    /
    # |   /
    # |  /
    # | /
    # |/

    @staticmethod
    def goofy_shape():
        l1 = LatticeTest(3)
        l2 = LatticeTest(4)
        l3 = LatticeTest(5)
        l4 = LatticeTest(4)

        e1 = l1._nodes_list[EDGE_LATTICE_LAYER][0]
        e2 = l2._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = l1.glue_edge(e1, l2, e2)

        e1 = shape.get_node_from_label("8E1")
        e2 = l3._nodes_list[EDGE_LATTICE_LAYER][0]
        shape = shape.glue_edge(e1, l3, e2)

        v1 = shape.get_node_from_label("4V00")
        v2 = shape.get_node_from_label("4V10")
        return shape.fill_gap(v1, l4, v2)


    #  * 
    #  |\\     
    #  | \ \
    #  |  \  \ 
    #  |   *--*
    #  |      |
    #  *------*

    @staticmethod
    def filled_quad():
        l1 = LatticeTest(4)
        v1 = l1._nodes_list[VERTEX_LATTICE_LAYER][0]
        v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][1]
        if l1.is_connected(v1, v2):
            v2 = l1._nodes_list[VERTEX_LATTICE_LAYER][2]

        tri = LatticeTest(3) 

        return l1.fill_gap(v1, tri, v2)

    #    *    *
    #   /|\  /|
    #  / | \/ |
    #  \ | /\ |
    #   \|/  \|
    #    *    *

    @staticmethod
    def glued_edge_tri_tri_glued_vertex_tri():
        l1 = LatticeTest(3)
        vertex_nodes1 = l1._bot_node.get_parents()
        vertex_node1 = vertex_nodes1[0]
        edges1 = vertex_node1.get_parents()
        edge_node1 = edges1[0]

        l2 = LatticeTest(3)
        vertex_nodes2 = l2._bot_node.get_parents()
        vertex_node2 = vertex_nodes2[0]
        edges2 = vertex_node2.get_parents()
        edge_node2 = edges2[0]
        post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

        vertex_to_glue = post_glued._bot_node.get_parents()[2]

        l3 = LatticeTest(3)
        vertex = l3._bot_node.get_parents()[0]

        return post_glued.glue_vertex(vertex_to_glue, l3, vertex)

    #        *     *
    #       / \   /|
    #      /   \ / |
    #     *-----*  |
    #      \   / \ |
    #       \ /   \|
    #        *     *

    @staticmethod
    def complex_fish():
        l1 = LatticeTest(3)
        vertex_nodes1 = l1._bot_node.get_parents()
        vertex_node1 = vertex_nodes1[0]
        edges1 = vertex_node1.get_parents()
        edge_node1 = edges1[0]

        l2 = LatticeTest(3)
        vertex_nodes2 = l2._bot_node.get_parents()
        vertex_node2 = vertex_nodes2[0]
        edges2 = vertex_node2.get_parents()
        edge_node2 = edges2[0]
        post_glued = l1.glue_edge(edge_node1, l2, edge_node2)

        v2 = post_glued.get_node_from_label("2V0")

        l3 = LatticeTest(3)
        vertex = l3._bot_node.get_parents()[0]

        return post_glued.glue_vertex(v2, l3, vertex)

    # .        .____.
    # |\      /|\   |
    # | \    / | \  |
    # |  \  /  |  \ |
    # |___\/___|   \|

    @staticmethod
    def snake():
        l1 = LatticeTest(3)
        l2 = LatticeTest(3)
        l3 = LatticeTest(3)
        vertex_node1 = l1._bot_node.get_parents()[0]
        vertex_node2 = l2._bot_node.get_parents()[0]
        vertex_node3 = l3._bot_node.get_parents()[0]

        post_glued1 = l1.glue_vertex(vertex_node1, l2, vertex_node2) # /_\/_\ two triangle glued lattice
        post_glued1_vertex = post_glued1._bot_node.get_parents()[0]
        if len(post_glued1_vertex.get_parents()) == 4:
            post_glued1_vertex = post_glued1._bot_node.get_parents()[1] # we DON'T want the one with 4 parents

        return post_glued1.glue_vertex(post_glued1_vertex, l3, vertex_node3) # now we have all three


    #          *   *
    #         / \ / \
    #        /   *   \ 
    #       *\  / \ /*         
    #          *---*
    #          |   |
    #          *---*

    @staticmethod
    def tri_with_quad_on_each_edge():
        tri = LatticeTest(3)

        for i in range(3):
            label1 = str(i + 2) + "V" + ''.join(['0'] * i)
            label2 = str(i + 3 if i < 2 else 2) + "V" + ''.join(['0'] * i)
            edge = (tri.get_node_from_label(label1), tri.get_node_from_label(label2))
            tri = tri.fill_gap(edge[0], LatticeTest(4), edge[1])

        return tri