import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapes.triangles.triangle_factory              import TriangleFactory
from quadrilaterals.quadrilateral_factory    import QuadrilateralFactory
from pentagon.pentagon_factory               import PentagonFactory
from hexagon.hexagon_factory                 import HexagonFactory
from octagon.octagon_factory                 import OctagonFactory
from septagon.septagon_factory               import SeptagonFactory
from line_segment.segment_factory            import SegmentFactory

#temp
from lattice import Lattice
from shapely.geometry import Point

PLACEHOLDER = "there is no shape with only 2 edges"
SHAPE_TYPES = [SegmentFactory(), PLACEHOLDER, TriangleFactory(), QuadrilateralFactory(), PentagonFactory(), HexagonFactory(), SeptagonFactory(), OctagonFactory()]    

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0


class ShapeFactory:
    """
        the ShapeFactory class is a factory class that coordinatizes the given shape (edge_amount).
        edge_amount is the number of edges the shape has, and is used to determine which specific shape factory class to use (e.g. TriangleFactory if edge_amount == 3).
        once coordinartize() is run, you will have all figures that have every form of the given shape attached to it (according to your known coords) in the form
        of a list of scenarios.

        each scenario is a possible figure (?)

    """
<<<<<<< Updated upstream
    def __init__(self, edge_amount, predetermined_shape_types=['Segment',     # line segment
                                                               'Equilateral', # triangles
                                                               'Isosceles',
                                                               'IsoscelesRight',
                                                               'NonIsoscelesRight',
                                                               'Square',      # quadralaterals
                                                               'Rectangle',
                                                               'Rhombus',
                                                               'Parallelogram',
                                                               'Kite',
                                                               'RightTrapezoid',
                                                               'IsoTrapezoid',
                                                               'Dart',
                                                               'RegularPent', # n-gons
                                                               'RegularHex',
                                                               'RegularHept',
                                                               'RegularOct']):
=======
    def __init__(self, edge_amount, predetermined_shape_types=['Segment', 'Equilateral', 'IsoscelesRight', 'NonIsoscelesRight', 'Square', 'Rectangle', 'Kite', 'IsoTrapezoid', 'RightTrapezoid', 'RegularPent', 'RegularHex', 'RegularSept', 'RegularOct']):
>>>>>>> Stashed changes

        if edge_amount < 1:
            raise ValueError('Shape must have at least 1 edge')

        # Determine which shape types to use.
        shape_types = SHAPE_TYPES
        if predetermined_shape_types is not None:

            shape_types = [None, PLACEHOLDER, None, None, None, None, None, None]

            #TODO pop this stuff out / reduce repeated code?

            # If any triangle types are in the list of predetermined shape types, append to the triangle factory,
            # and use the triangle factory.
            tri_factory = TriangleFactory()
            tri_factory._empty_types()
            for type in predetermined_shape_types:
                
                if tri_factory._include_type(type):
                    shape_types[2] = tri_factory
            
            # If any quadrilateral types are in the list of predetermined shape types, append to the quadrilateral factory,
            # and use the quadrilateral factory.
            quad_factory = QuadrilateralFactory()
            quad_factory._empty_types()
            for type in predetermined_shape_types:

                if quad_factory._include_type(type):
                    shape_types[3] = quad_factory

            # If any pentagon types are in the list of predetermined shape types, append to the pent factory,
            # and use the pent factory.
            pent_factory = PentagonFactory()
            pent_factory._empty_types()
            for type in predetermined_shape_types:
                if pent_factory._include_type(type):
                    shape_types[4] = pent_factory

            # same thing
            hex_factory = HexagonFactory()
            hex_factory._empty_types()
            for type in predetermined_shape_types:
                if hex_factory._include_type(type):
                    shape_types[5] = hex_factory

            sept_factory = SeptagonFactory()
            sept_factory._empty_types()
            for type in predetermined_shape_types:
                if sept_factory._include_type(type):
                    shape_types[6] = sept_factory

            oct_factory = OctagonFactory()
            oct_factory._empty_types()
            for type in predetermined_shape_types:
                if oct_factory._include_type(type):
                    shape_types[7] = oct_factory

        # -1 to shift values to 0-indexed
        self._shape_type_factory = shape_types[edge_amount - 1]

        self._draw_order_indices = []

    """
        param known_coords: an unfinished scenario (list of Points) - unfinished meaning it has Nones in it
        param lattice: the lattice that the figure represents.
        param sl_index: the index of the shape in shape lattice layer.
        returns a list of completed scenarios (there are no Nones in them).
    """
    def coordinatize(self, known_coords, lattice, sl_index):

        # get the indices of the coordinates corresponding to the vertex nodes in the shape of the lattice
        correspondance_indices = [x for x in lattice._get_corresponding_coordinates(sl_index)]
        coords = [known_coords[x] for x in correspondance_indices]

        self._draw_order_indices = self.get_draw_order_indices(coords, correspondance_indices)

        scenarios = self._shape_type_factory._coordinatize(coords)

        for scenario in scenarios:

            if len(scenario) != len(correspondance_indices):
                raise ValueError('Scenario has wrong number of coordinates')

            output = known_coords + []
            for i in range(len(scenario)):
                output[correspondance_indices[i]] = scenario[i]

            yield output

    """
        helper method for coordinatize(). gets draw order indices and returns them.
        param coords: a list of Points that correspond to the vertices of the shape.
        param correspondance_indices: the indices of the coordinates corresponding to the vertex nodes in the shape of the lattice.
        returns draw order indices - the indices of the coordinates corresponding to the vertex nodes in the shape of the lattice IN ORDER they should be drawn.
    """
    def get_draw_order_indices(self, coords, correspondance_indices):
        # first, get how the indices are ordered after they are sorted (according to their values). save to sorted_indices.
        first_sort = [ b for b in sorted(enumerate(coords), key=lambda e: e[1] is None ) ]
        sorted_indices = [b[0] for b in first_sort]

        # unsort correspondance_indices along with sorted_indices.
        # (i got this code from here: https://www.adamsmith.haus/python/answers/how-to-sort-two-lists-together-in-python)
        zipped_lists = zip(sorted_indices, correspondance_indices)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        draw_order_indices = [ list(tuple) for tuple in tuples ]  [1]

        return draw_order_indices