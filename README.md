# Lattice-Based Generation of Geometry Figures​

---

Lattice-Based Generation of Geometry Figures is a program that allows users to inputs desired shapes and quantities.  The program will then output textbook-like figures that contain the shapes in the quantities.

## Requirements

---

I'm not quite sure yet

## Usage

---

```python
from lattice_generator import LatticeGenerator
from face_graphs.face_graph_generator import FaceGraphGenerator
from shapes.shape_generator import ShapeGenerator
from textbook_identifier import TextbookIdentifier

show_figures  = True

# Create input shape list
#                  [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]
input_shape_list = [0,         2,        0,      0,        0,        0,         0       ]

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

shape_types = ['IsoTriangle', 'RightTriangle']

# Convert lattices to geometry figures.
shape_generator = ShapeGenerator(shape_types)

generate_from_dual_lattice_pairs(final_lattices, dual_graphs, show_figures)
```