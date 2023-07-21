import math

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *
from geometry import Geometry

DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the equilateral triangle

class Segment: 
    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        scenarios = []  # list of lists of Points

        # shouldn't happen, because segments annot be edge glued
        if None not in self._points: # two points in
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        # Later, I will sort that list of indices and drag the points along with it, which will unsort the list of Points
        # which i need to be happening so we maintain Point order

        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        # to make it easier to understand what sorted points are
        point1 = sorted_points[0]
        point2 = sorted_points[1]

        if point2 == None: # one point in
            # get second point
            point2 = Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

        # we have 1 scenario at 0 degrees: point1 and point2.
        scenarios.append([point1, point2])

        # now we will rotate the one scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
        # creating a new scenario, and add it to the list of scenarios
        # 1 scenario * 9 angles = 9 new scenarios
        # 10 scenarios in total
        # note: we are rotating the points about point 1, because we know that point 1 is either the origin or the vertex the segment is glued to.
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

        # a list of lists of 3 Points
        return scenarios