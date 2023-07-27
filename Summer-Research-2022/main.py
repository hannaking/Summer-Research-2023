# Main file for the project.
# This file is responsible for the main flow of the program.
#from analyzer import Analyzer
#from random_face_graph_creator import RandomFaceGraphCreator
#from to_json import ToJson
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
    #                  [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]
    input_shape_list = [0,        1,         1,     0,         0,        0,         0       ]

    # Initialize the lattice generator.
    lattice_generator = LatticeGenerator(input_shape_list)
    
    # Generate the lattices.
    lattices = lattice_generator.glue_shapes()._lattice_matrix
    
    # removes the partial figure lattices and unnecessary detail
    lattices_final = lattice_generator.constrain_to_final(lattices, sum(input_shape_list))

    # generates the associated dual graphs for each lattice
    dual_graphs = FaceGraphGenerator.from_lattices(lattices_final)

    # reduces the lattices and graphs to only those the model considers to be textbook-like
    key = TextbookIdentifier.identify(dual_graphs, "model__1")
    lattices_final, dual_graphs = TextbookIdentifier.get_only_in_textbook(lattices_final, dual_graphs, key)
    
    # re-adds certain detail for the old figure generator
    refomatted_final = [[(lattice, [0, 0, 0, 0, 0, 0, 0]) for lattice in lattices_final]]

    # Show lattices.
    if show_lattices:

        for layer in [[lattices[1][-1]]]:
            for lattice, _ in layer:
                
                lattice.show()

    # face graphs is a list of lists, each list containing the face graphs for one lattice
    # the lists are stored in the same order as their lattices are in lattices
    # so they are associated, bc I need the lattice for the face graph later when graphing to the plane.

    # note: if a shape is handed enough points (minimum of 3) it can become a more rigorius shape
    # examples: NonIsoscelesRight --> IsoscelesRight
    #           Parallelogram --> Square

    # chooses the specific shapes that will appear in the generated figures
    # options: 'Segment',   'Equilateral', 'Isosceles',     'IsoscelesRight', 'NonIsoscelesRight', 'Square',
    #          'Rectangle', 'Rhombus',     'Parallelogram', 'Kite',           'RightTrapezoid',    'IsoTrapezoid',
    #          'Dart',      'RegularPent', 'RegularHex',    'RegularSept',    'RegularOct'
    shape_types = ['Square', 'IsoscelesRight', 'Equilateral']

    # Convert lattices to geometry figures.
    shape_generator = ShapeGenerator(shape_types)
    
    # puts the figures on the plane and removes overlapping figures
    # shape_generator.generate_from_dual_lattice_pairs(lattices_final, dual_graphs, show_figures)

    figures = 0
    for i, (lattice, graphs) in enumerate(zip(lattices_final, dual_graphs)):
        print("Lattices:", str(i+1) + "/" + str(len(lattices_final)))
        if True:
            for j, graph in enumerate(graphs):
                print("      Dual Graphs:", str(j+1) + "/" + str(len(graphs)))
                if True:
                    figures += shape_generator.generate_from_dual_lattice_pairs([lattice], [[graph]], show_figures)
    print(figures)
