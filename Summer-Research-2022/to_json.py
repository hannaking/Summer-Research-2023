import networkx as nx
import json

NUMBER_SHAPE_MAP = {00 : "Line Segment",
                    10 : "Isosceles Right Triangle", 11 : "Right Triangle", 12 : "Equilateral Triangle", 13 : "Isosceles Triangle",
                    20 : "Square", 21 : "Rectangle", 22 : "Rhombus", 23 : "Parallelogram", 24 : "Kite",
                    25 : "Right Trapezoid", 26 : "Isosceles Trapezoid", 27 : "Dart",
                    30 : "Regular Pentagon",
                    40 : "Regular Hexagon",
                    50 : "Regular Septagon",
                    60 : "Regular Octagon"}

class ToJson():

    @staticmethod
    def create_json_file(directory, name, json_data):
        f = open(directory + name + ".json", 'w')
        f.write(json_data)
        f.close()

    @staticmethod
    def from_networkx(graph, attribute_name):
        nodes = ToJson._get_nodes(graph, attribute_name)

        edges = ToJson._get_edges(graph)

        to_json = {"source"   : "Negative Example Generator",
                   "textbook" : [False],
                   "nodes"    : nodes,
                   "edges"    : edges}
        
        json_data = json.dumps(to_json, indent=4)
        json_data = json_data.replace('[\n        false\n    ]', '[false]')

        return json_data
    
    @staticmethod
    def _get_nodes(graph, attribute_name):
        nodes = []
        att = nx.get_node_attributes(graph, attribute_name)
        for point, attribute in att.items():
            nodes.append({"ID"    : point,
                          "shape" : NUMBER_SHAPE_MAP[attribute[0]],
                          "sides" : int(attribute[1])})
        return nodes

    def _get_edges(graph):
        edges = []
        quantity = ToJson._get_edge_quantities(graph)
        for points, count in quantity.items():
            edges.append({"point 1" : points[0],
                          "point 2" : points[1],
                          "count"   : count})
        return edges
    
    def _get_edge_quantities(graph):
        quantity = {}
        for p1, p2, version in graph.edges:
            quantity[(p1, p2)] = int(version) + 1
        return quantity