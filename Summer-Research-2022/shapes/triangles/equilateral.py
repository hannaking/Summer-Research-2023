# takes a non zero number of points and returns lists of 3 points such that they form equilateral triangles 
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# all sides will be of equal length, defaulting to side length 1
# all interior angles are 60 degrees
#        /\
#       /60\
#   x  /    \  x
#     /60  60\
#    '--------'
#         x

import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *
from geometry import Geometry

ANGLE = math.radians(60)
DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the equilateral triangle

class Equilateral(): 
    def __init__(self, known_coords):
        self._points = known_coords
        self._draw_order_indices = []

    def coordinatize(self):
        # you will start with either one or two Points in _points that are not None
        #
        # if you start with one point, you need to get every second point for the possible rotation angles
        # use the default side length (1 unit)
        # then do the same as you would if you got two points for every second point you got above
        #
        # if you start with two, you have the length of the desired segment and you have only two options for the third point - on one side of the segment or on the other
        # so 60 or -60 degrees from either of the points (doesn't matter which) becaue this is an equilateral triangle, with interior angles of 60

        scenarios = []
        second_points = []

        # sort the coords , dragging along a list of indices
        # Later, sort that list of indices and drag the points along with it, which will unsort the list of Points
        # maintains Point order in the lattice which is needed in generator
        #
        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None )]
        sorted_points = [b[1] for b in first_sort]

        # 3 Points known
        # checks if the Points given are or are not a valid equilateral triangle
        if None not in sorted_points:
            if(self._verify_equilateral_triangle()):
                return [self._points]
            else:
                return []

        # 1 Point known
        # get all possible next point for the given single point
        # includes all rotations
        if (sorted_points[1] == None): # one known point
            second_points.extend(Geometry.get_second_points(sorted_points[0]))
        else:
            second_points.append(sorted_points[1])

        # 2 Points known
        # there are two possible third points per second point
        # third point 1:
        #   1----2
        #         \
        #          3     positive angle
        # third point 2:
        #          3     negative angle
        #         /
        #   1----2
        for point in second_points:
            side_length = sorted_points[0].distance(point)
            third_point = Geometry.calculate_point_from_angle(ANGLE, sorted_points[0], point, side_length)

            # build the scenario and unsort
            scenario = [sorted_points[0], point, third_point]
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]

            scenarios.append(scenario)

        # a list of lists of 3 Points
        return scenarios

    # verifies the points form an equilateral triangle
    #
    # returns True if 3 equilateral sides, otherwise False
    def _verify_equilateral_triangle(self):
        if len(self._points) != 3:
            return False

        # Calculate the lengths of the three sides of the triangle
        side1 = Geometry.distance(self._points[0], self._points[1])
        side2 = Geometry.distance(self._points[1], self._points[2])
        side3 = Geometry.distance(self._points[2], self._points[0])
        
        # Check if it's equilateral
        if not math.isclose(side1, side2) or not math.isclose(side2, side3):
            return False

        return True