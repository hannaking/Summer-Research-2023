# Main file for the project.
# This file is responsible for the main flow of the program.

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


    # ======================================================================================================= #
    #                                                   Inputs

    # Create input shape list
    #                  [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]
    input_shape_list = [0,        1,         1,     0,         0,        0,         0       ] # counts

    # note: if a shape is handed enough points (minimum of 3) it can become a more rigorous shape
    # examples: NonIsoscelesRight --> IsoscelesRight
    #           Parallelogram --> Square

    # chooses the specific shapes that will appear in the generated figures
    # options: 'Segment',   'Equilateral', 'Isosceles',     'IsoscelesRight', 'NonIsoscelesRight', 'Square',
    #          'Rectangle', 'Rhombus',     'Parallelogram', 'Kite',           'RightTrapezoid',    'IsoTrapezoid',
    #          'Dart',      'RegularPent', 'RegularHex',    'RegularSept',    'RegularOct'
    shape_types = ['Square', 'IsoscelesRight', 'Equilateral']

    # ======================================================================================================= #

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
    
    # Show lattices.
    if show_lattices:

        for layer in [[lattices[1][-1]]]:
            for lattice, _ in layer:
                
                lattice.show()

    # Convert lattices to geometry figures.
    shape_generator = ShapeGenerator(shape_types)
    
    # puts the figures on the plane and removes overlapping figures
    shape_generator.generate_from_dual_lattice_pairs(lattices_final, dual_graphs, show_figures)
