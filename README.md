
# Lattice-Based Generation of Geometry Figures​

Lattice-Based Generation of Geometry Figures is a program that allows users to inputs desired shapes and quantities.  The program will then output textbook-like figures that contain the shapes in the quantities.

## Requirements

I'm not quite sure yet

## Usage

```python
from lattice_generator import LatticeGenerator
from face_graphs.face_graph_generator import FaceGraphGenerator
from shapes.shape_generator import ShapeGenerator
from textbook_identifier import TextbookIdentifier

# Create input shape list
#                  [Segments, Triangles, Quads, Pentagons, Hexagons, Septagons, Octagons]
input_shape_list = [0,         2,        0,      0,        0,        0,         0       ]

# Initialize the lattice generator.
lattice_generator = LatticeGenerator(input_shape_list)

# Generate the lattices.
lattices = lattice_generator.glue_shapes()._lattice_matrix

# Removes the partial figure lattices and unnecessary detail.
lattices_final = lattice_generator.constrain_to_final(lattices, sum(input_shape_list))

# Generates the associated dual graphs for each lattice.
dual_graphs = FaceGraphGenerator.from_lattices(lattices_final)

# Reduces the lattices and graphs to only those the model considers to be textbook-like.
key = TextbookIdentifier.identify(dual_graphs, "model__1")
lattices_final, dual_graphs = TextbookIdentifier.get_only_in_textbook(lattices_final, dual_graphs, key)

# determines whether or not the individual figures are displayed
show_figures  = False

# chooses the specific shapes that will appear in the generated figures
# options: 'Segment',   'Equilateral', 'Isosceles',     'IsoscelesRight', 'NonIsoscelesRight', 'Square',
#          'Rectangle', 'Rhombus',     'Parallelogram', 'Kite',           'RightTrapezoid',    'IsoTrapezoid',
#          'Dart',      'RegularPent', 'RegularHex',    'RegularSept',    'RegularOct'
shape_types = ['Isosceles', 'NonIsoscelesRight']

# Convert lattices to geometry figures.
# not including the shape_types allows all shapes
shape_generator = ShapeGenerator(shape_types)

# puts the figures on the plane and removes overlapping figures
shape_generator.generate_from_dual_lattice_pairs(final_lattices, dual_graphs, show_figures)
```

### sample output

```
-----------------------------------
Number of figures generated: 37060
-----------------------------------
Time elapsed: 727.6770117282867 seconds
-----------------------------------
```