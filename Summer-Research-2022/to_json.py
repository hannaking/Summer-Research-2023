import networkx as nx
import json

# assocation of the shape code and the name of the shape
NUMBER_SHAPE_MAP = {00 : "Line Segment",
                    10 : "Isosceles Right Triangle", 11 : "Right Triangle", 12 : "Equilateral Triangle", 13 : "Isosceles Triangle",
                    20 : "Square", 21 : "Rectangle", 22 : "Rhombus", 23 : "Parallelogram", 24 : "Kite",
                    25 : "Right Trapezoid", 26 : "Isosceles Trapezoid", 27 : "Dart",
                    30 : "Regular Pentagon",
                    40 : "Regular Hexagon",
                    50 : "Regular Septagon",
                    60 : "Regular Octagon"}

class ToJson():

    # creates a json file using a json string with a given name at a given directory
    #
    # directory - relative path to the folder that will store the json file
    # name - name of the json file not including the extension
    # json_data - json string containg the contents of the json file
    #
    @staticmethod
    def create_json_file(directory, name, json_data):
        f = open(directory + name + ".json", 'w')
        f.write(json_data)
        f.close()

    # turns a networkx graph into a json file
    #
    # graph - the networkx graph being converted
    # attribute_name - the name of the node attributes in the networkx graph
    # 
    # returns a json string encoding the information in the graph
    @staticmethod
    def from_networkx(graph, attribute_name, source, is_from_textbook):
        nodes = ToJson._get_nodes(graph, attribute_name)

        edges = ToJson._get_edges(graph)

        to_json = {"source"   : source,
                   "textbook" : [is_from_textbook],
                   "nodes"    : nodes,
                   "edges"    : edges}
        
        json_data = json.dumps(to_json, indent=4)
        # puts the '[false]' / '[true]' back on one line
        json_data = json_data.replace('[\n        false\n    ]', '[false]')
        json_data = json_data.replace('[\n        true\n    ]', '[true]')

        return json_data
    
    # turns the nodes of a networkx graph into a formatted dictionary.
    #
    # graph - the networkx graph whose nodes are being converted
    # attribute_name - the name of the node attributes
    #
    # returns the dictionary containing the node data
    @staticmethod
    def _get_nodes(graph, attribute_name):
        nodes = []
        att = nx.get_node_attributes(graph, attribute_name)
        for point, attribute in att.items():
            nodes.append({"ID"    : point,
                          "shape" : NUMBER_SHAPE_MAP[attribute[0]],
                          "sides" : int(attribute[1])})
        return nodes

    # turns the nodes of a networkx graph into a formatted dictionary.
    #
    # graph - the networkx graph whose edges are being converted
    #
    # returns the dictionary containing the edge data
    def _get_edges(graph):
        edges = []
        quantity = ToJson._get_edge_quantities(graph)
        for points, count in quantity.items():
            edges.append({"point 1" : points[0],
                          "point 2" : points[1],
                          "count"   : count})
        return edges
    
    # gets the number of repetionions of each edge and convert them into a
    # dictionary
    #
    # graph - the graph whose edges are being counted
    #
    # returns a dictionary associating the number of repetionions with the
    # a tuple of the constituant nodes of each unique edge
    def _get_edge_quantities(graph):
        quantity = {}
        for p1, p2, version in graph.edges:
            quantity[(p1, p2)] = int(version) + 1
        return quantity