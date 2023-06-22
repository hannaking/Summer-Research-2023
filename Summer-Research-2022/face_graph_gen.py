import itertools
import random as rand
import networkx as nx
import networkx.algorithms.isomorphism as iso
import pandas as pd
import stellargraph as sg
from stellargraph import StellarGraph

from lattice_generator import LatticeGenerator
from face_graphs.face_graph_generator import FaceGraphGenerator

class FaceGraphGen():

    @staticmethod
    def generate():
        g

    def create_random_face_graph(self):
        num_of_shapes = rand.randint(1, 10)

        name = 'A'
        nodes = {}
        for i in range(0, num_of_shapes):
            nodes[name] = self.create_random_face_node()
            name = chr(ord(name) + 1)

        if len(nodes) < 2: return points

        segments = []
        points = list(nodes.keys())
        segment_counts = dict.fromkeys(points, 0)
        seg_count = rand.randint(0, pow(2, len(nodes)))
        print(segment_counts)
        for i in range(0, seg_count):
            pair = rand.sample(points, 2)
            if(self.valid_segment_for_point(segment_counts[pair[0]], nodes[pair[0]]) and
               self.valid_segment_for_point(segment_counts[pair[1]], nodes[pair[1]])):
                segments.append(pair)
                segment_counts[pair[0]] += 1
                segment_counts[pair[1]] += 1

        return segments
        
    def valid_segment_for_point(self, segment_count, node):
        if node[1] == 1: return False
        if node[1] >= segment_count: return False
        return True


    def create_random_face_node(self):
        SHAPES = [[0, 1],
                  [10, 3], [11, 3], [12, 3], [13, 3],
                  [20, 4], [21, 4], [22, 4], [23, 4], [24, 4], [25, 4], [26, 4], [27, 4],
                  [30, 5],
                  [40, 6],
                  [50, 7],
                  [60, 8]]
        return rand.choice(SHAPES)


    def _is_valid_shape_type(self, graph:nx.MultiGraph):
        # list of nodes that have already been analyzed
        seen = []
        adj_lists = dict(graph.adj)
        for node, adj_list in adj_lists.items():
            same_connections = True
            seen.append(node)
            # only have to worry about neigbors of nodes that have atleast 3 connections
            # and atleast 1 face outside of the shape 
            if (self._is_outside(graph, node) and
                self._count_connections(graph, node) >= 3):
                for neighbor in list(adj_list):
                    # ignores neighbors have already gone through the upper loop
                    if neighbor not in seen:
                        # passes if any neighbor is fully enclosed or have a different set of neighbors
                        if (not self._has_same_connections(graph, node, neighbor) or
                            not self._is_outside(graph, neighbor)):
                            same_connections = False
                if(same_connections):
                    return False
        return True

    def _has_same_connections(self, graph:nx.MultiGraph, node:str, neighbor:str):
        adj_node = dict(graph[node])
        adj_node[node] = adj_node.pop(neighbor)
        adj_neighbor = dict(graph[neighbor])

        return adj_node == adj_neighbor
    
    def _count_connections(self, graph:nx.MultiGraph, node:str):        
        count = 0
        for conn in list(graph[node].values()):
            count += len(conn)
        return count

    def _is_outside(self, graph:nx.MultiGraph, node:str):        
        num_sides = nx.get_node_attributes(graph, 'Shape')[node][1]
        connections = self._count_connections(graph, node)

        return num_sides > connections

# graph = nx.MultiGraph()
# graph.add_edge("A", "B")
# graph.add_edge("A", "D")
# graph.add_edge("A", "C")
# graph.add_edge("B", "C")
# graph.add_edge("B", "D")
# node = "C"
# nx.set_node_attributes(graph, {'A' : [12, 3],
#                                'B' : [24, 4],
#                                'C' : [30, 5],
#                                'D' : [10, 3]},
#                                'Shape')