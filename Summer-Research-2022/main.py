# Main file for the project.
# This file is responsible for the main flow of the program.
from random_face_graph_creator import RandomFaceGraphCreator
from to_json import ToJson
from lattice_generator import LatticeGenerator
from face_graphs.face_graph_generator import FaceGraphGenerator
from shapes.shape_generator import ShapeGenerator
from textbook_identifier import TextbookIdentifier

if __name__ == '__main__':

    show_lattices = False
    show_figures  = False

    if not show_lattices:
        print("Not showing lattices.")

    if not show_figures:
        print("Not showing figures.")

    print()

    # Create input shape list
    # [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]
    input_shape_list = [0, 1, 0, 0, 0, 0, 0]

    # Initialize the lattice generator.
    lattice_generator = LatticeGenerator(input_shape_list)
    
    # Generate the lattices.
    lattices = lattice_generator.glue_shapes()._lattice_matrix
    
    # Show lattices.
    if show_lattices:

        for layer in lattices:
            for lattice, _ in layer:
                
                lattice.show()

    # face graphs is a list of lists, each list containing the face graphs for one lattice
    # the lists are stored in the same order as their lattices are in lattices
    # so they are associated, bc I need the lattice for the face graph later when graphing to the plane.
    face_graphs = FaceGraphGenerator.from_lattices(lattices)
    
    face_graphs = [RandomFaceGraphCreator.create_random_face_graphs(100)]
    isTextbooks = TextbookIdentifier.identify(face_graphs, "model__1")
    print(isTextbooks)

    for i, graph_group in enumerate(face_graphs):
        for j, graph in enumerate(graph_group):
            json = ToJson.from_networkx(graph, 'default', 'generator', isTextbooks[i][j])
            ToJson.create_json_file("Summer-Research-2022/hold/", str(i) + str(j), json)

    # Determine shape types to use. Value of 'None' will include all shape types.
    # Options: 'Segment', 'Equilateral' ..... 'RegularPent', 'RegularHex', 'RegularSept', 'RegularOct'
    shape_types = ['RegularPent']

    # Convert lattices to geometry figures.
    shape_generator = ShapeGenerator(shape_types)

    # Generate the figures. Returns tuple in the form (list of coordinates, corresponding lattice)
    figures = shape_generator.generate_from_lattice_matrix(lattices, show_figures)
