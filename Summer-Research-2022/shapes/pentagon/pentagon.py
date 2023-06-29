import math
import sys

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *

from shapes.geometry import Geometry
from shapes.vector import Vector

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

# 5 sides of equal length, all angles are 108 degrees

class Pentagon(): 
    # take a list of 1-5 Points, the unknown Points being None
    # known information about the starting position of the pentagon
    def __init__(self, known_coords):
        self._points = known_coords

    # Get Points to make up the Pentagon
    #
    # returns a list of lists of Points, each list is one coordinatization of the pentagon
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
        # has to be a list for get_next_points
        second_points = sorted_points[1]
        third_points = sorted_points[2]
        fourth_points = sorted_points[3]
        fifth_points = sorted_points[4]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            second_points = []
            # 10 possible second points
            second_points.extend(Geometry.get_second_points([sorted_points[0]]))

        # now have at least 2 points, so side length can be determined
        side_length = Geometry.distance(sorted_points[0], second_points[0])

        # then continue to the next
        if  (sorted_points[2] == None): # two known points
            # this line might be unnecessary?
            side_length = Geometry.distance(sorted_points[0], sorted_points[1])
            third_points = []
            # each second point has 2 possible third points
            # now 20 scenarios
            third_points.extend(self._get_next_points(second_points, sorted_points[0], side_length))
            third_points.extend(self._get_next_points(second_points, sorted_points[0], side_length, 0 - ANGLE))
            
        # then continue to the next
        if  (sorted_points[3] == None): # three known points
            # each third point has one possible fourth point
            fourth_points = []
            fourth_points.extend(self._get_next_points(third_points, second_points, side_length))

        # then continue to the next
        if (sorted_points[4] == None): # four known points
            # each fourth point has one possible fifth point
            fifth_points = []
            fifth_points.extend(self._get_next_points(fourth_points, third_points, side_length))

        # all five points known handled above
        
        # build the scenarios - should total 20 for one in, 2 for 2 in, and 1 for the others
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
    
    # get the next round of points. Pentagons have the same interior angles and side lengths,
    # so getting the next Point is the same for all points (second, third, etc)
    #
    # points - the list of Points for which you want the next Point
    # reference_points - list of Points one step back. so if i'm looking for the 3rd points,
    #                    points is the second points and reference the first
    # length - int, the length of the side of the pentagon
    #
    # returns a list of Points
    def _get_next_points(self, points, reference_points, length = DEFAULT_SIDE_LENGTH, angle = ANGLE):
        new_points = []
        for i in range(0, len(points)):
            new_points.extend(Geometry.calculate_point_from_angle(angle, points[i], reference_points[i], length))
        return new_points