import sys
import math

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from shapes.geometry import Geometry
from lattice import Lattice

ANGLE = math.radians(60)
DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the equilateral triangle

# sides of equal length, all angles are 60 degrees
class Equilateral(): 
    # coming from Triangle (?) based on the lattice (not anymore)
    def __init__(self, known_coords):
        self._points = known_coords
        self._draw_order_indices = []

    def coordinatize(self):
        # you will start with either one or two Points in _points that are not None
        # i need to see which index(es) in the list is/are not None, I can't assume it gois Point None None or Point Point None like I did before
        # then that index in _points is the jumping off point for the rest of the points
        #
        # if you start with one point, you need to get every other point for the possible angles (just do pos and neg angles because I will filter it after)
        # then do the same as you would if you got two points for every second point you got above

        # if you start with two, you have the length of the desired segment and you have only two options for the third point - on one side of the segment or on the other
        # so 60 or -60 degrees from either of the points (doen't matter which) becaue this is an equilateral triangle
        
        # make sure to not overwrite any points
        # each unique group of three points is its own scenario

        # about the Lattice - there is a whole mess about sorting and unsorting the coord list to make it match the lattice in thr factory
        scenarios = []  # list of lists of Points

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        second_points = [] # list of possible second points in the shape - don't necessarily go in the second position of the list

        # I need to sort the coords , dragging along a list of indices.
        # Later, I will sort that list of indices and drag the points along with it, which will unsort the list of Points
        # which i need to be happening so we maintain Point order
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None )]

        # but this does get a sorted points list

        sorted_points = [b[1] for b in first_sort]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            second_points.extend(Geometry.get_second_points(sorted_points[0]))
        else: # two known points
            second_points.append(sorted_points[1])

        # there are two possible third points per second point
        for point in second_points:
            side_length = sorted_points[0].distance(point)
            third_point = Geometry.calculate_point_from_angle(ANGLE, sorted_points[0], point, side_length)

            # unsort
            scenario = [sorted_points[0], point, third_point]
            # print("before unsort",[str(x) for x in scenario])
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            # print("after unsort:",[str(x) for x in scenario])

            scenarios.append(scenario)

        # a list of lists of 3 Points
        return scenarios

    
