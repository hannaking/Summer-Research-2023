import math
import copy
import itertools
from re import X
import time
import sys
sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import Point, Polygon
from matplotlib import pyplot as plt
from shapes.shape_factory import ShapeFactory
#from vector import Vector

from lattice import Lattice

#@ temp stuff, delete later
from unit_tests.shape_helpers import ShapeHelpers

SEGMENT = 2
TRIANGLE = 3
QUADRILATERAL = 4
PENTAGON = 5
HEXAGON = 6
SEPTAGON = 7
OCTAGON = 8

TOP_LATTICE_LAYER       = 4
SHAPE_LATTICE_LAYER     = 3
EDGE_LATTICE_LAYER      = 2
VERTEX_LATTICE_LAYER    = 1
BOTTOM_LATTICE_LAYER    = 0

DEFAULT_SIDE_LENGTH = 1

"""
    The ShapeGenerator class is responsible for everything that has to do with putting a lattice on a plane.
    To do this, instantiate a ShapeGenerator, then call generate_by_lattice_traversal(lattice), with lattice being the lattice
    you're generating shapes for.

    generate_by_lattice traversal is the main method of the class. Its algorithm:
    1. populate the draw_order_indices list with Nones for the length of the shape lattice layer
    2. populate the coords list with Nones for the length of the vertex lattice layer
    3. declare an empty list of coordinate_figures, which will be the list of completed scenarios
       and declare your starting shape index (sl_index) to be 0
    4. call the recursive lattice_traversal_helper method, passing coords, coordinate_figures, and sl_index into it.
       this will get you a list of coordinate_figures, which will be the list of completed scenarios
    5. filter out all scenarios that contain overlapping shapes

    lattice_traversal_helper does the rest of the bulk work.
    1. 

    key structures:
    scenario: a list of shapely Point objects. Each Point represents a vertex of a shape and contains the x and y coordinates.

        In a scenario, order matters. Each Point corresponds to a vertex on the vertex lattice layer at the same index.
        For example, imagine we have a triangle:
        vertex lattice layer = [Node1, Node2, Node3]
        scenario = [(0,0), (1,0), (0,1)]
        (0,0) corresponds to Node1, (1,0) corresponds to Node2, (0,1) corresponds to Node3

        look in shape_factory.py for more details on how the corresponding vertices are actually found.

    coordinates: a Point object. When the word "coordinate" is used, it means a point on the graph.
"""
class ShapeGenerator:

    #TODO: Add more shape types
    def __init__(self, shape_types=None):

        self._draw_order_indices = []
        self._shape_types = shape_types
        
#############################################################################################################################

    """
        has_overlap is the method used to filter out scenarios that have overlapping shapes.
        1. First, we chuck out scenarios that have only one shape, because obviously they don't overlap.
           (For some reason, without this check, the scenarios with only one shape will be filtered out.)
        2. We then turn the scenario into a list of shapely Polygon objects, because we need them to use
           shapely methods to check for overlap.
        3. We then loop through every pair of polygons in the scenario, checking if they overlap, returning
           True if they do.
        4. If no overlaps are found, then we return False.
    """
    def has_overlap(self, scenario, lattice): 
        # single shapes were filtering themselves out, but there is no overlap with only one shape
        # so just leave
        if len(lattice._nodes_list[SHAPE_LATTICE_LAYER]) == 1:
            return False

        polygons = self._scenario_to_polygons(scenario, lattice)

        # loop through every pair of polygons in the scenario
        for poly1, poly2 in self.pairwise(polygons):
            # check if they overlap 
            if self.intersects_without_touching(poly1, poly2):
                return True
            
        # check the last poly with the first poly
        if self.intersects_without_touching(polygons[0], polygons[-1]):
            return True

        return False

    # for some reason itertools.pairwise doesn't work so we have to use this (it does the same thing tho)
    """
        Zips two lists together, and returns a list of tuples.
    """
    def pairwise(self, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    """
        Given a scenario, return a list of Polygons that represent each shape in the scenario.
        param scenario: a list of points 
        param lattice: the lattice that the scenario is being generated for
        return: a list of Polygons
    """
    def _scenario_to_polygons(self, scenario, lattice):

        polygons = []
        shape_layer = lattice._nodes_list[SHAPE_LATTICE_LAYER]

        i = 0

        # we stop when the index is has reached the number of shapes in the lattice
        while i < len(shape_layer):
            # we want the points in the order in which you would walk around the perimeter of the shape
            # we have to build the Polygons from in-order Points to avoid "twisting"
            # twisting is when the points in the shape are drawn in the wrong order,
            # making it twist in the middle with an X
            # ex   a rectangle, twisted
            #      A----B
            #       \  /
            #        \/       This has been drawn like A B D C
            #        /\        instead of A B C D so it crosses
            #       /  \
            #      D----C
            draw_order_points = []

            shape_draw_order_indices = self._draw_order_indices[i]
            for index in shape_draw_order_indices:
                # i think this is the other point on the edge?
                corresponding_point = scenario[index]
                draw_order_points.append(corresponding_point)

            # create a polygon from the points
            new_polygon = Polygon(draw_order_points)
            # add it to our list of polygons
            polygons.append(new_polygon)
            i = i + 1

        return polygons

    """
        Given two Polygons, return True if they intersect without touching, False otherwise.

        Our definition of whether something "overlaps" is if it intersects the other polygon and also does not touch it.
        shapely's definition of intersects: Returns True if the boundary or interior of the object intersect in any way with those of the other.
        shapely's definition of touches: Returns True if the objects have at least one point in common and their interiors do not intersect with any part of the other.
        So here, the polygons are not considered to overlap if they are ONLY touching at a vertex or at an edge and nowhere else. 
        They only intersect if the interiors intersect.
        This is how we make sure vertex- and edge-glued shapes are not filtered out!
    """
    def intersects_without_touching(self, polygon1, polygon2): 
        return polygon1.intersects(polygon2) and not polygon1.touches(polygon2)

    """
        The main method of the class.
        1. populate the draw_order_indices list with Nones for the length of the shape lattice layer
        2. populate the coords list with Nones for the length of the vertex lattice layer
        3. declare an empty list of coordinate_figures, which will be the list of completed scenarios
        and declare your starting shape index (sl_index) to be 0
        4. call the recursive lattice_traversal_helper method, passing coords, coordinate_figures, and sl_index into it
        5. filter out all scenarios that contain overlapping shapes out of coordinate_figures
        6. return the coordinate_figures list
    """
    def generate_by_lattice_traversal(self, lattice):
        # list that will hold the indices of the shape's coordinates in the scenario
        # in the order that they should be drawn (i.e. the order in which you would walk around the perimeter of the shape)
        self._draw_order_indices = [None] * len(lattice._nodes_list[SHAPE_LATTICE_LAYER])

        # list with length of lattice vertex node amount, bc each vertex will need coordinates
        # we have to start somewhere, so the first vertex is always the origin
        coords = [Point(0,0)] + [None] * (len(lattice._nodes_list[VERTEX_LATTICE_LAYER]) - 1)

        # pass through the lattice and the initial list of scenarios
        coordinate_figures = []
        sl_index = 0
        
        # call the recursive function
        self.lattice_traversal_helper(lattice, coords, coordinate_figures, sl_index)

        overlapping_scenarios = []
        # loop through each scenario and check if it has any overlapping shapes
        for scenario in coordinate_figures:
            # if we have a None scenario (empty), skip it
            if None in scenario:
                continue

            # keep track of overlapping scenarios by adding them to the list.
            # the reason it doesn't remove the scenarios here is because it had caused
            # problems by missing some overlapping scenarios bc loop
            if self.has_overlap(scenario, lattice):
                overlapping_scenarios.append(scenario)

        # now we can remove the overlapping scenarios from the coordinate_figures list and return
        return [i for i in coordinate_figures if i not in overlapping_scenarios]

    """ 
        The recursive function that does the parsing 

        lattice: the lattice that the shapes are being generated from
        coords: the list of coordinates that have been calculated so far
        coordinate_figures: the list of scenarios that have been found so far
        sl_index: the current index in the shape lattice layer list

        returns: nothing, but adds completed scenarios to the class's coordinate_figures list,
        which will be returned in generate_by_lattice_traversal
        base case: when None is not in coords, we have found all the coordinates for a scenario

        
    """
    def lattice_traversal_helper(self, lattice, coords, coordinate_figures, sl_index):
        # if there are no more empty spots in the list, then all the coordinates have been calculated
        # base case
        if None not in coords and sl_index >= len(lattice._nodes_list[SHAPE_LATTICE_LAYER]):
            coordinate_figures.append(coords)
            return

        shape_node = lattice._nodes_list[SHAPE_LATTICE_LAYER][sl_index]

        # get the number of children of the shape node
        # this is the number of edges that the shape has
        shape_edge_amount = len(shape_node.get_children())

        # creates a shape factory object that will be used to generate the coordinates of the shape
        # passing shape_edge_amount gives ShapeFactory the information needed to pick the correct shape
        shape_factory = ShapeFactory(shape_edge_amount, self._shape_types)

        # Scenarios is a list of lists of coordinates.
        # Each list of coordinates represents one figure.
        #
        # [
        #   [(0,0), None, (1,1)],
        #   [(0,0), None, (0,1)]
        # ]
        new_coords = [x for x in shape_factory.coordinatize( copy.deepcopy(coords), lattice, sl_index )]

        # now that we've coordinatized, shape factory has stored the draw order of the shape (draw order is
        # the same for all scenarios of a shape). we'll append it to our list
        # of draw order indices to use for drawing later.
        self._draw_order_indices[sl_index] = (shape_factory._draw_order_indices)

        # verify that the scenarios are consistent with each other
        self.verify_scenarios(new_coords) #@ debugging purposes

        # for each scenario, call the recursive function
        for coord in new_coords:
            self.lattice_traversal_helper(lattice, coord, coordinate_figures, sl_index + 1)

    """
        param scenarios: list of scenarios
        param lattice: the lattice that the scenarios are being generated from
        displays each scenario onto a coordinate plane, one by one.
    """
    def show(self, scenarios, lattice):
        # for printing purposes
        current_scenario = 0
        total_scenarios = len(scenarios)

        for scenario in scenarios:
            print(scenario)

        # we want to show every scenario, so we will loop through every scenario.
        for scenario in scenarios:

            # default size for a matplotlib figure
            plt.figure(figsize=(8, 8))
            plt.axis('equal')

            # loop through each shape in the lattice
            for i in range(len(lattice._nodes_list[SHAPE_LATTICE_LAYER])):
                # use the draw order indices to get the points that correspond to those indices
                draw_order_points = [scenario[index] for index in self._draw_order_indices[i]]

                x, y = [], []
                # get x and y values from the points
                for point in draw_order_points:
                    x.append(point.x)
                    y.append(point.y)

                # put the shape on the graph
                plt.fill(x, y, alpha=0.5, edgecolor='purple', linewidth=3)

            # now, display the scenario
            current_scenario = current_scenario + 1
            print(" --- showing scenario " + str(current_scenario) + " of " + str(total_scenarios) + " --- ")
            print(scenario)
            plt.show()
            # then we'll loop to the next scenario

    def generate_from_lattice_matrix(self, lattice_matrix, show_scenarios=False):
        """
            Generates scenarios from a lattice matrix.
            lattice_matrix: the lattice matrix that the scenarios will be generated from
        """
        start = time.time()

        coords = []
        for layer in lattice_matrix:
            for lattice, _ in layer:

                figures = self.generate_by_lattice_traversal(lattice)
                coords.extend(figures)

                if show_scenarios:
                    self.show(figures, lattice)

        end = time.time()

        print("-----------------------------------")
        print("Number of figures generated:", len(coords))
        print("-----------------------------------")
        print("Time elapsed:", end - start, "seconds")
        print("-----------------------------------")

    #@ Helper methods for debugging purposes
    #@ These can be deleted once the code is working

    # checks if the scenarios are consistent with each other
    # and that no indices have varying data types
    def verify_scenarios(self, scenarios):

        baseline = scenarios[0]

        for scenario in scenarios:

            for i in range( len( scenario )):

                if scenario[i] is None:
                    if not baseline[i] is None:
            
                        raise Exception("Scenario " + str(scenario) + " has inconsistent data types at index " + str(i))
            
