import math
import sys

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
        scenarios = [] # list of lists of Points

        # start with anywhere from 1 to 5 points
        # if all Points are given (5 points), just return that one scenario
        if None not in self._points:
            return scenarios.append(self._points)

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        side_length = DEFAULT_SIDE_LENGTH

        second_points = []
        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            second_points.extend(Geometry.get_second_points(sorted_points[0]))
        else: # two known points
            second_points.append(sorted_points[1])
            side_length = Geometry.distance(sorted_points[0], sorted_points[1])

        # now, there is only one possible third point for each second point
        # 108 degrees off
        third_points = []
        for point2 in second_points:
            third_points.extend(Geometry.calculate_point_from_angle(ANGLE, sorted_points[0], point2, side_length))

        # now, there is only one possible fourth point for each third point
        # 108 degrees off
        fourth_points = []
        for i in range(0, len(third_points)):
            fourth_points.extend(Geometry.calculate_point_from_angle(ANGLE, second_points[i], third_points[i], side_length))

        # now, there is only one possible fifth point for each fourth point
        # 108 degrees off
        fifth_points = []
        for i in range(0, len(fourth_points)):
            fifth_points.extend(Geometry.calculate_point_from_angle(ANGLE, third_points[i], fourth_points[i], side_length))

        # now I have...
        # first point -> sorted_points[0]
        # second point -> from list second_points, which has len 10
        # third point -> from list third_points, which has len 10 to match
        # fourth point -> from list fourth_points, which has len 10 to match
        # fifth point -> from list fifth_points, which has len 10 to match

        # build the scenarios
        for i in range(0, len(fifth_points)):
            scenario = []
            scenario.append(sorted_points[0])
            scenario.append(second_points[i])
            scenario.append(third_points[i])
            scenario.append(fourth_points[i])
            scenario.append(fifth_points[i])
            scenarios.append(scenario)

        # unsort all scenarios
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 5 Points
        return scenarios
