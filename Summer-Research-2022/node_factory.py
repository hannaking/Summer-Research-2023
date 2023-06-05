# Node Factory is used to manage Node labels. This file also contains instructions on how to read Node labels.
#
# functions:
#   - make node

from node       import Node

class NodeFactory:
    def __init__(self):
        pass

    # Makes a Node and labels it according to the given parameters.
    #
    # lattice_layer - the layer of the lattice the node is on (ex. TOP_LATTICE_LAYER)
    # label         - the starting label of the node (ex. "0B")
    #
    # returns: the newly created node
    def make_node(self, lattice_layer, label):
        node = Node(lattice_layer)

        # add label prefix depending on node's lattice layer
        if node.get_lattice_layer() == 0:
            node.set_label(str(label) + "B") # B - bottom
            
        elif node.get_lattice_layer() == 1:
            node.set_label(str(label) + "V") # V - vertex

        elif node.get_lattice_layer() == 2:
            node.set_label(str(label) + "E") # E - edge
            
        elif node.get_lattice_layer() == 3:
            node.set_label(str(label) + "S") # S - shape
            
        elif node.get_lattice_layer() == 4:
            node.set_label(str(label) + "T") # T - top

        return node

# How to Read a Label:
# a label has three parts - 
#   1) the number is the order # it was added to the original constructed single-shape lattice.
#           only important thing about this is that each node has a different number
#
#   2) the letter is the lattice layer this node is on
#             T - Top level node
#             S - Shape level node
#             E - Edge level node
#             V - Vertex level node
#             B - Bottom level node
#
#   3) the last number tracks when that shape was added to the lattice and what shape that node is a part of
#            - T and B nodes do not get this value because they are cut off and recreated for every gluing operation
#            - every node with the same value for this portion of the label are part of the same shape
# 
# Examples:
#     0    - first shape / original shape
#     1    - the second lattice being glued to something else
#     10   - also the second shape of a single glueing, but this time I know that there are three shapes on this lattice and that this one was the second shape for the
#             penultimate gluing and a part of the first shape for the second glueing
#     0000 - the first shape, but I also know that this lattice has five shapes in it. This one has been on the first shape side the entire time
#
# ex. 4V0   - the fourth node added to the original construction of this lattice (4). This is a vertex node (V) on the first shape in the glued lattice (0)
# ex. 5E100 - the fifth node added to the original construction of this lattice (5). This is an edge node (E) on the second shape in the glued lattice of 4 shapes (100)
# ex. 23T   - the 23rd node added to this lattice. This is a top level node (T).


#* artwork :) I moved it down so it wouldn't be in the way but don't have the heart to delete it
#*                          _               __           _                   
#*                         | |             / _|         | |                  
#*          _ __   ___   __| | ___        | |_ __ _  ___| |_ ___  _ __ _   _ 
#*         | '_ \ / _ \ / _` |/ _ \       |  _/ _` |/ __| __/ _ \| '__| | | |
#*         | | | | (_) | (_| |  __/ _____ | || (_| | (__| || (_) | |  | |_| |
#*         |_| |_|\___/ \__,_|\___||_____||_| \__,_|\___|\__\___/|_|   \__, |
#*                                                                      __/ |
#*                                                                     |___/ 
#*                           __  . .* ,
#*                         ~#%(" .,$ 
#*                         ."^ ';"
#*                        ..
#*                       ;. :                                   . .
#*                       ;==:                     ,,   ,.@#(&*.;'
#*                       ;. :                   .;#$% & ^^&
#*                       ;==:                   &  ......
#*                       ;. :                   ,,;      :
#*                       ;==:  ._______.       ;  ;      :
#*                       ;. :  ;    ###:__.    ;  ;      :
#* _____________________.'  `._;       :  :__.' .'        `.________________________
#*|_____________________|_________________|_________________|_______________________|