# Node objects that make up the lattice. Have children and parent lists of Nodes to maintain connections.
#
# attributes:
#     _lattice_layer : integer, the layer of the lattice the node is in
#     _label         : string, unique alphanumeric id. for help reading labels, see the bottom of node_factory.py
#     _children      : list of child Node objects
#     _parents       : list of parent Node objects
#     _flagged       : boolean, used to help find the Node after deepcopy performed in gluing operations
#     _graph_object  : segment (if node is an edge) or coordinate object (if node is a vertex), used to find the corresponding object in the plane
#
# functions:
#   - add child
#   - disown child
#   - add parent
#   - disown parent
#   - exists in children
#   - exists in parents
#   - flag
#   - unflag
#   - set lattice layer
#   - get lattice layer
#   - get children
#   - set children
#   - get parents
#   - set parents
#   - get parents and children
#   - set label
#   - str override

class Node:

    def __init__(self, lattice_layer):
        self._lattice_layer = None
        self._label = None
        # need to check if it's valid before it can be added
        self.set_lattice_layer(lattice_layer) 
        self._children = []
        self._parents = []
        self._flagged = False
        self._graph_object = None

        #@ J_Isomorphism thing
        self._structure_label = None

    # no duplicate children or parents allowed

    # add a node to the list of child nodes
    # if node passed in is already in child list, nothing happens
    #
    # child - Node to be added to child list
    #
    # throws exception if child passed in is not a Node object
    def add_child(self, child):
        if not isinstance(child, Node):
            raise Exception("Child must be a node.")

        # will not add duplicates
        if not self._exists_in_children(child):
            self._children.append(child)

    # remove a node from the list of child nodes
    # if that node is not a child, nothing happens
    #
    # child - Node to be removed from child list
    #
    # throws exception if child passed in is not a Node object
    def disown_child(self, child):
        if not isinstance(child, Node):
            raise Exception("Child must be a node.")
 
        if self._exists_in_children(child):
            self._children.remove(child)


    # add a node to the list of parent nodes
    # if node passed in is already in parent list, nothing happens
    #
    # parent - Node to be added to parent list
    #
    # throws exception if parent passed in is not a Node object
    def add_parent(self, parent):   
        if not isinstance(parent, Node):
            raise Exception("Parent must be a node.")

        # will not add duplicates
        if not self._exists_in_parents(parent):
            self._parents.append(parent)

    # remove a node from the list of parent nodes
    # if that node is not a parent, nothing happens
    #
    # parent - Node to be removed from parent list
    #
    # throws exception if parent passed in is not a Node object
    def disown_parent(self, parent):
        if not isinstance(parent, Node):
            raise Exception("Parent must be a node.")
 
        if self._exists_in_parents(parent):
            self._parents.remove(parent)

    #@-----------------------------@#
    #@---- protected helpers ------@#
    #@-----------------------------@#

    # child - Node to look for in the child list
    #
    # returns true if the node exists in the list of children, false if it does not
    #
    # throws exception if child passed in is not a Node object
    def _exists_in_children(self, child):
        if not isinstance(child, Node):
            raise Exception("Child must be a node.")

        if child in self._children:
            return True
        
        return False

    # parent - Node to look for in the parent list
    #
    # returns true if the node exists in the list of parents, false if it does not
    #
    # throws exception if parent passed in is not a Node object
    def _exists_in_parents(self, parent):
        if not isinstance(parent, Node):
            raise Exception("Parent must be a node.")

        if parent in self._parents:
            return True
            
        return False

    #@-------------------------------@#
    #@-------- baby methods ---------@#
    #@-------------------------------@#    

    # set the value of _flagged to True
    def flag(self):
        self._flagged = True

    # set the value of _flagged to False
    def unflag(self):
        self._flagged = False


    # sets the value of _lattice_layer to the value passed in
    #
    # lattice_layer - new _lattice_layer value
    #
    # throws if the value passed in is not a valid lattice layer (< 0 or > 4)
    def set_lattice_layer(self, lattice_layer):
        # range increments by 1, so this will exclude non-ints
        if lattice_layer not in range(0, 5):
            raise Exception("lattice layer number must be an integer between 0 and 4")        

        self._lattice_layer = lattice_layer
    
    # returns the value of _lattice_layer
    def get_lattice_layer(self):
        return self._lattice_layer


    # returns the value of _children, which is the nodes in this node's list of children
    def get_children(self):
        return self._children

    # sets the value of _children to a list which is passed in
    def set_children(self, list):
        self._children = list

    #returns the value of _parents, which is the nodes in this node's list of parents
    def get_parents(self):
        return self._parents

    # sets the value of _parents to a list which is passed in
    def set_parents(self, list):
        self._parents = list

    # returns the contents of both _children and _parents as one list
    def get_parents_and_children(self):
        return self._parents + self._children

    # sets the value of label to the label passed in
    def set_label(self, label):
        self._label = label

    # returns the label of the node as a string for printing
    def __str__(self):
        return self._label

    # returns the value of _graph_object, which is the segment (if node is an edge) or coordinate object (if node is a vertex)
    def get_graph_object(self):
        return self._graph_object

    # sets the value of _graph_object to the segment or coordinate object passed in
    def set_graph_object(self, graph_object):
        self._graph_object = graph_object