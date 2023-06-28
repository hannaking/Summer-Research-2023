import random as rand
import networkx as nx
import networkx.algorithms.isomorphism as iso

# list of all possible node features for the graphs
SHAPES = [[0, 1],                                                                   # Line Segments
          [10, 3], [11, 3], [12, 3], [13, 3],                                       # Triangles
          [20, 4], [21, 4], [22, 4], [23, 4], [24, 4], [25, 4], [26, 4], [27, 4],   # Quadrilaterals
          [30, 5],                                                                  # Pentagons
          [40, 6],                                                                  # Hextagons
          [50, 7],                                                                  # Heptagons
          [60, 8]]                                                                  # Octagons

# index of the attributes that contains the shape
SHAPE = 0
# index of the attributes that contains the number of sides
SIZE = 1

class RandomFaceGraphCreator():

    # Creates a list of random graphs of a fixed length.
    #
    # total - total number of graphs to generate 
    # max_size(26) - maximum number of nodes that can exist
    #
    # returns the list of random graphs
    @staticmethod
    def create_random_face_graphs(total, max_size=26):
        graphs = []
        # goes until total number of graphs have been made
        while len(graphs) < total:
            graph = RandomFaceGraphCreator.create_random_face_graph(max_size)
            if not RandomFaceGraphCreator.is_in(graph, graphs):
                graphs.append(graph)
        return graphs

    # Creates a random face graph.
    #
    # max_size(26) - maximum number of nodes that can exist
    #
    # returns the random face graph
    @staticmethod
    def create_random_face_graph(max_size=26):
        is_planar = False
        
        # planar face graph ensures planar geometry figure without holes
        while not is_planar:
            nodes = RandomFaceGraphCreator._create_all_nodes(max_size)
        
            edges = RandomFaceGraphCreator._create_all_edges(nodes)
        
            graph = nx.MultiGraph()
            for node, attribute in nodes.items():
                graph.add_node(node)
                nx.set_node_attributes(graph, {node: attribute}, 'default')
            for edge in edges:
                graph.add_edge(edge[0], edge[1])
        
            is_planar, proof = nx.check_planarity(graph)
        
        graph.remove_node('Universe')
        return graph
        
    # Creates a list of nodes that is between 2 and 27 inclusive.
    # Labeled as increasing ascii starting at A. (A, B, C, ...)
    # The last nodes is the Universe node.
    # Each node contains random attributes.
    #
    # max_size(26) - maximum number of nodes that can exist
    #
    # returns the list of nodes
    @staticmethod
    def _create_all_nodes(max_size=26):
        num_of_nodes = rand.randint(1, max_size)
        name = 'A'

        nodes = {}
        for i in range(0, num_of_nodes):
            nodes[name] = rand.choice(SHAPES)
            # increases characher (A, B, C, ...)
            name = chr(ord(name) + 1)
        
        # universe is added last = [Undefined Shape, Infinite]
        nodes['Universe'] = [-1, -1]
        
        return nodes
    
    # creates all of the edges for a given set of nodes distributed
    # randomly.
    #
    # nodes - map of node names to node attributes with the last being the
    #         Universe node
    #
    # returns the edges
    @staticmethod
    def _create_all_edges(nodes):
        has_all_universe_edges = False

        # must touch the universe with atleast three edges (must be at least a triangle)
        while not has_all_universe_edges:
            edges = []
            # list of point names
            points = list(nodes.keys())
            # map from point name to number of edges going off of it
            segment_counts = dict.fromkeys(points, 0)

            for i, point in enumerate(points):
                # size of 1 is can't connect to anything other than the universe,
                # which doesn't need to be represented
                size = nodes[point][SIZE] if nodes[point][SIZE] > 1 else 0
                
                while size > 1 and segment_counts[point] < size:
                    # always chooses valid other point
                    other_point = rand.choice(RandomFaceGraphCreator._get_other_points(i, nodes, segment_counts))
                    
                    edges.append([point, other_point])
                    
                    segment_counts[point] += 1
                    segment_counts[other_point] += 1

            if edges == [] or segment_counts['Universe'] >= 3:
                    has_all_universe_edges = True
        
        # edges are sorted for cleaner looking display
        edges.sort()
        return edges
    
    # Gets the list of points that a a node at given position can be legally
    # connected to.
    #
    # position - index of the current point in the node's key
    # nodes - map of node names to node attribute
    # counts - map of node names to number of edges off of it
    #
    # returns the list of other points
    @staticmethod
    def _get_other_points(position, nodes, counts):
        other_points = list(nodes.keys())[position+1:]
        
        # list of points that can not have any more connections
        bad_points = []
        for other_point in other_points:
            size = nodes[other_point][SIZE]
            if not RandomFaceGraphCreator._is_valid_to_connect(size, counts[other_point]):
                bad_points.append(other_point)
        
        other_points = list(set(other_points).difference(bad_points))
        
        # sort back to original order
        other_points.sort()
        return other_points
    
    # checks whether a node is valid to connect
    #
    # size - maximum number of connections that the node can have
    #         * -1 is Infinite / 1 is 0
    # count - number of connections that the node has
    #
    # returns whether the node is valid to be connected to
    @staticmethod
    def _is_valid_to_connect(size, count):
        return size != 1 and (size == -1 or size > count)
    
    # determines whether or not a graph has an identical graph from a list
    # ignoring the names of points
    #
    # example_graph - graph being compared to the list
    # graphs - graphs being used for the comparison of the example graph
    #
    # returns whether the graph has an match
    @staticmethod
    def is_in(example_graph, graphs):
        for graph in graphs:
            if RandomFaceGraphCreator.is_matching(example_graph, graph):
                return True
        return False

    # determines whether or not two graphs are identical ignoring the names of points
    #
    # graph1 - graph being compared to graph2
    # graph2 - graph being compared to graph1
    #
    # returns whether the graph has an match
    @staticmethod
    def is_matching(graph1, graph2):
        GM = iso.GraphMatcher(graph1, graph2, node_match=lambda n1, n2 : list(n1['default']) == list(n2['default']))
        return GM.is_isomorphic()