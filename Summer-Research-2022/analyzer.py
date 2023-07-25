import itertools as itt
import json
import math
from matplotlib import pyplot as plt
from matplotlib import ticker as mtick
import networkx as nx
import numpy as np
from scipy import stats
import pandas as pd

from random_face_graph_creator import RandomFaceGraphCreator
from textbook_identifier import TextbookIdentifier
from to_json import ToJson
from face_graphs.face_graph_generator import FaceGraphGenerator
from lattice_generator import LatticeGenerator
from negative_example_generator import NegativeExampleGen
from gcn_graph_classification import GraphClassifier

#      Catagory     |     Textbook     |   Not-Textbook   |       Base       
# ==================|==================|==================|==================
# count             |                  |                  |                  
# <shapes>          |                  |                  |                  
# <pairs>           |                  |                  |                  
# mean Edge Degree  |                  |                  |                  
# std Edge Degree   |                  |                  |                  
# max Edge Degree   |                  |                  |                  
# min Edge Degree   |                  |                  |                  
# mean Node Degree  |                  |                  |                  
# std Node Degree   |                  |                  |                  
# max Node Degree   |                  |                  |                  
# min Node Degree   |                  |                  |                  
# mean Edge Count   |                  |                  |                  
# std Edge Count    |                  |                  |                  
# max Edge Count    |                  |                  |                  
# min Edge Count    |                  |                  |                  
# mean Node Count   |                  |                  |                  
# std Node Count    |                  |                  |                  
# max Node Count    |                  |                  |                  
# min Node Count    |                  |                  |                  

NUMBER_SHAPE_MAP = {00 : "Line Segment",
                    10 : "Isosceles Right Triangle",
                    11 : "Right Triangle",
                    12 : "Equilateral Triangle",
                    13 : "Isosceles Triangle",
                    20 : "Square",
                    21 : "Rectangle",
                    22 : "Rhombus",
                    23 : "Parallelogram",
                    24 : "Kite",
                    25 : "Right Trapezoid",
                    26 : "Isosceles Trapezoid",
                    27 : "Dart",
                    30 : "Regular Pentagon",
                    40 : "Regular Hexagon",
                    50 : "Regular Septagon",
                    60 : "Regular Octagon"}
SHAPE_NUMBER_MAP = {shape : code for code, shape in NUMBER_SHAPE_MAP.items()}

SHAPE = 0

class Analyzer():

    @staticmethod
    def calculate_percents(base_counts, textbook_counts):
        percent_counts = dict.fromkeys(base_counts.keys(), 0)

        for key in percent_counts:
            if base_counts[key] != 0:
                percent_counts[key] = float(textbook_counts[key]) / float(base_counts[key])
            else:
                percent_counts[key] = 0
        
        return percent_counts

    @staticmethod
    def calculate_shape_parts(textbook_shape_counts, textbook_total):
        part_counts = {name : 0 for name in NUMBER_SHAPE_MAP.values()}

        for shape in part_counts:
            part_counts[shape] = float(textbook_shape_counts[shape]) / float(textbook_total)

        return part_counts
    
    def calculate_node_parts(textbook_node_counts, textbook_total):
        part_counts = dict.fromkeys(textbook_node_counts, 0)

        for count in part_counts:
            part_counts[count] = float(textbook_node_counts[count]) / float(textbook_total)

        return part_counts

    @staticmethod
    def split_pairs(pairs):
        splits = []
        for pair in pairs:
            splits.append(Analyzer.split_pair(pair))
        return splits

    @staticmethod
    def split_pair(pair):
        return tuple(pair.split(", "))

    @staticmethod
    def merge_pair(shape1, shape2):
        if type(shape1) == str: shape1 = SHAPE_NUMBER_MAP[shape1]
        if type(shape2) == str: shape2 = SHAPE_NUMBER_MAP[shape2]
        
        shape1, shape2 = sorted([shape1, shape2])
        
        shape1 = NUMBER_SHAPE_MAP[shape1]
        shape2 = NUMBER_SHAPE_MAP[shape2]
        
        return shape1 + ", " + shape2

    @staticmethod
    def draw_qq_plots_parts():
        data = Analyzer.read_data("Summer-Research-2022/hold", "textbook_118.json")
        positive_shape_counts = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
        data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")
        textbook_shape_percents = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
        pos_shapes = pd.Series(positive_shape_counts.values())
        txt_shapes = pd.Series(textbook_shape_percents.values())

        Analyzer.draw_qq_plot_parts(pos_shapes, "Textbook Shapes per Figure Q-Q Plot", "textbook_parts_qqplot")
        Analyzer.draw_qq_plot_parts(txt_shapes, "Textbook-like Shapes per Figure Q-Q Plot", "textbook_like_parts_qqplot")

    @staticmethod
    def draw_qq_plot_parts(data, title, name):
        stats.probplot(data, dist="norm", plot= plt)
        plt.title(title)
        plt.savefig(name + ".png")
        plt.close()

    @staticmethod
    def aquire_willingness():
        data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")
        textbook_pair_percents = Analyzer.calculate_percents(data["Base"]["Pair Counts"], data["Textbook"]["Pair Counts"])
        textbook_pair_counts = data["Textbook"]["Pair Counts"]
        base_pair_counts = data["Base"]["Pair Counts"]
        textbook_shape_counts = data["Textbook"]["Shape Counts"]
        base_shape_counts = data["Base"]["Shape Counts"]

        pairs = []
        for pair in textbook_pair_counts:
            p1, p2 = Analyzer.split_pair(pair)
            p1 = SHAPE_NUMBER_MAP[p1]
            p2 = SHAPE_NUMBER_MAP[p2]
            pair = str(p1) + ", " + str(p2)
            inverse_pair = str(p2) + ", " + str(p1)
            pairs.append(pair)
            pairs.append(inverse_pair)
        pairs = sorted(pairs)

        bse_count = {}
        for pair in pairs:
            p1, p2 = Analyzer.split_pair(pair)
            p1 = NUMBER_SHAPE_MAP[int(p1)]
            p2 = NUMBER_SHAPE_MAP[int(p2)]
            pair = p1 + ", " + p2
            bse_count[pair] = 0

        for pair in bse_count.keys():
            p1, p2 = Analyzer.split_pair(pair)
            if p1 == p2:
                bse_count[pair] += math.comb(base_shape_counts[p1]+1, 2)
            else:
                bse_count[pair] += base_shape_counts[p1] * base_shape_counts[p2]

        base_per_rep = bse_count.copy()
        maximum = bse_count[max(bse_count, key=lambda key: bse_count[key])]
        for pair in bse_count:
            base_per_rep[pair] /= maximum

        base_pair_rep = base_pair_counts.copy()

        for pair in pairs:
            p1, p2 = Analyzer.split_pair(pair)
            p1 = NUMBER_SHAPE_MAP[int(p1)]
            p2 = NUMBER_SHAPE_MAP[int(p2)]
            pair = p1 + ", " + p2
            sorted_pair = Analyzer.merge_pair(p1, p2)
            base_pair_rep[pair] = base_pair_counts[sorted_pair]

        maximum = base_pair_rep[max(base_pair_rep, key=lambda key: base_pair_rep[key])]
        for pair in base_pair_rep:
            base_pair_rep[pair] /= base_per_rep[pair]

        Analyzer._create_histogram(base_pair_counts, False, "base")
        Analyzer._create_histogram(base_pair_rep, False, "Thing")
        Analyzer._create_histogram(base_per_rep, False, "Per")

        txt_count = {}
        for pair in pairs:
            p1, p2 = Analyzer.split_pair(pair)
            p1 = NUMBER_SHAPE_MAP[int(p1)]
            p2 = NUMBER_SHAPE_MAP[int(p2)]
            pair = p1 + ", " + p2
            txt_count[pair] = 0

        for pair in txt_count.keys():
            p1, p2 = Analyzer.split_pair(pair)
            if p1 == p2:
                txt_count[pair] += math.comb(textbook_shape_counts[p1]+1, 2)
            else:
                txt_count[pair] += textbook_shape_counts[p1] * textbook_shape_counts[p2]

        textbook_per_rep = txt_count.copy()
        maximum = textbook_per_rep[max(textbook_per_rep, key=lambda key: textbook_per_rep[key])]
        for pair in txt_count:
            textbook_per_rep[pair] /= maximum

        textbook_pair_rep = textbook_pair_counts.copy()

        for pair in pairs:
            p1, p2 = Analyzer.split_pair(pair)
            p1 = NUMBER_SHAPE_MAP[int(p1)]
            p2 = NUMBER_SHAPE_MAP[int(p2)]
            pair = p1 + ", " + p2
            sorted_pair = Analyzer.merge_pair(p1, p2)
            textbook_pair_rep[pair] = textbook_pair_counts[sorted_pair]

        maximum = textbook_pair_rep[max(textbook_pair_rep, key=lambda key: textbook_pair_rep[key])]
        for pair in textbook_pair_rep:
            textbook_pair_rep[pair] /= textbook_per_rep[pair]

        Analyzer._create_histogram(textbook_pair_counts, False, "Textbook")
        Analyzer._create_histogram(textbook_pair_rep, False, "TXT Thing")
        Analyzer._create_histogram(textbook_per_rep, False, "TXT Per")

        Analyzer._create_histogram(Analyzer.calculate_percents(base_pair_rep, textbook_pair_rep), True, "A Thing")

    @staticmethod
    def perform_test_parts():
        data = Analyzer.read_data("Summer-Research-2022/hold", "textbook_118.json")
        positive_shape_counts = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
        data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")
        textbook_shape_percents = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
        pos_shapes = pd.Series(positive_shape_counts.values())
        txt_shapes = pd.Series(textbook_shape_percents.values())

        print(stats.shapiro(pos_shapes))
        print(stats.shapiro(txt_shapes))
        print(stats.mannwhitneyu(pos_shapes, txt_shapes))

        fig = plt.figure(figsize= (10, 5))
        ax = fig.add_subplot(111)
        ax.set_xlabel("Average Shape Instances per Figures")
        ax.set_ylabel("number of Shape Types")
        plt.hist(pos_shapes, label= "Textbook Shapes", density= False, alpha=0.5)
        plt.hist(txt_shapes, label= "Textbook-Like Shapes", density= False, alpha=0.5)
        plt.legend()
        plt.text(0, 5.6, f"Textbook-Like: $\mu= {txt_shapes.mean()}, \ \sigma= {txt_shapes.std()}$")
        plt.text(0, 5.4, f"Textbook: $\mu= {pos_shapes.mean()}, \ \sigma= {pos_shapes.std()}$")
        plt.show()

    @staticmethod
    def flatten_reps(data):
        flattened = []
        for key, reps in data.items():
            for i in range(0, reps):
                flattened.append(int(key))
        return flattened

    @staticmethod
    def perform_test_nodes():
        data = Analyzer.read_data("Summer-Research-2022/hold", "textbook_118.json")
        textbook_sizes = Analyzer.flatten_reps(data["Textbook"]["Node Count Info"]["count"])
        
        data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")
        textbook_like_sizes = Analyzer.flatten_reps(data["Textbook"]["Node Count Info"]["count"])
        
        txt_sizes = pd.Series(textbook_sizes)
        txt_lk_sizes = pd.Series(textbook_like_sizes)
        print(len(txt_sizes), len(txt_lk_sizes))
        print(stats.shapiro(txt_sizes))
        print(stats.shapiro(txt_lk_sizes))
        print(stats.mannwhitneyu(txt_sizes, txt_lk_sizes))
        print(txt_sizes)
        fig = plt.figure(figsize= (10, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Distribution of Figure Sizes")
        ax.set_xlabel("Figure Size")
        ax.set_ylabel("Percent")
        plt.hist(txt_sizes,    label= "Textbook Sizes",      density= True, alpha=0.5)
        plt.hist(txt_lk_sizes, label= "Textbook-Like Sizes", density= True, alpha=0.5)
        plt.legend()
        plt.text(0, 5.6, f"Textbook-Like: $\mu= {txt_lk_sizes.mean()}, \ \sigma= {txt_lk_sizes.std()}$")
        plt.text(0, 5.4, f"Textbook: $\mu= {txt_sizes.mean()}, \ \sigma= {txt_sizes.std()}$")
        plt.show()

    @staticmethod
    def read_data(directory, name):
        json_file = open(directory + "/" +name)
        return json.load(json_file)

    @staticmethod
    def analyze(graphs:list[list[nx.MultiGraph]], labels, name="analysis_data"):

        textbook_total = sum([sum(lbl_lst) for lbl_lst in labels])
        non_textbook_total = sum([len(lbl_lst) for lbl_lst in labels])  - textbook_total

        textbook_node_degrees = []
        non_textbook_node_degrees = []
        base_node_degrees = []
        
        textbook_edge_degrees = []
        non_textbook_edge_degrees = []
        base_edge_degrees = []

        textbook_node_count = []
        non_textbook_node_count = []
        base_node_count = []

        textbook_edge_count = []
        non_textbook_edge_count = []
        base_edge_count = []

        for i, graph_group in enumerate(graphs):
            for j, graph in enumerate(graph_group):
                if labels[i][j]:
                    # construct lists for textbook-like info
                    for degree in list(dict(graph.degree).values()):
                        textbook_node_degrees.append(degree)
                    for degree in [graph.number_of_edges(u, v) for u, v, c in graph.edges]:
                        textbook_edge_degrees.append(degree)
                    textbook_node_count.append(len(graph.nodes))
                    textbook_edge_count.append(len(graph.edges))
                else:
                    # construct lists for non-textbook-like info
                    for degree in list(dict(graph.degree).values()):
                        non_textbook_node_degrees.append(degree)
                    for degree in [graph.number_of_edges(u, v) for u, v, c in graph.edges]:
                        non_textbook_edge_degrees.append(degree)
                    non_textbook_node_count.append(len(graph.nodes))
                    non_textbook_edge_count.append(len(graph.edges))
                # construct lists for base info
                for degree in list(dict(graph.degree).values()):
                    base_node_degrees.append(degree)
                for degree in [graph.number_of_edges(u, v) for u, v, c in graph.edges]:
                    base_edge_degrees.append(degree)
                base_node_count.append(len(graph.nodes))
                base_edge_count.append(len(graph.edges))
        
        
        textbook_node_degree_info = Analyzer.get_info(textbook_node_degrees)
        textbook_node_count_info = Analyzer.get_info(textbook_node_count)
        textbook_edge_degree_info = Analyzer.get_info(textbook_edge_degrees)
        textbook_edge_count_info = Analyzer.get_info(textbook_edge_count)

        non_textbook_node_degree_info = Analyzer.get_info(non_textbook_node_degrees)
        non_textbook_node_count_info = Analyzer.get_info(non_textbook_node_count)
        non_textbook_edge_degree_info = Analyzer.get_info(non_textbook_edge_degrees)
        non_textbook_edge_count_info = Analyzer.get_info(non_textbook_edge_count)

        base_node_degree_info = Analyzer.get_info(base_node_degrees)
        base_node_count_info = Analyzer.get_info(base_node_count)
        base_edge_degree_info = Analyzer.get_info(base_edge_degrees)
        base_edge_count_info = Analyzer.get_info(base_edge_count)

        textbook_shape_counts = {name : 0 for name in NUMBER_SHAPE_MAP.values()}
        non_textbook_shape_counts = textbook_shape_counts.copy()

        textbook_shape_inclusions = textbook_shape_counts.copy()
        non_textbook_shape_inclusions = textbook_shape_counts.copy()

        textbook_pair_counts = Analyzer._get_all_pairs()
        non_textbook_pair_counts = textbook_pair_counts.copy()
        
        textbook_pair_inclusions = textbook_pair_counts.copy()
        non_textbook_pair_inclusions = textbook_pair_counts.copy()

        for i, graph_group in enumerate(graphs):
            for j, graph in enumerate(graph_group):
                shapes = Analyzer._get_shapes(graph)
                for a_shape in shapes:
                        if labels[i][j]: textbook_shape_counts[a_shape] += 1
                        else: non_textbook_shape_counts[a_shape] += 1
                for shape in NUMBER_SHAPE_MAP.values():
                    if shape in shapes:
                        if labels[i][j]: textbook_shape_inclusions[shape] += 1
                        else: non_textbook_shape_inclusions[shape] += 1

        for i, graph_group in enumerate(graphs):
            for j, graph in enumerate(graph_group):
                pairs = Analyzer._get_shape_pairs(graph)
                for pair in pairs:
                        if labels[i][j]: textbook_pair_counts[pair] += 1
                        else: non_textbook_pair_counts[pair] += 1
                for shape_pair in textbook_pair_counts.keys():
                    if shape_pair in pairs:
                        if labels[i][j]: textbook_pair_inclusions[shape_pair] += 1
                        else: non_textbook_pair_inclusions[shape_pair] += 1

        analysis = {
            "Textbook" : {
                "Total"            : textbook_total,
                "Node Degree Info" : textbook_node_degree_info,
                "Node Count Info"  : textbook_node_count_info,
                "Edge Degree Info" : textbook_edge_degree_info,
                "Edge Count Info"  : textbook_edge_count_info,
                "Shape Counts"     : textbook_shape_counts,
                "Shape Inclusion"  : textbook_shape_inclusions,
                "Pair Counts"      : textbook_pair_counts,
                "Pair Inclusion"   : textbook_pair_inclusions
            },
            "Non-Textbook" : {
                "Total"            : non_textbook_total,
                "Node Degree Info" : non_textbook_node_degree_info,
                "Node Count Info"  : non_textbook_node_count_info,
                "Edge Degree Info" : non_textbook_edge_degree_info,
                "Edge Count Info"  : non_textbook_edge_count_info,
                "Shape Counts"     : non_textbook_shape_counts,
                "Shape Inclusion"  : non_textbook_shape_inclusions,
                "Pair Counts"      : non_textbook_pair_counts,
                "Pair Inclusion"   : non_textbook_pair_inclusions
            },
            "Base" : {
                "Total"            : Analyzer.get_base_values(textbook_total, non_textbook_total),
                "Node Degree Info" : base_node_degree_info,
                "Node Count Info"  : base_node_count_info,
                "Edge Degree Info" : base_edge_degree_info,
                "Edge Count Info"  : base_edge_count_info,
                "Shape Counts"     : Analyzer.get_base_values(textbook_shape_counts, non_textbook_shape_counts),
                "Shape Inclusion"  : Analyzer.get_base_values(textbook_shape_inclusions, non_textbook_shape_inclusions),
                "Pair Counts"      : Analyzer.get_base_values(textbook_pair_counts, non_textbook_pair_counts),
                "Pair Inclusion"   : Analyzer.get_base_values(textbook_pair_inclusions, non_textbook_pair_inclusions)
            }
        }

        json_data = json.dumps(analysis, indent=4)

        ToJson.create_json_file("Summer-Research-2022/hold/", name, json_data)
    
    @staticmethod
    def _get_all_pairs():
        code_combos = itt.combinations_with_replacement(NUMBER_SHAPE_MAP.keys(), 2)
        code_combos = sorted(sorted(pair) for pair in code_combos)
        for i, combo in enumerate(code_combos):
            for j, code in enumerate(combo):
                code_combos[i][j] = NUMBER_SHAPE_MAP[code]
            code_combos[i] = str(code_combos[i]).replace('[','').replace(']','').replace("'",'')
        return dict.fromkeys(code_combos, 0)

    @staticmethod
    def _get_shapes(graph):
        shapes = []
        attributes = nx.get_node_attributes(graph, 'default')
        for att in attributes.values():
            shapes.append(NUMBER_SHAPE_MAP[att[SHAPE]])
        return shapes
    
    @staticmethod
    def _get_shape_pairs(graph):
        edge_shapes = []
        attributes = nx.get_node_attributes(graph, 'default')
        for u, v in graph.edges():
            shape_u = NUMBER_SHAPE_MAP[attributes[u][SHAPE]]
            shape_v = NUMBER_SHAPE_MAP[attributes[v][SHAPE]]
            edge_shapes.append(Analyzer.merge_pair(shape_u, shape_v))
        return edge_shapes
    
    @staticmethod
    def get_base_values(textbook_values, non_textbook_values):
        if type(textbook_values) != dict:
            return textbook_values + non_textbook_values
        else:
            base_values = {}
            for data in textbook_values:
                base_values[data] = Analyzer.get_base_values(textbook_values[data], non_textbook_values[data])
            return base_values

    @staticmethod
    def get_info(information):
        count = dict.fromkeys(sorted(information), 0)
        for info in information:
            count[info] += 1
        
        if information != []:
            return {"mean"               : float(np.mean(information)),
                    "standard deviation" : float(np.std(information)),
                    "max"                : int(np.amax(information)),
                    "min"                : int(np.amin(information)),
                    "count"              : count}
        else:
            return {"mean"               : -1,
                    "standard deviation" : -1,
                    "max"                : -1,
                    "min"                : -1,
                    "count"              : count}
        
    @staticmethod
    def remove_duplicates(graphs, labels):
        unique_graphs = []
        unique_labels = []
        for graph_group in enumerate(graphs):
            unique_group = []
            for graph in enumerate(graph_group):
                if not RandomFaceGraphCreator.is_in(graph, graphs):
                    unique_group.append(graph)
            if unique_group != []:
                unique_graphs.append(unique_group.copy())
        return unique_graphs

    @staticmethod
    def _create_histogram(data, is_percent, name):
        # Extract the shape names and counts
        shape_names = list(data.keys())
        shape_counts = list(data.values())

        # Set the colors for each shape
        colors = ['blue', 'green', 'red', 'yellow', 'orange', 'purple', 'cyan',
                  'magenta', 'gray', 'brown']

        # Create the figure and axes
        fig, ax = plt.subplots()

        # Create the histogram
        bars = ax.bar(shape_names, shape_counts, color=colors)
        if is_percent:
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=2))

        # Add labels and titles
        ax.set_xlabel('Shapes')
        if is_percent:
            ax.set_ylabel('Percent')
        else:
            ax.set_ylabel('Count')
        ax.set_title(name)

        # Customize the appearance
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # Add color labels
        if is_percent:
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                    str(round(shape_counts[i] * 100, 1)) + "%", ha='center', va='bottom')
        else:
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                    round(shape_counts[i], 2), ha='center', va='bottom')

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation= -90)

        # Display the histogram
        #plt.tight_layout()
        plt.show()

#face_graphs = []
#c = 0
#quant = 10000
#for i in range(0, quant):
#    if c%int(quant/10) == 0:
#        print(c)
#    c+=1
#face_graphs = RandomFaceGraphCreator.create_random_face_graphs(quant)

#isTextbooks = TextbookIdentifier.identify_group(face_graphs, "model__1")

#Analyzer.analyze([face_graphs], [isTextbooks], "data_random_" + str(quant))

#data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")

#textbook_shape_percents = Analyzer.calculate_percents(data["Base"]["Shape Counts"], data["Textbook"]["Shape Counts"])
#textbook_pair_percents = Analyzer.calculate_percents(data["Base"]["Pair Counts"], data["Textbook"]["Pair Counts"])

#Analyzer._create_histogram(textbook_pair_percents, True, "Percents")

#Analyzer._create_histogram(textbook_pair_percents, True, "Percents")

#Analyzer._create_histogram(textbook_pair_percents, True, "Percents")

# SHAPES = {0 : "Segment",
#           1 : "Triangle",
#           2 : "Quadralateral",
#           3 : "Pentagon",
#           4 : "Hexagon",
#           5 : "Heptagon",
#           6 : "Octagon"}

# data_size_3 = {}
# length = 1
# for com in itt.combinations_with_replacement(range(0,7), length):
#     input_shape_list = [0, 0, 0, 0, 0, 0, 0]
#     for i in com: input_shape_list[i] += 1

#     shapes = []
#     for i, input in enumerate(input_shape_list):
#         for inp in range(0, input):
#             shapes.append(SHAPES[i])

#     data_size_3[tuple(shapes)] = Analyzer.read_data("Summer-Research-2022/hold/inputs/size_1", "input_" + str(input_shape_list) + ".json")

# total_size_3 = {key : {}.copy() for key in data_size_3}
# for shapes, inp in data_size_3.items():
#     total_size_3[shapes]["Textbook"] = inp["Textbook"]["Total"]
#     total_size_3[shapes]["Base"]     = inp["Base"]["Total"]

# for (shape1), total in total_size_3.items():
#     print(total["Base"])

#print(pair_percents)

# length = 3
# for com in itt.combinations_with_replacement(range(0,7), length):
#     input_shape_list = [0, 0, 0, 0, 0, 0, 0]
#     for i in com: input_shape_list[i] += 1

#     lattice_generator = LatticeGenerator(input_shape_list)
#     lattices = lattice_generator.glue_shapes()._lattice_matrix
#     lattices = lattice_generator.constrain_to_final(lattices, length)
    
#     face_graphs = FaceGraphGenerator.from_lattices(lattices)
#     isTextbooks = TextbookIdentifier.identify(face_graphs, "model__1")

#     Analyzer.analyze(face_graphs, isTextbooks, "inputs/size_" + str(length) + "/input_" + str(input_shape_list))

# Analyzer.perform_test_parts()

# Analyzer.draw_qq_plots_parts()

#data = Analyzer.read_data("Summer-Research-2022/hold", "textbook_118.json")

#textbook_node_counts = data["Textbook"]["Node Count Info"]["count"]
#base_node_counts = data["Base"]["Node Count Info"]["count"]

#for amount in textbook_node_counts:
#    textbook_node_counts[amount] /= base_node_counts[amount]

#Analyzer._create_histogram(textbook_node_counts, True, "Node Counts")

#Analyzer.perform_test_parts()

# data = Analyzer.read_data("Summer-Research-2022/hold", "textbook_118.json")
# positive_shape_parts = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
# data = Analyzer.read_data("Summer-Research-2022/hold", "data_repeated_100000.json")
# textbook_shape_parts = Analyzer.calculate_shape_parts(data["Textbook"]["Shape Counts"], data["Textbook"]["Total"])
        
# pos_shapes = pd.Series(positive_shape_parts.values())
# txt_shapes = pd.Series(textbook_shape_parts.values())
# print(pos_shapes)
# plt.figure()
# plt.scatter(np.sort(pos_shapes), np.sort(txt_shapes))
# plt.xlabel('Percent Textbook-like Shape Distribution')
# plt.ylabel('Percent Textbook Shape Distribution')
# plt.show()
# plt.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# shape breakdown:
#   percent - percent of the total number of each shape found in textbook-like examples vs how many there are total
#                 * textbook-like <shape>s per <shape>
#   count   - total number of each shape found in textbook-like examples
#                 * textbook-like <shape>s
#   parts   - average number of each shape found in a textbook-line figure
#                 * textbook-like <shape>s per textbook-like figure
#   base    - total number of each shape found
#                 * <shape>s
#
# *textbook-like <shape>: <shape> that comes from a textbook-like figure

# inclusion breakdown:
#   percent - percent of figures that include each shape found in the textbook-like examples vs how many there are in all examples
#                 * textbook-like figures containing <shape> per figure containing <shape>
#   count   - total number of figures that include each shape found in the textbook-like examples
#                 * textbook-like figures containing <shape>
#   parts   - percent of figures that include each shape found in the textbook-like examples
#                 * textbook-like figures containing <shape> per textbook-like figure
#   base    - total number of figures that include each shape found
#                 * figures containing <shape>


# most textbook figures are built from trianges or contain triangles
# most repeated is 2 edge glued right triangles (2x next one)
# most figures have 1, 2 or 4 shapes
# 1 is by far the most common
# 3 figures shapes are rarer
# large figures tend to have 1 or 2 types of shapes

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# smaller figures are very perfered to larger figures

# most textbook figures have triangles

# the paterns are from <not to less> present with less than 10000 graphs

# very few line-segments pass, then has a peak with the triangles, before noticably decreasing upon hitting the quadralaterals,
# then slopping downward to near nothing until octagons

# smaller number of sides is better until 1 which is bad
# smaller shape code is better until 0 which is bad

# less than half of the figures contain any given shape

# 61.9% accuracy on the textbook graphs
# 83.1% accuracy on the non-textbook graphs

# it generally perfers edges between one smaller and one larger shape
# Right Triangle, Regular Octagon - 63.3%
# Isosceles Right Triangle, Regular Septagon - 62.0%
# Isosceles Right Triangle, Regular Hexagon - 58.9%
# Equilateral Triangle, Regular Septagon - 57.5%
# Equilateral Triangle, Regular Pentagon - 54.1%
# Isosceles Right Triangle, Regular Pentagon - 51.7%
# Isosceles Right Triangle, Regular Octagon - 50.5%

# Shapes
#
# Textbook shapiro test:
#                       statistic = 0.8537275791168213 
#                       p-value   = 0.012230399064719677
#       * not normal distribution
# Textbook-like shapeiro test:
#                       statistic = 0.9082025289535522
#                       p-value   = 0.09328904747962952
#       * not likely normal distribution
# Mannwhitneyu test:
#                       statistic(textbook)      = 164.0
#                       statistic(textbook-like) = 125.0
#                       p-value                  = 0.5126755928763647
#       * different

# Nodes
#
# Textbook shapiro test:
#                       statistic = 0.7588671445846558
#                       p-value   = 0.0000000000012226482846988684
#       * not normal distribution
# Textbook-like shapeiro test:
#                       statistic = 0.8589462041854858
#                       p-value   = ~0 (N is to high for accurate results)
#       * not notmal distribution
# Mannwhitneyu test:
#                       statistic(textbook)      = 1146147.5
#                       statistic(textbook-like) = 688516.5
#                       p-value                  = 0.000002076427567519129
#       * similier