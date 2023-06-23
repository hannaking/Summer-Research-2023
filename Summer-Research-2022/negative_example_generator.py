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
        # list of all figures that are isomorphically unique positive examples
        positive_graphs = NegativeExampleGen.read_all_positive_graphs()
        # list, as long as the number of positive figures, that is split as evenly as possible
        # with the extras scattered randomly
        counts = NegativeExampleGen.split_evenly(total, len(positive_graphs))
        # list of all generated negative figures
        negative_graphs = NegativeExampleGen.generate_all_negative_graphs(positive_graphs, counts)
        print(len(positive_graphs))
        print(counts)
        if creates_files:
            for i, negative_graph in enumerate(negative_graphs):
                json = ToJson.from_networkx(negative_graph, 'default')
                # names are: 0.json, 1.json, 2.json, 3.json, ...
                ToJson.create_json_file('Summer-Research-2022/Negative shapes/', str(i), json)
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
    # positive_graphs - list of isomorphicaly unique positive figures
    # desired_counts - 
    @staticmethod
    def generate_all_negative_graphs(positive_graphs, desired_counts):
        negative_graphs = []
        while len(negative_graphs) < sum(desired_counts):
            random.shuffle(positive_graphs)
            for i, positive_graph in enumerate(positive_graphs):
                #generated_negative_graphs = NegativeExampleGen.generate_all_possible_for_graph(positive_graph)
                negative_graphs = NegativeExampleGen.generate_negatives_from_graph(positive_graph,
                                                                                   sum(desired_counts),
                                                                                   negative_graphs,
                                                                                   desired_counts[i])
        return negative_graphs

    @staticmethod
    def generate_negatives_from_graph(pos_graph, total_required, neg_graphs, desired_count):
        prior_count = len(neg_graphs)
        desired_position = desired_count + prior_count
        itter = 0
        history = []
        depth = 200
        while(len(neg_graphs) < total_required and
              len(neg_graphs) < desired_position and
              (history[-1] != history[itter-depth] if itter >= depth else True)):
            graph = NegativeExampleGen.generate_random_isomorphic_graph(pos_graph.copy())
            if(not NegativeExampleGen.is_matching(graph, pos_graph) and
               not NegativeExampleGen.is_in(graph, neg_graphs)):
                neg_graphs.append(graph)
            history.append(len(neg_graphs)-prior_count)
            itter += 1
        return neg_graphs

    @staticmethod
    def generate_random_isomorphic_graph(graph):
        for node in graph:
            attribute = nx.get_node_attributes(graph, 'default')[node]
            attribute = NegativeExampleGen.random_shape_shift(attribute)
            nx.set_node_attributes(graph, {node: attribute}, 'default')
        return graph

    @staticmethod
    def random_shape_shift(attribute):
        shape = random.choice(SIDES_FOR_SHAPES[attribute[1]])
        return [shape, attribute[1]]

    @staticmethod
    def subtract_graphs_from_set(base_graphs, subtract_graphs):
        pass

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
                            if not NegativeExampleGen.is_in(graph, graphs):
                                graphs.append(graph)
                            else:
                                print(filename)
        else:
            print("File does not exist.")
        print("====================")
        return graphs

    @staticmethod
    def has_isomorphic_match(example_graph, graphs):
        for graph in graphs:
            if nx.is_isomorphic(example_graph, graph):
                return True
        return False

    @staticmethod
    def is_in(example_graph, graphs):
        for graph in graphs:
            if NegativeExampleGen.is_matching(example_graph, graph):
                return True
        return False
        
    @staticmethod
    def is_matching(graph1, graph2):
        GM = iso.GraphMatcher(graph1, graph2, node_match=lambda n1, n2 : list(n1['default']) == list(n2['default']))
        return GM.is_isomorphic()
    
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

NegativeExampleGen.generate(115)