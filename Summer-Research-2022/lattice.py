# A lattice is a partially ordered set (poset). For every pair of elements in the poset, they must have a unique meet and join.​
# This class
#
# attributes:
#   - _factory          : NodeFactory object, used to create new nodes
#   - _label            : string, unique alphanumeric id. for help reading labels, see the bottom of node_factory.py
#   - _top_node         : Node object, the rank 4 node
#   - _list_of_shapes   : list of Node objects, part of nodes_list, the shape rank 3 nodes
#   - _list_of_edges    : list of Node objects, part of nodes_list, the edge rank 2 nodes
#   - _list_of_vertices : list of Node objects, part of nodes_list, the vertex rank 1 nodes
#   - _bot_node         : Node object, the rank 0 node
#   - _vertices         : int, number of vertices in this lattice / shape
#   - _nodes_list       : list of lists of nodes, each list is a rank
#   - _geo_graph        : Geometry Graph object for rough display of shape specified by this lattice
#
# functions:
#   - init
#   - number_of_nodes
#   - number_of_edges
#   - print_lattice
#   - _set_nodes
#   - _make_node
#   - str override
#   - __build_lattice
#   - __make_vertex_layer
#   - __make_edge_layer
#   - __make_shape_layer
#   - _get_corresponding_coordinates
#   - _get_connected_edge             (static)
#   - edge_glued
#   - get_node_from_label
#   - list_layer_lengths
#   - get_top_from_node               (static)
#   - get_bot_from_node               (static)
#   - bfs
#   - find_shortest_path
#   - convert_to_edge_path
#   - get_neighbors                   (static)
#   - is_connected                    (static)(needs unit testing)
#   - get_edge_between                (static)(needs unit testing)
#   - show
#   - _find_flagged_node
#   - _make_copy_of_lattice
#   - smash_lattices
#   - _merge
#   - _remove_node
#   - fill_gap
#   - glue_edges
#   - _get_current_shape_edge          (needs unit testing)
#   -_glue_rest_of_edges
#   - glue_edge
#   - glue_vertex

import copy
import networkx             as nx
import matplotlib.pyplot    as plt

# local modules
from node               import Node
from node_factory       import NodeFactory
from geometry_graph     import GeometryGraph

#@---------------------@#
#@----- Constants -----@#
#@---------------------@#

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

class Lattice:
    # vertices - the number of vertices on the desired shape
    #
    # throws exception if number of vertices is not an integer >= 2
    def __init__(self, vertices):
        # handle vertices < 2 (negative numbers, 0, 1) and non-integer vertices
        # these are not valid shapes and cannot become lattices
        if (vertices < 2 or int(vertices) != vertices):
            raise Exception("Invalid number of vertices")

        self._factory = NodeFactory()
        self._label = 0
        
        # Create figure-level and end nodes
        #   top label is #0 for the first construction
        #   fills other label numbers starting in vertex layer and going up
        #   bottom label is #1 for the first construction
        self._top_node          = self._make_node(TOP_LATTICE_LAYER)       
        self._list_of_shapes    = []
        self._list_of_edges     = []
        self._list_of_vertices  = []                                       
        self._bot_node          = self._make_node(BOTTOM_LATTICE_LAYER)          

        # vertices is the number of vertices in the shape passed in to __init__
        self._vertices = vertices

        #build the lattice and create accompanying geometry graph (for visualization when testing. does not always display as intended)
        self.__build_lattice()
        
        # list of lists of nodes in the lattice
        # organized by layer where each layer is a new list, bottom first
        self._nodes_list = [  
            [self._bot_node],
            self._list_of_vertices,
            self._list_of_edges,
            self._list_of_shapes,
            [self._top_node]
        ]

        self._geo_graph = GeometryGraph(self)

    #@-------------------------------@#
    #@----- Getters and Setters -----@#
    #@-------------------------------@#

    # returns the total number of nodes in the lattice
    def number_of_nodes(self):
        return sum(len(row) for row in self._nodes_list)

    # get the number of connections in the lattice
    #
    # returns the total number of parent and child connections for every node in the lattice
    # the returned value is double the number of lines you would draw on paper because
    # it counts both up and down connections
    def number_of_edges(self):
        num_parents = 0
        num_children = 0
        
        # for every node,
        for layer in self._nodes_list:
            for node in layer:
                # add how many parents and children it has
                num_parents += len(node.get_parents())
                num_children += len(node.get_children())
        
        return num_parents + num_children

    # prints the nodes in the latttice
    # loops through each list in self._nodes_list and prints the node's label
    # looks like: (one triangle)
    #             ['1B']
    #             ['2V', '3V', '4V']
    #             ['5E', '6E', '7E']
    #             ['8S']
    #             ['0T']
    #
    # no return
    def print_lattice(self):
        for layer in self._nodes_list:
            print([str(node) for node in layer])

    #@--------------------------@#
    #@----- Helper Methods -----@#
    #@--------------------------@#

    # set two existing nodes as parent and child to each other 
    # this is reflected as an edge displayed between them on the lattice graph
    #
    # node_u - the parent node
    # node_v - the child node
    #
    # no return
    def _set_nodes(self, node_u, node_v):
        node_u.add_child(node_v) # adds node v as node u's child
        node_v.add_parent(node_u) # adds node u as node v's parent

    # create a new node with a label
    # it has no ties to any other nodes
    #
    # layer - the lattice layer of the node being created
    #
    # returns the new Node
    def _make_node(self, layer):
        node = self._factory.make_node(layer, self._label)
        #update label # (first number in label) to be ready for next node created
        self._label += 1
        return node

    # returns string containing the number of nodes and the number of edges in your lattice
    # in a nice formatted way
    def __str__(self):
        return "Lattice with " + str(self.number_of_nodes()) + " nodes and " + str(self.number_of_edges()) + " edges"

    #@--------------------------------@
    #@----- Constructing Lattice -----@
    #@--------------------------------@

    # Helper for __init__
    # Nodes are created, added to lattice structure, and tied to each other
    #
    # no return
    def __build_lattice(self):
        # Top and bottom nodes already created in __init__
        
        # Call make_vertex_layer to create vertex nodes and connect them to _bot_node
        self.__make_vertex_layer()
        
        # Call make_edge_layer to create edge nodes and connect them to the appropriate vertex nodes
        self.__make_edge_layer()
        
        # Call make_shape_layer to create shape node and tie all edge nodes to that
        # it will return the shape node
        shape = self.__make_shape_layer()
        
        #finish by connecting the top node to the shape node
        self._set_nodes(self._top_node, shape)
    
    # create vertex nodes (same number as _vertices)
    # add them to the appropriate list in _nodes_list
    # tie them to _bot_node
    # adds _bot_node as a child of all vertex nodes and all vertex nodes as a parent to _bot_node
    # each vertex is labeled starting from 2 (because top is 0 and bot is 1)
    #
    # no return
    def __make_vertex_layer(self):  
        # create vertices (however many the lattice was told to have when initialized)
        # and add them to a list of nodes
        for _ in range(self._vertices):
            self._list_of_vertices.append(self._make_node(VERTEX_LATTICE_LAYER))
            
        # connect each vertex node to the bottom node
        for vertex in self._list_of_vertices:
            self._set_nodes(vertex, self._bot_node)

    # create edge nodes (simple shapes excluding line segments will have equal edges and vertices)
    # line segments have 1 edge and 2 vertices
    # add the edge nodes to the appropriate list in _nodes_list
    # tie the new edge nodes to the appropriate vertex nodes
    # edge labels are numbered starting + 1 from the last label of the vertices
    #
    # no return value (there is a return to force you to leave after line segment if it is a line segment)
    def __make_edge_layer(self):
        # special case: line segment. we will only have one edge but two vertices.
        # normally, simple shapes have equal number of edges and vertices
        if self._vertices == 2:
            # create new node
            new_edge = self._make_node(EDGE_LATTICE_LAYER)

            # update _nodes_list
            self._list_of_edges.append(new_edge)

            # set connections
            self._set_nodes(new_edge, self._list_of_vertices[0])
            self._set_nodes(new_edge, self._list_of_vertices[1])

            return

        # not a line segment
        # create new edge, then connects two vertices to it. update _nodes_list
        # this new edge represents the connection between those vertices.
        # for loop works in a cycle, so it will connect each two vertices and end with the last vertex to the first vertex
        #   a to b, b to c, c to d, d to a
        for i in range(len(self._list_of_vertices)):
            # create new node
            new_edge = self._make_node(EDGE_LATTICE_LAYER)

            # update _nodes_list
            self._list_of_edges.append(new_edge)

            # set connections
            self._set_nodes(new_edge, self._list_of_vertices[i])
            # when i+1 is the last vertex, it will mod with itself (which is 0), 
            # so the new edge connects to the first vertex in the list
            self._set_nodes(new_edge, self._list_of_vertices[(i+1) % len(self._list_of_vertices)])

    # create shape node (just one because this is for building simple shapes) and tie all edge nodes to that
    # shape is numbered starting + 1 more than the last label of the edges
    #
    # returns shape-level Node so __build_lattice can set the connection to _top_node  
    def __make_shape_layer(self):
        # create new node
        shape = self._make_node(SHAPE_LATTICE_LAYER)

        # update _nodes_list
        self._list_of_shapes.append(shape)
        
        # set connections
        for node in self._list_of_edges:
            self._set_nodes(shape, node)
        
        return shape

    #@--------------------------@#
    #@----- Public Methods -----@#
    #@--------------------------@#

    # Yields the indices of the vertex nodes in the shape of the lattice given by sl_index.
    # This is used to get the coordinates of the vertex nodes in this specific shape of the lattice
    # so that the shape can be generated.
    # e.g. performing this function on a lattice that contains only one triangle and sl_index == 0,
    # it will return 0, 1, and 2 (this triangle only has three vertex nodes).
    # indexing is done from the nodes list
    #
    # shape_index - the index of the shape whose vertices you want
    #
    # returns a list of indices of the vertex nodes in the shape
    def _get_corresponding_coordinates(self, shape_index):
        visited = []
        vertex_layer = self._nodes_list[VERTEX_LATTICE_LAYER]

        for edge in self._nodes_list[SHAPE_LATTICE_LAYER][shape_index].get_children():

            for vertex in edge.get_children():

                vertex_index = vertex_layer.index(vertex)

                if vertex_index not in visited:
                    visited.append(vertex_index)

                    yield vertex_index

    # if node is an edge, step down each child and back up to the edges and add them to the list,
    # then remove node from the list so node is not connected to itself
    # if node is a vertex, get each parent edge and add them to the list 
    #
    # node - Node object
    #
    # returns a list of edge Node objects that are connected to the given vertex or edge (on the shape, not the lattice)
    #
    # throws exception if node is not a Node object
    # throws exception if node is not a vertex or edge node
    @staticmethod
    def get_connected_edges(node):
        if not isinstance(node, Node):
            raise Exception("node must be a Node object")
        if not(node._lattice_layer != EDGE_LATTICE_LAYER or node._lattice_layer != VERTEX_LATTICE_LAYER):
            raise Exception("node must be on either the edge or vertex lattice layer.")

        connected = []

        if node._lattice_layer == EDGE_LATTICE_LAYER:
            children = node.get_children()
            for child in children:
                parents = child.get_parents()
                for parent in parents:
                    connected.append(parent)
            if node in connected:
                # remove the edge itself from the list
                connected.remove(node) 

        else:
            #get the edges this vertex is a part of
            edges = node.get_parents()
            for edge in edges:
                connected.append(edge)

        return connected

    # determine if a given edge node has already been glued to by checking parents
    # edges that have been glued to have more than one parent shape node
    #
    # edge - the edge node to check glued / not glued
    # 
    # returns True if edge node is glued, False if not
    def edge_glued(self, edge):
        return len(edge.get_parents()) > 1
    
    # given a string label, it finds the node in the lattice with that label
    #
    # label - the label of the node to find
    #
    # returns Node if a node with the given label is found, otherwise returns None
    # 
    # throws exception if label passed in is not a string
    def get_node_from_label(self, label):
        if not isinstance(label, str):
            raise Exception("Label must be a string")

        for layer in self._nodes_list:
            for node in layer:
                if node._label == label:
                    return node

        return None

    # prints the lengths of the nodes list
    # 
    # returns a list of the lengths of the lists in _nodes_list
    # order: bottom layer, edge layer, vertex layer, shape layer, top layer
    # ex. [1, 5, 5, 1, 1]
    def list_layer_lengths(self):
        len_list = []
        for i in self._nodes_list:
            len_list.append(len(i))

        return len_list

    # Gets the top-most node of a lattice from any nodes
    # helpful when navigating around a lattice from just one node in it
    # recursively moves up the first node in a layer until it reaches the top layer, identified by lattice layer
    #
    # returns the top-most Node of the lattice
    @staticmethod
    def get_top_from_node(node):
        if node._lattice_layer == TOP_LATTICE_LAYER:
            return node
        else:
           return Lattice.get_top_from_node(node.get_parents()[0])

    # Gets the bottom-most node of a lattice from any nodes
    # helpful when navigating around a lattice from just one node in it
    # recursively moves up the first node in a layer until it reaches the bottom layer, identified by lattice layer
    #
    # returns the bottom-most Node of the lattice
    @staticmethod
    def get_bot_from_node(node):
        if node._lattice_layer == BOTTOM_LATTICE_LAYER:
            return node
        else:
            return Lattice.get_bot_from_node(node.get_children()[0])

    # Use breadth first search in the lattice object from the starting node passed in
    # Creates an edge on the networkx graph between each parent and child of the nodes
    #
    # visited - a list of nodes that have already been visited by bfs
    # node - the node being currently looked at
    # queue - the queue of nodes not yet visited
    #
    # no return value
    def bfs(self, visited, node, queue):
        visited.append(node)
        for child in node.get_children():
            if child not in visited:
                queue.append(child)
        for child in queue:
            self.bfs(visited, child, queue)

    # find the shortest exterior path between two nodes in the lattice
    # will end up used in convert_to_edge_path and then fill_gap
    #
    #start_vertex - the node to start the path from
    # end_vertex - the node to end the path at
    # 
    # returns a list of vertex nodes that make up the shortest path on the perimeter between the two vertices passed in
    # start and end nodes are included in the shortest path
    # There may be more than one shortest path between a start and end. This returns only one of them.
    #
    # throws exception if either vertex node passed in is not a Node object
    # throws exception if start and end vertices are the same node
    def find_shortest_path(self, start_vertex, end_vertex):
        if not isinstance(start_vertex, Node) or not isinstance(end_vertex, Node):
            raise Exception("Type of both inputs must be Node.")
        if start_vertex is end_vertex:
            raise Exception("You cannot find the shortest path between the exact same nodes.")

        # nx.shortest_path returns a LIST of nodes forming the shortest path,
        # excluding interior edges (hence .get_perimeter).
        return nx.shortest_path(self._geo_graph.get_perimeter(), start_vertex, end_vertex)

    # convert vertex path identified by find_shortest_path to a path of edges for use in fill_gap
    # how it works: start at the first two vertices. while you are not at the end vertex,
    #               get the edges the vertex is connected to.
    #               for each of those edges, find the one that connects to the next vertex in the path.
    #               add that edge to the edge_path
    #               update your current and next vertices and loop
    #
    # vertex_path - the list of vertex nodes that make up the shortest path between the two vertices
    #
    # returns a list of edge nodes that make up the shortest path between the two vertices
    def convert_to_edge_path(self, vertex_path):
        edge_path = []

        current_vertex = vertex_path[0]
        next_vertex = vertex_path[1]

        #while not at the end of the path, 
        while current_vertex is not vertex_path[-1]:
            # get the edges this vertex is part of and
            edges = current_vertex.get_parents()

            # for each of those edges,
            for edge in edges:
                # find the edge node which also connects to the next vertex in the shortest_path
                if next_vertex in edge.get_children():
                    # add that edge to the shortest edge path and update the vertex you are looking at
                    edge_path.append(edge)
                    current_vertex = next_vertex

                    # update the next_vertex
                    if next_vertex is not vertex_path[-1]:
                        next_vertex = vertex_path[vertex_path.index(current_vertex) + 1]
                    
                    # break to consider next pair of vertices
                    break

        return edge_path

    # gets the vertex neighbors of the vertex (on the shape itself, not the lattice!)
    # e.g. one of a triangle's vertices will have two neighbors
    # uses a zig-zag movement to go up and down from vertex to edge layer to follow the shape edges
    #
    # vertex - Node to get the neighbors of
    #
    # returns list of vertex nodes
    #
    # throws exception if vertex is not on the vertex lattice layer
    @staticmethod
    def get_neighbors(vertex):
        if vertex._lattice_layer != VERTEX_LATTICE_LAYER:
            #if it is not a vertex, we don't care about it
            raise Exception("You can only get the neighbors of a vertex.") 
        
        # get the edges this vertex is a part of
        edges = vertex.get_parents()
        neighbors = []

        # go up from the vertex to each edge it is connected to,
        for edge in edges:
            #then down from that edge to the other vertex, which gets added to the neighbors list
            edge_children = edge.get_children()

            if edge_children[0] is not vertex:
                neighbor = edge_children[0]
            else:
                neighbor = edge_children[1]

            neighbors.append(neighbor)

        return neighbors

    # checks connectivity between vertices OR edges
    # ask if a vertex is a neighbor of another vertex  (in the shape)
    # ask if a edge is a neighbor of another edge  (in the shape)
    # uses get_neighbors(vertex) when checking for vertex connectivity
    # checks in a zig-zag up and down the lattice when checking for edge connectivity
    #
    # node1 - Node to check if it is connected to node2
    # node2 - Node to check if it is connected to node1
    #
    # returns boolean whether two nodes are connected (in the actual shape)
    # it will return false if you check if a node is connected to itself
    #
    # throws exception if either node is not a Node object
    # throws exception if both nodes are not on the vertex lattice layer
    # and both nodes are not on the edge lattice layer
    # #@ needs test
    @staticmethod
    def is_connected(node1, node2): 
        if not isinstance(node1, Node):
            raise Exception("node1 must be a Node object")
        if not isinstance(node2, Node):
            raise Exception("node2 must be a Node object")

        # both nodes must be on the same layer
        if node1._lattice_layer != node2._lattice_layer:
            raise Exception("node1 and node2 must be on the same lattice layer")
        # both nodes must be on the edge lattice layer or both nodes must be on the vertex lattice layer
        # (node1 being on edge or vertex layer implies node2 is as well, due to the previous if-statement)
        if not(node1._lattice_layer != EDGE_LATTICE_LAYER or node1._lattice_layer != VERTEX_LATTICE_LAYER):
            raise Exception("both node1 and node2 must be on either the edge or vertex lattice layer.")
        
        # finally, we can check for connectivity

        # if layer is vertex layer:
        if node1._lattice_layer == VERTEX_LATTICE_LAYER:
            neighbors_of_vertex1 = Lattice.get_neighbors(node1)

            if node2 in neighbors_of_vertex1:
                return True
            else:
                return False

        # if layer is edge layer:
        else:
            children_of_edge1 = node1.get_children()
            for child in children_of_edge1:
                parents = child.get_parents()
                for parent in parents:
                    if parent is node2:
                        return True
            return False

    # gets the Node object (on edge layer) that is between vertex1 and vertex2 (on the shape, not the lattice)
    # # finds the edge between by going up from vertex1 to each edge it is connected to, then down from that edge to 
    # see if vertex2 is in the children of that edge. if it is, then that edge is the edge between vertex1 and vertex2.
    # if vertex2 is not found, then vertex1 and vertex2 are not connected.
    #
    # vertex1 - vertex Node to get the edge between
    # vertex2 - vertex Node to get the edge between
    #
    # returns None if the edges are not connected
    #
    # throws exception if vertex1 is not a Node
    # throws exception if vertex2 is not a Node
    # throws exception if vertex1 is not on the vertex lattice layer
    # throws exception if vertex2 is not on the vertex lattice layer
    # #@ needs test
    @staticmethod
    def get_edge_between(vertex1, vertex2): 
        if not isinstance(vertex1, Node):
            raise Exception("vertex1 must be a Node object")
        if not isinstance(vertex2, Node):
            raise Exception("vertex2 must be a Node object")
        
        # both nodes must be vertices
        if vertex1._lattice_layer != VERTEX_LATTICE_LAYER:
            raise Exception("vertex1 must be on the vertex lattice layer")
        if vertex2._lattice_layer != VERTEX_LATTICE_LAYER:
            raise Exception("vertex2 must be on the vertex lattice layer")

        edges = vertex1.get_parents()
        for edge in edges:
            children = edge.get_children()
            if vertex2 in children:
                return edge
        return None

    # creates and displays a networkx graph of the lattice
    # builds the lattice graph from the _nodes_list
    # layers are color-coded and display in rows by layer
    #
    # returns the networkx graph of the lattice
    def show(self):
        graph = nx.Graph()
        for layer in self._nodes_list:
            for node in layer:
                graph.add_node(node, layer=node._lattice_layer)
                for parent in node.get_parents():
                    graph.add_edge(parent, node)

        # Print in pretty colors
        layer_colors = ["purple", "red", "green", "blue", "orange"]

        # Assigning color and position based on layer_id
        # this forces the lattice to adhere to its layers when printed
        color = [layer_colors[data["layer"]] for v, data in graph.nodes(data=True)]
        pos = nx.multipartite_layout(graph, subset_key="layer", align="horizontal")

        # Output to display
        nx.draw(graph, pos, node_color=color, with_labels = False)
        plt.show()
        return graph

    #@---------------------------------@#
    #@----- Gluing Helper Methods -----@#
    #@---------------------------------@#

    # finds the flagged node in the specified layer
    # does NOT unflag the node
    #
    # layer - the layer to search for a flagged node in
    #
    # returns Node
    # returns None if no flagged node is found on the layer
    def _find_flagged_node(self, layer):
        for node in self._nodes_list[layer]:
            if node._flagged:
                return node
        return None

    # makes deepcopy of a lattice
    # preserves which node is to be glued by flagging it before copying
    # node is then unflagged in original
    #
    # node - node to be copied (must be preserved over the copying, hence flag)
    #
    # returns Lattice
    #
    # throws exception ifnode is not a Node object
    # throws exception if node to be flagged is not in self Lattice
    def _make_copy_of_lattice(self, node):
        if not isinstance(node, Node):
            raise Exception("Node input is not a Node object")
        
        in_lists = False
        for i in self._nodes_list:
            if node in i:
                in_lists = True

        if not in_lists:
            raise Exception("Node does not exist in this lattice.")

        #----------------exceptions done----------------#

        # flag node being glued
        node.flag()
        
        # make deepcopy
        copy_lattice = copy.deepcopy(self)

        # unflag node in original
        node.unflag()

        #return deepcopy of the lattice, with the node to be glued flagged
        return copy_lattice

    # smashes two lattices (self and lattice 2) into one lattice object, saved to self
    # (so make sure this is a copy--don't overwrite an original!)
    # adds the data from lattice2's nodes list data to self's nodes list data
    # no connections are made
    # the _nodes_list for lattice_2 is then cleared
    #
    # lattice2 - Lattice to absorb into self
    #
    # returns Lattice containing the nodes from both lattices
    #
    # throws exception if lattice_2 is not a Lattice object
    def smash_lattices(self, lattice2):
        if not isinstance(lattice2, Lattice):
            raise Exception("lattice2 is not a Lattice")
        
        for i in range(len(lattice2._nodes_list)):
            self._nodes_list[i] += lattice2._nodes_list[i]

        lattice2._nodes_list.clear()
        return self

    # merges two nodes
    # all connections from node v are moved to node u
    # if either u or v is flagged, u becomes flagged
    # removes all connections to and from node v to "delete" it
    #
    # node_u - node to merge into
    # node_v - node to merge, will be removed
    #
    # returns merged Node, (u) containing all connections and flag status from both nodes passed in
    def _merge(self, node_u, node_v):                                           
        # add the children of vertex 2 to vertex 1
        children_of_node_v = node_v.get_children()

        for child in children_of_node_v:
            self._set_nodes(node_u, child)

        # add the parents of vertex 2 to vertex 1
        parents_of_node_v = node_v.get_parents()

        for parent in parents_of_node_v:
            self._set_nodes(parent, node_u)

        # maintain flagging
        if node_v._flagged or node_u._flagged:
            node_u.flag()

        # sever vertex 2 from all connections (remove it)
        self._remove_node(node_v)

        # returns the vertex that the new connections have been made to
        return node_u

    # removes a given node from its lattice by severing all connections to and from it
    # also removes the node from the _nodes_list
    #
    # node - Node to remove
    #
    # no return value
    #
    # throws exception if node is not a Node object
    def _remove_node(self, node):
        if not isinstance(node, Node):
            raise Exception("You cannot remove a non-node")
            
        #clear links to node from its parents
        for parent in node.get_parents():
            parent.disown_child(node)

        #clear links from node to its parents
        node.set_parents([])

        #clear links to node from its children
        for child in node.get_children():
            child.disown_parent(node)

        #clear links from node to its children
        node.set_children([])

        # remove the node from the list of nodes
        self._nodes_list[node._lattice_layer].remove(node)

    #@------------------@            
    #@----- Gluing -----@
    #@------------------@

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
        # pick any point on lattuce_to_fill, it doesn't matter which
        # leave
        if node_u is node_v:
            return self.glue_vertex(node_u, lattice_to_fill, lattice_to_fill._nodes_list[VERTEX_LATTICE_LAYER][0])

        if node_u not in self._geo_graph.get_perimeter().nodes:
            raise Exception("Node u is not an exterior node.")

        if node_v not in self._geo_graph.get_perimeter().nodes:
            raise Exception("Node v is not an exterior node.")

        #find shortest path of edges btwn u and v
        shortest_path_vertices = self.find_shortest_path(node_u, node_v)
        shortest_path = self.convert_to_edge_path(shortest_path_vertices)
        
        # check you have no interior edges on your path (already glued onto before)
        for edge in shortest_path:
            if len(edge.get_parents()) > 1:
                raise Exception("There is already a shape glued onto one of the edges in the path")
            
            for vertex in edge.get_children():
                # returns self since it will get filtered out when checking for isomorphism
                # Exception: There is already a shape singly glued onto one of the vertices in the path
                # i think this is “The thing about three / four edge parents”??? - Imagine you have a bowtie,
                # you want to be able to glue to that middle vertex because it is still exterior
                if len(vertex.get_parents()) > 3:
                    return self
        
        # if we have only one segment,
        # call glue_edge to glue only along that one edge
        # leave
        if len(shortest_path) == 1:
            lattice_to_fill_edge = lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER][0]
            return self.glue_edge(shortest_path[0], lattice_to_fill, lattice_to_fill_edge)

        # if node_u and node_v are already connected, you cannot fill. it is the three-tri-but-it-looks-like-two-because-they-stacked thing
        #  /|\    looks like this
        # / | \   the second one is actually two triangles, one on top of the other, because it tried
        # \ | /   to glue two sides of a triangle to two sides of an existing triangle, forcing the last side
        #  \|/    to be directly on top of the third side of the existing triangle
        # Dr. Stadnyk - "2 vertices can only ever have 1 edge between them because we are in two dimensions"
        for parent in node_u.get_parents():   
            if node_v in parent.get_children():
                # need to return something, so just glue onto the first edge. it will get filtered out later when we check isomorphism
                lattice_to_fill_edge = lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER][0]
                return self.glue_edge(shortest_path[0], lattice_to_fill, lattice_to_fill_edge)

        # check that path length < the number of edges lattice_to_fill has
        # (you can't proceed if the path is the same length or longer than the shape's # of edges)
        num_edges_of_shape = len(lattice_to_fill._nodes_list[EDGE_LATTICE_LAYER])
        if len(shortest_path) >= num_edges_of_shape:
            raise Exception("The length of the path was too large. Choose a smaller path or a larger shape.")

        # now we fill the gap
        return self.glue_edges(shortest_path, lattice_to_fill)

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
    # returns Lattice
    #
    # throws exception if lattice_v is not a simple shape
    def glue_edges(self, list_of_edges, lattice_v):

        # make sure lattice v is a simple shape
        if len(lattice_v._top_node.get_children()) > 1:
            raise Exception("The input lattice is not a simple shape.")

        # make copies of both of our lattices
        copy_of_self = copy.deepcopy(self)
        copy_of_lattice_v = copy.deepcopy(lattice_v)

        # find the shortest path edges in the copy IN ORDER of what they're supposed to be in
        # use the labels
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
        # now we have the copied_path_edges in the correct order
            
        # add shape / glue order information to the labels of the nodes (see node_factory.py for help reading labels) 
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
        
        # FIRST merging. this merge is unique and has a different process than each subsequent merge.
        # it merges one edge and two vertices, not one edge and one vertex like the following ones 
        child0 = current_path_edge.get_children()[0]
        child1 = current_path_edge.get_children()[1]

        child0_v = current_shape_edge.get_children()[0]
        child1_v = current_shape_edge.get_children()[1]

        copy_of_self._merge(child0, child0_v)
        copy_of_self._merge(child1, child1_v)
        
        copy_of_self._merge(current_path_edge, current_shape_edge)

        #@ glue the rest
        # current_path_edge is still copied_path_edges[0]
        next_path_edge = copied_path_edges[1]

        # loop through the rest of the edges in the shortest path
        # current_shape_edge - the current edge in the shape we are filling the gap with
        # current_path_edge - the current edge in the path
        # next_path_edge - the next edge in the path
        # glue_rest_of_edges glues current_shape_edge and current_path_edge.
        # the loop handles the next iteration of glue_rest_of_edges, because it updates next_path_edge.
        for i in range(1, len(copied_path_edges)): 

            current_shape_edge = self._get_current_shape_edge(copied_shape_edges, current_path_edge, next_path_edge)
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

        # update geo graph
        copy_of_self._geo_graph = GeometryGraph(copy_of_self)
        
        # return the new lattice
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
    def _get_current_shape_edge(self, shape_edges, current_path_edge, next_path_edge): 
        #get the vertex that connects the next_path_edge to current_path_edge
        vertex_between = None
        for child in next_path_edge.get_children():
            parents = child.get_parents()

            # if this vertex has both the current and prev edge as its parents (aka it's between them), then we want it
            if current_path_edge in parents:
                vertex_between = child
                break

        #get the vertex's parents and make sure the edge we get is part of the second lattice
        for parent in vertex_between.get_parents():
            if parent in shape_edges:
                current_shape_edge = parent
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
        child0 = current_path_edge.get_children()[0]
        child1 = current_path_edge.get_children()[1]

        child0_v = current_shape_edge.get_children()[0]
        child1_v = current_shape_edge.get_children()[1]
        
        children = [child0, child1, child0_v, child1_v]

        # this will remove the repeated vertex (aka the just previously glued vertex).
        # it has already been glued in the previous edge glue so we cannot glue it again
        # it should remove two vertices (because the edges both share this vertex).
        for vertex in children:
            if children.count(vertex) == 2:
                children.remove(vertex)
                children.remove(vertex)

        if len(children) != 2:
            raise Exception("The children of the path and shape edges did not properly remove the previously glued vertex.")

        # the vertices to be glued
        v1 = children[0]
        v2 = children[1]
        
        # merge the pair of vertices that are connected to the shape edge and path edge.
        # due to the previous check, we know that neither of these are the previously glued vertex.
        self._merge(v1, v2)
        
        # now, we merge the edges themselves.
        self._merge(current_path_edge, current_shape_edge)

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
            raise Exception("node_u is not an edge in self.")

        if node_v not in lattice_v._nodes_list[EDGE_LATTICE_LAYER]:
            raise Exception("node_v is not an edge in the input lattice.")
        
        if self is lattice_v:
            raise Exception("You cannot glue to yourself.")

        if self._vertices == 2:
            return self

        if lattice_v._vertices == 2:
            return lattice_v

        #interior edge (already glued onto before)
        if len(node_u.get_parents()) == 2 or len(node_v.get_parents()) == 2:
            raise Exception("There is already a shape glued onto this edge")
        #---------------------

        # Make copies of lattices
        copy_of_self = self._make_copy_of_lattice(node_u)
        copy_of_lattice_v = lattice_v._make_copy_of_lattice(node_v)

        # update labels
        for layer in copy_of_self._nodes_list:
            for node in layer:
                node._label += str(0)

        for layer in copy_of_lattice_v._nodes_list:
            for node in layer:
                node._label += str(1)

        # Remove top and bottom nodes
        copy_of_self._remove_node(copy_of_self._top_node)
        copy_of_self._remove_node(copy_of_self._bot_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._top_node)
        copy_of_lattice_v._remove_node(copy_of_lattice_v._bot_node)

        # Smash lattices into one
        copy_of_self = copy_of_self.smash_lattices(copy_of_lattice_v)

        # Get node_u and node_v in the copied lattice
        new_u = copy_of_self._find_flagged_node(EDGE_LATTICE_LAYER)
        new_u.unflag()

        new_v = copy_of_self._find_flagged_node(EDGE_LATTICE_LAYER) 
        new_v.unflag()

        # Make child and parent connections
        # For each node in downset, add the child and parent connections 
        # from the first lattice to the second lattice
        child0 = new_u.get_children()[0]
        child1 = new_u.get_children()[1]

        child0_v = new_v.get_children()[0]
        child1_v = new_v.get_children()[1]

        copy_of_self._merge(child0, child0_v)
        copy_of_self._merge(child1, child1_v)

        new_v = copy_of_self._merge(new_u, new_v)

        # Add new top and bottom nodes
        new_top = self._make_node(TOP_LATTICE_LAYER)
        new_bot = self._make_node(BOTTOM_LATTICE_LAYER)

        copy_of_self._top_node = new_top
        copy_of_self._nodes_list[TOP_LATTICE_LAYER].append(copy_of_self._top_node)
        copy_of_self._bot_node = new_bot
        copy_of_self._nodes_list[BOTTOM_LATTICE_LAYER].append(copy_of_self._bot_node)

        # Connect shape to new top
        for shape in copy_of_self._nodes_list[SHAPE_LATTICE_LAYER]:
            copy_of_self._set_nodes(copy_of_self._top_node, shape)

        # Connect vertices to new bottom    
        for vertex in copy_of_self._nodes_list[VERTEX_LATTICE_LAYER]: 
            copy_of_self._set_nodes(vertex, copy_of_self._bot_node)

        # update geo graph
        copy_of_self._geo_graph = GeometryGraph(copy_of_self)
        
        return copy_of_self

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

        # check for correct layer
        # check both nodes aren't from same lattice (u must be from this)
        if node_u not in self._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("Node_u is not an element of the current lattice.")

        if node_v not in lattice_v._nodes_list[VERTEX_LATTICE_LAYER]:
            raise Exception("Node_v is not an element of the input lattice.")

        if self is lattice_v:
            raise Exception("You cannot glue to yourself.")

        interior_vertex = True
        for edge in node_u.get_parents():
            if not self.edge_glued(edge):
                interior_vertex = False
                break

        if interior_vertex:
            return self

        interior_vertex = True
        for edge in node_v.get_parents():
            if not self.edge_glued(edge):
                interior_vertex = False
                break

        if interior_vertex:
            return self
        #----------------------------------
        
        # flag and copy
        copy_of_self = self._make_copy_of_lattice(node_u)
        copy_of_lattice_v = lattice_v._make_copy_of_lattice(node_v)

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

        # this is right because copy of self IS the smashed lattice
        new_v = copy_of_self._find_flagged_node(VERTEX_LATTICE_LAYER)
        new_v.unflag()

        #glue vertices
        new_u = copy_of_self._merge(new_u, new_v)

        # create new top and bottom nodes and a new lattice
        new_top = self._make_node(TOP_LATTICE_LAYER)
        new_bot = self._make_node(BOTTOM_LATTICE_LAYER)

        # re-add top and bottom
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

        copy_of_self._geo_graph = GeometryGraph(copy_of_self)

        return copy_of_self