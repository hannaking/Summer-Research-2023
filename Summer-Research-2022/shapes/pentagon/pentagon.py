import sys
import math
import collections

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from shapes.geometry import Geometry
from shapes.vector import Vector

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the equilateral triangle

# 5 sides of equal length, all angles are 108 degrees
#TODO: unfinished. the Pentagon class must be able to take anywhere between 0-5 points inclusive and generate a valid Pentagon from them.

class Pentagon(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):

        scenarios = []  # list of lists of Points

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        # to make it easier to understand what sorted points are
        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]

        # boolean that tells whether this square is vertex glued or not. default to False.
        vertex_gluing = False

        if point2 == None:
            vertex_gluing = True

        # we have two scenarios at 0 degrees: above the x axis and below the x axis
        scenarios.append([point1, point2, third_points[0], fourth_points[0]])
        scenarios.append([point1, point2, third_points[1], fourth_points[1]])

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            # 2 scenarios * 9 angles = 18 new scenarios
            # 20 scenarios in total
            # note: we are rotating the points about point 1, because we know that point 1 is either the origin or the vertex we are glued to.
            angles = [30, 45, 60, 90, 180, -30, -45, -60, -90]
            original_scenario_len = len(scenarios)
            for i in range(original_scenario_len):
                for angle in angles:
                    new_scenario = Geometry.rotate(scenarios[i], math.radians(angle))
                    scenarios.append(new_scenario)

        # unsort all scenarios
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 4 Points
        return scenarios

    # returns a Point object. there is only one option: 1 unit to the right of the start point.
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    def get_all_points(self, existing_points, side_length):
        pass
