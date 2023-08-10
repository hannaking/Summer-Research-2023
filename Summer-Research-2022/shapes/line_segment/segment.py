# takes a non-zero number of points and returns lists of 2 points such that they form a line segment
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# side length defaults to 1
# because line segments cannot be edge glued (lattice definition), all line segment will be of default length

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

        # 2 Points in
        # shouldn't happen, because segments cannot be edge glued
        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]
        sorted_points = [b[1] for b in first_sort]

        point1 = sorted_points[0]
        point2 = sorted_points[1]

        # 1 Point in
        if point2 == None:
            # get second point
            point2 = Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

        # we have 1 scenario at 0 degrees: point1 and point2.
        scenarios.append([point1, point2])

        # now we will rotate the one scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
        # creating a new scenario, and add it to the list of scenarios
        # 1 scenario * 9 angles = 9 new scenarios
        # 10 scenarios in total
        # note: we are rotating the points about point 1, because point 1 is either the origin or the vertex the segment is glued to
        angles = [30, 45, 60, 90, 180, -30, -45, -60, -90]
        original_scenario_len = len(scenarios)
        for i in range(original_scenario_len):
            for angle in angles:
                new_scenario = Geometry.rotate(scenarios[i], math.radians(angle))
                scenarios.append(new_scenario)

        # unsort all scenarios to be back in lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 2 Points
        return scenarios
    
    # verify the Points form a valid line segment
    #
    # return False if not 2 Points or if both Points are equal, otherwise True (valid line segment)
    def _verify_line_segment(self):
        if len(self._points) != 2:
            return False

        if (math.isclose(self._points[0].x, self._points[1].x, abs_tol=1e-9) and
            math.isclose(self._points[0].y, self._points[1].y, abs_tol=1e-9)):
            return False
        
        return True 