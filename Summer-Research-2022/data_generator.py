from collections import defaultdict
import os
import networkx as nx
from to_stellar_graph import ToStellarGraph
import matplotlib.pyplot as plt

def datareader():
    NUMBER_SHAPE_MAP = {
        00: "Line Segment",
        10: "Isosceles Right Triangle",
        11: "Right Triangle",
        12: "Equilateral Triangle",
        13: "Isosceles Triangle",
        20: "Square",
        21: "Rectangle",
        22: "Rhombus",
        23: "Parallelogram",
        24: "Kite",
        25: "Right Trapezoid",
        26: "Isosceles Trapezoid",
        27: "Dart",
        30: "Regular Pentagon",
        40: "Regular Hexagon",
        50: "Regular Septagon",
        60: "Regular Octagon"
    }

    Shape_Count = defaultdict(int)

    directory = 'Summer-Research-2022/Json shapes'
    if os.path.exists(directory):
        valid_extensions = {'.json'}
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if os.path.splitext(filename)[1] in valid_extensions:
                    with open(os.path.join(dirpath, filename)) as f:
                        graph, label = ToStellarGraph.from_json(f.name)
                        graph = graph.to_networkx(feature_attr='default')
                        data = nx.get_node_attributes(graph, 'default')
                        for i in data:
                            shape_number = data[i][0]
                            shape_name = NUMBER_SHAPE_MAP.get(shape_number)
                            if shape_name:
                                Shape_Count[shape_name] += 1

    print(Shape_Count)

def create_histogram(data):
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

    # Add labels and titles
    ax.set_xlabel('Shapes')
    ax.set_ylabel('Count')
    ax.set_title('Shape Counts')

    # Customize the appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Add color labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                shape_counts[i], ha='center', va='bottom')

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=90)

    # Display the histogram
    plt.tight_layout()
    plt.show()

# Call the function with your Shape_Count data
Shape_Count = {
    'Line Segment': 20,
    'Right Triangle': 87,
    'Isosceles Triangle': 91,
    'Equilateral Triangle': 66,
    'Isosceles Trapezoid': 38,
    'Kite': 11,
    'Dart': 6,
    'Regular Hexagon': 27,
    'Regular Pentagon': 21,
    'Parallelogram': 21,
    'Square': 77,
    'Regular Octagon': 10,
    'Rectangle': 56,
    'Regular Septagon': 1,
    'Rhombus': 2,
    'Isosceles Right Triangle': 21,
    'Right Trapezoid': 11
}

create_histogram(Shape_Count)


create_histogram(Shape_Count)
datareader()
