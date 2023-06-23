import os
import random
from to_stellar_graph import ToStellarGraph
import networkx as nx
import networkx.algorithms.isomorphism as iso

from to_json import ToJson

# association between number of sides and shape codes
SIDES_FOR_SHAPES = {1: [00],
                    3: [10, 11, 12, 13],
                    4: [20, 21, 22, 23, 24, 25, 26, 27],
                    5: [30],
                    6: [40],
                    7: [50],
                    8: [60]}

# how many itterations it will wait for an improvement
PATIENCE = 200

class NegativeExampleGen():

    # generates a number of figures that are isomorphic to the texbook examples, but
    # contain different shape labels. The figures are created a networkx and can be
    # stored as json files. (in the Negative shapes folder)
    # The figures are distributed between the different textbook examples.
    # 
    # total -  the total number of figures that should be made
    # creates_files(True) - whether or not to create json files
    # 
    # returns the figures as networkx graphs 
    @staticmethod
    def generate(total, creates_files=True):
        # list of all figures that are isomorphically unique textbook examples
        positive_graphs = NegativeExampleGen.read_all_positive_graphs()
        # list, as long as the number of textbook figures, that is split as evenly as possible
        # with the extras scattered randomly
        counts = NegativeExampleGen.split_evenly(total, len(positive_graphs))
        # list of all generated negative figures
        negative_graphs = NegativeExampleGen.generate_all_negative_graphs(positive_graphs, counts)
        if creates_files:
            for i, negative_graph in enumerate(negative_graphs):
                json = ToJson.from_networkx(negative_graph, 'default')
                # names are: 0.json, 1.json, 2.json, 3.json, ...
                ToJson.create_json_file('Summer-Research-2022/Negative shapes/', str(i), json)
        print(len(positive_graphs), len(negative_graphs))
        return negative_graphs
        
    # creates a list of groups that is num_of_splits long that adds up to total_count such that
    # the difference from the smallest group to the highest group is 0 or 1.
    #
    # total_count - total sum of all groups
    # num_of_splits - number of total groups
    #
    # returns evenly split groups
    @staticmethod
    def split_evenly(total_count, num_of_splits):
        # minimum amount contained in every group
        per_split = int(total_count / num_of_splits)
        # amount left over after placing minimum amount into each cell
        remainder = total_count % num_of_splits
        # indices that will recieve an extra one
        extras = random.sample([i for i in range(0, num_of_splits)], remainder)

        split_counts = [per_split for i in range(0, num_of_splits)]
        for i in extras:
            split_counts[i] += 1
        return split_counts

    # generates desired_counts negative figures
    #
    # positive_graphs - list of isomorphicaly unique textbook figures
    # desired_counts - list of desired number of repetitions of each textbook figure
    #                   * assocated with index not actual texbook figure
    #
    # returns the generated negative graphs
    @staticmethod
    def generate_all_negative_graphs(positive_graphs, desired_counts):
        negative_graphs = []
        # goes until there the number of negative graphs reaches the desired total
        while len(negative_graphs) < sum(desired_counts):
            # shuffles the textbook graphs to reduce bias
            random.shuffle(positive_graphs)
            for i, positive_graph in enumerate(positive_graphs):
                '''generated_negative_graphs = NegativeExampleGen.generate_all_possible_for_graph(positive_graph)'''
                negative_graphs = NegativeExampleGen.generate_negatives_from_graph(positive_graph,
                                                                                   sum(desired_counts),
                                                                                   negative_graphs,
                                                                                   desired_counts[i])
        return negative_graphs

    # generates a desired number of negative graphs from a single positive graph
    # 
    # pos_graphs - list of positive graphs
    # total_required - total number of graphs required overall
    # neg_graphs - list of current total negative graphs
    # desired_count - desired number of negative graphs for this positive graph
    # 
    # returns the list of generated negative graphs
    @staticmethod
    def generate_negatives_from_graph(pos_graph, total_required, neg_graphs, desired_count):
        # total number of negative graphs that have been generated before
        prior_count = len(neg_graphs)
        # total number of negative graphs that there is wanted to be at the end
        desired_position = desired_count + prior_count
        # list of the number of figures add at each itteration
        history = []
        

        itter = 0
        # goes until: the total number of graphs reaches the total number desired,
        #             the number of new graphs reaches the desired amount of this positive graph, or
        #             the program runs out of patience waiting for a new graph to be generated
        while(len(neg_graphs) < total_required and
              len(neg_graphs) < desired_position and
              (history[-1] != history[itter-PATIENCE] if itter >= PATIENCE else True)):
            # only appends the graph if it is not unchanged and hasn't been generated before
            graph = NegativeExampleGen.generate_random_isomorphic_graph(pos_graph.copy())
            if(not NegativeExampleGen.is_matching(graph, pos_graph) and
               not NegativeExampleGen.is_in(graph, neg_graphs)):
                neg_graphs.append(graph)
            history.append(len(neg_graphs)-prior_count)
            itter += 1
        return neg_graphs

    # generates a new graph that is isomorphic the the one passed in, but has randomized
    # node labels
    #
    # graph - passed in positive graph
    #
    # returns a graph with randomized node labels
    @staticmethod
    def generate_random_isomorphic_graph(graph):
        for node in graph:
            attribute = nx.get_node_attributes(graph, 'default')[node]
            attribute = NegativeExampleGen.random_shape_shift(attribute)
            nx.set_node_attributes(graph, {node: attribute}, 'default')
        return graph

    # randomly shifts a node label to another of the same size class
    #
    # attribute - the current attribute [shape, sides]
    #
    # returns the new attribute [new shape, same sides]
    @staticmethod
    def random_shape_shift(attribute):
        shape = random.choice(SIDES_FOR_SHAPES[attribute[1]])
        return [shape, attribute[1]]
    
    # reads all JSON files contained in Summer-Research-2022/Json shapes.
    # *only save graphs that are not isomorphic to prior ones
    # 
    # returns all of the contents as networkx graphs
    @staticmethod
    def read_all_positive_graphs():
        graphs = []

        directory = 'Summer-Research-2022/Json shapes'
        if os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith('.json'):
                        with open(os.path.join(dirpath, filename)) as f:
                            graph, label = ToStellarGraph.from_json(f.name)
                            graph = graph.to_networkx(feature_attr='default')
                            # only aquires new isomorphs
                            if not NegativeExampleGen.has_isomorphic_match(graph, graphs):
                                graphs.append(graph)
        else:
            print("File does not exist.")
        return graphs
    
    # reads all JSON files contained in Summer-Research-2022/Json shapes.
    # reports all that have been seen before as print output
    @staticmethod
    def determine_if_repeats():
        graphs = []

        directory = 'Summer-Research-2022/Json shapes'
        if os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith('.json'):
                        with open(os.path.join(dirpath, filename)) as f:
                            graph, label = ToStellarGraph.from_json(f.name)
                            graph = graph.to_networkx(feature_attr='default')
                            # only aquires new isomorphs
                            if not NegativeExampleGen.is_in(graph, graphs):
                                print(filename)
                                graphs.append(graph)
        else:
            print("File does not exist.")


    # determines whether or not a graph has a isomorphically identical graph from a list
    #
    # example_graph - graph being compared to the list
    # graphs - graphs being used for the comparison of the example graph
    #
    # returns whether the graph has an isomorphic match
    @staticmethod
    def has_isomorphic_match(example_graph, graphs):
        for graph in graphs:
            if nx.is_isomorphic(example_graph, graph):
                return True
        return False

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
            if NegativeExampleGen.is_matching(example_graph, graph):
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
    
    
    """

    May be Reimplemented if Needed
    (not certain to work)
    
    """
    
    # @staticmethod
    # def generate_all_possible_for_graph(graph:nx.MultiGraph, node=None):
    #     if node == None:
    #         return NegativeExampleGen.generate_all_possible_for_graph(graph, list(graph.nodes)[0])
    #     index = list(graph.nodes).index(node)
    #     if len(graph.nodes)-1 <= index: return []

    #     attribute = nx.get_node_attributes(graph, 'default')[node]
    #     graphs = NegativeExampleGen.generate_all_possible_for_node(graph, node, attribute)
    #     altered_graphs = graphs
    #     for altered_graph in graphs:
    #         altered_graphs.extend(NegativeExampleGen.generate_all_possible_for_graph(altered_graph.copy(), list(graph.nodes)[index+1]))
    #     return altered_graphs

    # @staticmethod
    # def generate_all_possible_for_node(graph, node, attribute):
    #     shapes = SIDES_FOR_SHAPES[attribute[1]]
    #     graphs = []
    #     for shape in shapes:
    #         graphs.append(NegativeExampleGen.create_with_altered_node(graph.copy(), node, [shape, attribute[1]]))
    #     return graphs

NegativeExampleGen.generate(101, False)