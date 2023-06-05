# Main file for the project.
# This file is responsible for the main flow of the program.
from lattice_generator import LatticeGenerator
from shapes.shape_generator import ShapeGenerator

if __name__ == '__main__':

    show_lattices = False
    show_figures  = False

    if not show_lattices:
        print("Not showing lattices.")

    if not show_figures:
        print("Not showing figures.")

    print()

    # Create input shape list
    # [Segments, Triangles, Quads, Hexagons, ..., Octagons]
    input_shape_list = [0, 1, 1]

    # Initialize the lattice generator.
    lattice_generator = LatticeGenerator(input_shape_list)

    # Generate the lattices.
    lattices = lattice_generator.glue_shapes()._lattice_matrix

    # Show lattices.
    if show_lattices:

        for layer in lattices:
            for lattice, _ in layer:

                lattice.show()

    # Determine shape types to use. Value of 'None' will include all shape types.
    shape_types = ['Equilateral', 'IsoscelesRight', 'Square']

    # Convert lattices to geometry figures.
    shape_generator = ShapeGenerator(shape_types)

    # Generate the figures. Returns tuple in the form (list of coordinates, corresponding lattice)
    figures = shape_generator.generate_from_lattice_matrix(lattices, show_figures)
