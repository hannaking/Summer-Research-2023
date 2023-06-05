# Inherits from Lattice, used to force / check specific shapes for unit testing. 
# Does the same things, just with trackers on what has been glued
#
# attributes:
#   - _testing_node_0
#   - _testing_node_1
#   - _testing_node_2
#   - _testing_v1
#   - _testing_v2
#   - _testing_glued_edges
#
# functions:
#   - init
#   - fill_gap
#   - glue_edges
#   - _get_current_shape_edges
#   - glue_rest_of_edges
#   - glue_edge
#   - glue_vertex

from lattice import Lattice
from node import Node
from geometry_graph import GeometryGraph
import copy

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class LatticeTest(Lattice):
    def __init__(self, size):
        super().__init__(size)
        
        # handle vertices < 2 (negative numbers, 0, 1) and non-integer vertices
        # these are not valid shapes and cannot become lattices
        if (size < 2 or int(size) != size):
            raise Exception("Lattice size must be greater than 2")

        #@ for testing purposes only
        self._testing_node_0 = None
        self._testing_node_1 = None
        self._testing_node_2 = None
        self._testing_v1 = None
        self._testing_v2 = None
        self._testing_glued_edges = []

    # weeds out exceptions and non-fill-gap glueing attempts
    # and identifies where we will be glueing by calling find_shortest_path and convert_to_edge_path
    #     returns result of glue vertex call if the gap you try to fill is a single vertex
    #     returns result of glue edge call if the gap you try to fill is one edge

    # if you try to glue something that would force a 3D shape (would need space between two shapes like a sail),
    # it just glues a random edge. this will be filtered out when the results of the generator are checked for isomorphism

    # at the bottom, calls the glue_edges method to actually glue into the gap
    #
    # node_u - start point on self lattice
    # node_v - end point on self lattice
    # lattice_v - lattice to glue onto th epath between node_u and node_v
    #
    # returns Lattice
    #
    # throws exception if...
    #                      node_u is not a Node object
    #                      node_v is not a Node object
    #                      node_u is not a vertex node on self lattice
    #                      node_v is not a vertex node on self lattice
    #                      lattice_to_fill is self (you cannot glue a lattice to itself)
    #                      lattice_to_fill is not a simple single shape
    #                      node_u is not an exterior point in the shape
    #                      node_v is not an exterior point in the shape
    #                      you are trying to glue onto a side that has already been glued onto
    #                             to avoid # *-----*-----*
                                           # |     | \   |
                                           # |     |  \  |
                                           # *-----*---\-*
                                           #        \   \
                                           #         *---*
    #                      the simple shape filling the gap does not have enough sides to fill the path
    #                               path length must be < the number of edges lattice_to_fill has
    def fill_gap(self, node_u, lattice_to_fill, node_v):
        # Filter out exceptions
        #-----------------------
        if not isinstance(node_u, Node):
            raise Exception("node_u input is not a Node object.")

        if not isinstance(node_v, Node):
            raise Exception("node_v input is not a Node object.")

        if node_u not in self._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("node_u is not a vertex element of the self lattice.")

        if node_v not in self._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("node_v is not a vertex element of the self lattice.")
        
        if self is lattice_to_fill:
            raise Exception("You cannot fill with yourself.") 

        num_shape_nodes = len(lattice_to_fill._nodes_list[SHAPE_LATTICE_LAYER])
        if num_shape_nodes != 1:
            raise Exception("The input lattice is not a simple shape.")

        # if filling at a point, it is just a vertex glue
        # pick any point on lattice_to_fill, it doesn't matter which
        # leave
        if node_u is node_v:
            return self.glue_vertex(node_u, lattice_to_fill, lattice_to_fill._nodes_list[VERTEX_LATTICE_LAYER][0])

        if node_u not in self._geo_graph.get_perimeter().nodes:
            raise Exception("Node u is not an exterior node.")

        if node_v not in self._geo_graph.get_perimeter().nodes:
            raise Exception("Node v is not an exterior node.")

        #---------------------done with exceptions-------------------------#
        #find shortest path btwn u and v
        shortest_path_vertices = self.find_shortest_path(node_u, node_v)

        shortest_path = self.convert_to_edge_path(shortest_path_vertices)

        # check you have no interior edges on your path (already glued onto before)
        for edge in shortest_path:
            if len(edge.get_parents()) > 1:
                raise Exception("There is already a shape glued onto one of the edges :(")

        # if we have only one segment, then we will call glue_edge to glue only along that one edge
        if len(shortest_path) == 1:
            lattice_to_fill_edge = lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER][0]
            #@ testing!!!!
            testing_return_this_in_full_file = self.glue_edge(shortest_path[0], lattice_to_fill, lattice_to_fill_edge) 
            
            return testing_return_this_in_full_file

        #if node_u and node_v are already connected, you cannot do this. it is the three-tri-but-it-looks-like-two-because-they-stacked thing
        for parent in node_u.get_parents():
            if node_v in parent.get_children():
                lattice_to_fill_edge = lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER][0]
                # need to return something, so just glue onto the first edge. 
                # it will get filtered out later
                return self.glue_edge(shortest_path[0], lattice_to_fill, lattice_to_fill_edge)     

        #check that path length < the number of edges lattice_to_fill has
        # (you can't proceed if the path is the same length or longer than the shape's # of edges)
        num_edges_of_shape = len(lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER])
        if len(shortest_path) >= num_edges_of_shape:
            raise Exception("The length of the path was too large. Choose a smaller path or a larger shape.")

        #@ testing purposes only. flag both nodes so we can get them after we fill
        node_u.flag()
        node_v.flag()

        # now we fill the gap.
        new_lattice = self.glue_edges(shortest_path, lattice_to_fill)
        
        # for testing purposes only. get the nodes we flagged. neither of them are supposed to be in particular order
        self._testing_v1 = self._find_flagged_node(VERTEX_LATTICE_LAYER)
        self._testing_v2 = self._find_flagged_node(VERTEX_LATTICE_LAYER)

        return new_lattice

    # does the actual gluing along an identified path of more than one edge
    # process:
    #      copy the lattices and re-identify the path by using the labels
    #      adjust node labels (see node_factory.py for help reading labels)
    #      identify the edges being glued onto that path
    #      cut off top and bottom nodes
    #      smash the lattices
    #      identify the first edge to glue along
    #      merge the vertexes on that edge, then merge the edge itself
    #      glue the rest of the edges with glue rest of edges (need this because one of the vertices will have been glued when it is time to edge-glue each edge)
    #      re-add top and bottom nodes and make the connections
    #      update geo graph
    # 
    # list_of_edges - list of edge nodes to glue along on the self lattice
    # lattice_to_fill - lattice to glue onto the path
    #
    # returns glued Lattice
    #
    # throws exception if lattice_v is not a simple shape
    def glue_edges(self, list_of_edges, lattice_v):
        # make sure lattice v is a simple shape
        if len(lattice_v._top_node.get_children()) > 1:
            raise Exception("The input lattice is not a simple shape.")

        # now, to get those flagged edges, we need to find them in the copy_of_self
        # make copies of both of our lattices
        copy_of_self = copy.deepcopy(self)
        copy_of_lattice_v = copy.deepcopy(lattice_v)

        # find the shortest path edges in the copy in ORDER of what they're supposed to be in
        copied_path_edges = []
        edge_lattice_layer_copy = copy_of_self._nodes_list[EDGE_LATTICE_LAYER]
        i = 0

        while True:  
            next_label_to_find = list_of_edges[i]._label
            i += 1     
            for edge in edge_lattice_layer_copy:
                if edge._label == next_label_to_find:
                    copied_path_edges.append(edge)
            if i >= len(list_of_edges):
                break                
        # now we have the copied_path_edges in the correct order.
            
        for layer in copy_of_self._nodes_list:
            for node in layer:
                node._label += str(0)

        for layer in copy_of_lattice_v._nodes_list:
            for node in layer:
                node._label += str(1)

        # we will also need all edges in copy of lattice v because we'll need them after we smash
        copied_shape_edges = []
        for edge in copy_of_lattice_v._nodes_list[EDGE_LATTICE_LAYER]:
            copied_shape_edges.append(edge)

        # remove top and bottom off both copies (we will add them back after everything)
        copy_of_self._remove_node(copy_of_self._top_node)
        copy_of_self._remove_node(copy_of_self._bot_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._top_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._bot_node)

        # smash here. now the new lattice will be saved in copy_of_self
        copy_of_self = copy_of_self.smash_lattices(copy_of_lattice_v)

        # get first item in shortest path
        current_path_edge = copied_path_edges[0]
        #get any edge on lattice 2 (doesn't matter which one for the first gluing)
        current_shape_edge = copied_shape_edges[0]
        
        #@ FIRST merging. this merge is unique and has a different process than each subsequent merge.
        child0 = current_path_edge.get_children()[0]
        child1 = current_path_edge.get_children()[1]

        child0_v = current_shape_edge.get_children()[0]
        child1_v = current_shape_edge.get_children()[1]

        v1 = copy_of_self._merge(child0, child0_v)
        v2 = copy_of_self._merge(child1, child1_v)
        
        #@ assignment is for testing purposes only. keep the merge in the full file.
        testing_only_delete_later = copy_of_self._merge(current_path_edge, current_shape_edge)

        #@ for testing purposes only
        copy_of_self._testing_glued_edges.append(testing_only_delete_later)
        
        # current_path_edge is still copied_path_edges[0]
        next_path_edge = copied_path_edges[1]


        for i in range(1, len(copied_path_edges)): 

            current_shape_edge = self._get_current_shape_edge(copied_shape_edges, current_path_edge, next_path_edge) #@ new
            current_path_edge = next_path_edge

            if i < len(copied_path_edges) - 1:
                next_path_edge = copied_path_edges[i+1]
                
            else:
                next_path_edge = copied_path_edges[i]

            copy_of_self._glue_rest_of_edges(current_shape_edge, current_path_edge)

        # Add new top and bottom nodes
        #------------------------------
        new_top = self._make_node(TOP_LATTICE_LAYER)
        new_bot = self._make_node(BOTTOM_LATTICE_LAYER)

        copy_of_self._top_node = new_top
        copy_of_self._nodes_list[TOP_LATTICE_LAYER].append(copy_of_self._top_node)
        copy_of_self._bot_node = new_bot
        copy_of_self._nodes_list[BOTTOM_LATTICE_LAYER].append(copy_of_self._bot_node)

        # Connect shape to new top
        #--------------------------
        for shape in copy_of_self._nodes_list[SHAPE_LATTICE_LAYER]:
            copy_of_self._set_nodes(copy_of_self._top_node, shape)

        # Connect vertices to new bottom
        # #------------------------------    
        for vertex in copy_of_self._nodes_list[VERTEX_LATTICE_LAYER]: 
            copy_of_self._set_nodes(vertex, copy_of_self._bot_node)

        # return the new lattice
        copy_of_self._geo_graph = GeometryGraph(copy_of_self)

        return copy_of_self
    
    # the method finds this edge by first finding the vertex between next_path_edge and current_path_edge.
    # this vertex is also connected to the shape edge we want, so we want to find it.
    # it loops through the parents of the vertex between to find the edge that is part of the fill gap shape.
    # that edge is the one that gets returned.
    #
    # shape_edges - a list of all edges that belong to the shape we are filling the gap with
    # current_path_edge - the edge in the path that we are currently gluing with
    # next_path_edge - the edge in the path that we are gluing with next
    #
    # returns the next shape edge we should be working with 
    # #@ NEEDS TO BE UNIT TESTED
    def _get_current_shape_edge(self, shape_edges, current_path_edge, next_path_edge): #@ new

        #get the vertex that connects it to current_path_edge
        vertex_between = None
        for j in next_path_edge.get_children():
            parents = j.get_parents()

            # if this vertex has both the current and prev edge as its parents (aka it's between them), then we want it
            if current_path_edge in parents:
                vertex_between = j
                break

        #get the vertex's parents and make sure the edge we get is part of the second lattice
        for j in vertex_between.get_parents():
            if j in shape_edges:
                current_shape_edge = j
                break

        return current_shape_edge

    # glues an edge and one of the vertex pairs on the edge
    # we need this because in glue edges, one side of the edge will have already been glued down by the previous edge glue
    # this just glues down the other side and the edge itself (like a hinge)
    #
    # process: get all four vertex children of the two edges to be glued
    #          identify the two that have not been glued by removing the two that have
    #          merge these two vertices
    #          merge the edge
    #
    # current_shape_edge - the edge on the shape being glued onto the path
    # current_path_edge - the edge on the path being glued to
    #
    # no return
    #
    # throws exception if the other vertex has not been properly glued previously
    def _glue_rest_of_edges(self, current_shape_edge, current_path_edge):
        
        #@ where the merging happens -------------------------
        child0 = current_path_edge.get_children()[0]
        child1 = current_path_edge.get_children()[1]

        child0_v = current_shape_edge.get_children()[0]
        child1_v = current_shape_edge.get_children()[1]
        
        children = [child0, child1, child0_v, child1_v]

        # this will remove the repeated vertex (aka the just previously glued vertex).
        # it should remove two vertices (because the edges both share this vertex).
        for vertex in children:
            if children.count(vertex) == 2:
                children.remove(vertex)
                children.remove(vertex)

        if len(children) != 2:
            raise Exception("The children of the path and shape edges did not properly remove the previously glued vertex.")
        v1 = children[0]
        v2 = children[1]
        
        # merge the pair of vertices that are connected to the shape edge and path edge.
        # due to the previous check, we know that neither of these are the previously glued vertex.
        self._merge(v1, v2)
        
        # now, we merge the edges themselves.
        #@ remove the assignment in the normal file. just the merge is needed.
        testing_only_delete_later = self._merge(current_path_edge, current_shape_edge)

        #@ for testing purposes only
        self._testing_glued_edges.append(testing_only_delete_later)

    # glue one edge to one other edge
    # process: filter exceptions and self-returns
    #          copy the lattices (flags the nodes in here)
    #          update labels
    #          cut off top and bottom nodes
    #          smash the lattices together
    #          re-identify the nodes to glue by looking for flags (fine bc there is only two nodes to be glued so order doesn't matter)
    #          merge the vertices, then the edge
    #          re-add top and bottom nodes and their connections
    #          update the geo graph
    # 
    # gluing must lead to something that is meaningfully different 
    # (ex no gluing just a vertex onto or a line segment onto the side of a shape)
    #
    # node_u - the edge Node on self to glue onto
    # lattice_v - Lattice to glue onto self
    # node_v - the edge Node on lattice_v to glue onto node_u
    #
    # returns the glued lattice,
    #         self if either Lattice is a line segment (bc gluing must lead to something fundamentally different)
    #
    # throws exception if node_u is not a Node object
    #                     node_v is not a Node object
    #                     node_u is not an edge in self
    #                     node_v is not an edge in lattice_v
    #                     self and lattice_v are the same Lattice object
    #                     node_u or node_v have already been glue onto
    def glue_edge(self, node_u, lattice_v, node_v):
        # Filter out exceptions
        #-----------------------
        if not isinstance(node_u, Node):
            raise Exception("node_u input is not a Node object.")

        if not isinstance(node_v, Node):
            raise Exception("node_v input is not a Node object.")
        
        if node_u not in self._nodes_list[EDGE_LATTICE_LAYER]:
            raise Exception("node_u is not in self.")

        if node_v not in lattice_v._nodes_list[EDGE_LATTICE_LAYER]:
            raise Exception("node_v is not an element of the input lattice.")

        if node_u not in self._nodes_list[EDGE_LATTICE_LAYER] or node_v not in lattice_v._nodes_list[EDGE_LATTICE_LAYER]:
            raise Exception("Input nodes are not isomorphic.")
        
        if self is lattice_v:
            raise Exception("You cannot glue to yourself.")

        if self._vertices == 2:
            return self

        if lattice_v._vertices == 2:
            return lattice_v

        #interior edge (already glued onto before)
        if len(node_u.get_parents()) == 2 or len(node_v.get_parents()) == 2:
            raise Exception("There is already a shape glued onto this edge :(")

        # Make copies of lattices
        #-------------------------
        copy_of_self = self._make_copy_of_lattice(node_u)
        copy_of_lattice_v = lattice_v._make_copy_of_lattice(node_v)

        # append an index representing the lattice to every node's label
        # this is used to make sure that the nodes are unique
        for layer in copy_of_self._nodes_list:
            for node in layer:
                node._label += str(0)

        for layer in copy_of_lattice_v._nodes_list:
            for node in layer:
                node._label += str(1)
                
        # Remove top and bottom nodes
        #-----------------------------

        copy_of_self._remove_node(copy_of_self._top_node)
        copy_of_self._remove_node(copy_of_self._bot_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._top_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._bot_node)

        # Smash lattices into one
        #-------------------------
        copy_of_self = copy_of_self.smash_lattices(copy_of_lattice_v)

        # Get node_u and node_v in the copied lattice
        #---------------------------------------------
        new_u = copy_of_self._find_flagged_node(EDGE_LATTICE_LAYER)
        new_u.unflag()
        # this is right because copy of self IS the smashed lattice
        new_v = copy_of_self._find_flagged_node(EDGE_LATTICE_LAYER)
        new_v.unflag()

        # Make child and parent connections
        #-----------------------------------
        # For each node in downset, add the child and parent connections 
        # from the first lattice to the second lattice

        child0 = new_u.get_children()[0]
        child1 = new_u.get_children()[1]

        child0_v = new_v.get_children()[0]
        child1_v = new_v.get_children()[1]

        copy_of_self._merge(child0, child0_v)
        copy_of_self._merge(child1, child1_v)

        new_u = copy_of_self._merge(new_u, new_v)

        # Add new top and bottom nodes
        #------------------------------
        new_top = self._make_node(TOP_LATTICE_LAYER)
        new_bot = self._make_node(BOTTOM_LATTICE_LAYER)

        copy_of_self._top_node = new_top
        copy_of_self._nodes_list[TOP_LATTICE_LAYER].append(copy_of_self._top_node)
        copy_of_self._bot_node = new_bot
        copy_of_self._nodes_list[BOTTOM_LATTICE_LAYER].append(copy_of_self._bot_node)

        # Connect shape to new top
        #--------------------------
        for shape in copy_of_self._nodes_list[SHAPE_LATTICE_LAYER]:
            copy_of_self._set_nodes(copy_of_self._top_node, shape)

        # Connect vertices to new bottom
        # #------------------------------    
        for vertex in copy_of_self._nodes_list[VERTEX_LATTICE_LAYER]: 
            copy_of_self._set_nodes(vertex, copy_of_self._bot_node)

        #for testing purposes only
        copy_of_self._testing_node_0 = copy_of_self._testing_node_1 
        copy_of_self._testing_node_1 = copy_of_self._testing_node_2
        copy_of_self._testing_node_2 = new_u

        copy_of_self._geo_graph = GeometryGraph(copy_of_self)
        
        return copy_of_self

    # Glue node_u to node_v (They must be vertex nodes)
    # node_u has to be part of the own lattice object
    # the other node must not be part of the own lattice object (you can't glue to yourself)
    # 
    # Glue at two vertex nodes, node_u (from this) and node_v (from the Lattice being glued on)
    # process: flag the vertex nodes you wish to glue at (fine bc there is only two nodes to be glued so order doesn't matter)
    #          copy the lattices (flags the nodes in here)
    #          cut off the top and bottom nodes
    #          re-identify the nodes to glue by looking for flags, unflag them
    #          merge the vertex
    #          re-add top and bottom nodes and their connections
    #          update the geo graph
    # 
    # node_u - the vertex Node on self to glue onto
    # lattice_v - Lattice to glue onto self
    # node_v - the vertex Node on lattice_v to glue onto node_u         
    # 
    # returns the glued Lattice, self if node_u is an interior vertex
    #
    # throws exception if node_u is not a Node
    #                     node_v is not a Node
    #                     lattice_v is not a Lattice
    #                     node_u is not a vertex in self
    #                     node_v is not a vertex in lattice_v
    #                     self is the same Lattice object as lattice_v
    def glue_vertex(self, node_u, lattice_v, node_v):
        
        # check that both nodes are actually nodes
        # check that lattice_v input is a Lattice
        if not isinstance(node_u, Node) or not isinstance(node_v, Node):
            raise Exception("Both node inputs must be nodes.")

        if not isinstance(lattice_v, Lattice):
            raise Exception("Lattice input must be a lattice.")

        # check for isomorphism
        # check both nodes aren't from same lattice (u must be from this)
        if node_u not in self._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("Node_u is not an element of the current lattice.")

        if node_v not in lattice_v._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("Node_v is not an element of the input lattice.")

        if self is lattice_v:
            raise Exception("You cannot glue to yourself.")

        if node_u not in self._nodes_list[VERTEX_LATTICE_LAYER] or node_v not in lattice_v._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("Gluing point is not isomorphic.")

        #flag and copy
        copy_of_self = self._make_copy_of_lattice(node_u)
        copy_of_lattice_v = lattice_v._make_copy_of_lattice(node_v)

        # append an index representing the lattice to every node's label
        # this is used to make sure that the nodes are unique
        for layer in copy_of_self._nodes_list:
            for node in layer:
                node._label += str(0)

        for layer in copy_of_lattice_v._nodes_list:
            for node in layer:
                node._label += str(1)

        
        # remove top and bottom off both copies (we will add them back after everything)
        copy_of_self._remove_node(copy_of_self._top_node)
        copy_of_self._remove_node(copy_of_self._bot_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._top_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._bot_node)

        # smash here. now the new lattice will be saved in copy_of_self
        copy_of_self = copy_of_self.smash_lattices(copy_of_lattice_v)

        #identify new_u and new_v and then unflag
        new_u = copy_of_self._find_flagged_node(VERTEX_LATTICE_LAYER)
        new_u.unflag()

        new_v = copy_of_self._find_flagged_node(VERTEX_LATTICE_LAYER)
        new_v.unflag()

        #glue vertices
        new_u = copy_of_self._merge(new_u, new_v)

        # create new top and bottom nodes and a new lattice
        new_top = self._make_node(TOP_LATTICE_LAYER)
        new_bot = self._make_node(BOTTOM_LATTICE_LAYER)

        # manipulate stuff
        copy_of_self._top_node = new_top
        copy_of_self._nodes_list[TOP_LATTICE_LAYER].append(copy_of_self._top_node)
        copy_of_self._bot_node = new_bot
        copy_of_self._nodes_list[BOTTOM_LATTICE_LAYER].append(copy_of_self._bot_node)

        # set each shape node to connect to the top node
        for shape in copy_of_self._nodes_list[SHAPE_LATTICE_LAYER]:
            copy_of_self._set_nodes(copy_of_self._top_node, shape)

        # set each vertex node to connect to the bottom node      
        for vertex in copy_of_self._nodes_list[VERTEX_LATTICE_LAYER]:
            
            copy_of_self._set_nodes(vertex, copy_of_self._bot_node)
        
        #print(copy_of_self.list_layer_lengths())
        copy_of_self._testing_node_0 = copy_of_self._testing_node_1
        copy_of_self._testing_node_1 = copy_of_self._testing_node_2
        copy_of_self._testing_node_2 = new_u       

        copy_of_self._geo_graph = GeometryGraph(copy_of_self)
        return copy_of_self