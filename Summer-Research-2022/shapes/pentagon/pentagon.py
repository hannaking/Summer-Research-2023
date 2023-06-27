import math
import sys

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from shapes.geometry import Geometry
from shapes.vector import Vector

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the regular pentagon

# 5 sides of equal length, all angles are 108 degrees

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
        second_points = sorted_points[1]
        third_points = sorted_points[2]
        fourth_points = sorted_points[3]
        fifth_points = sorted_points[4]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            second_points = []
            second_points.extend(Geometry.get_second_points(sorted_points[0]))

        # now have at least 2 points, so side length can be determined
        side_length = Geometry.get_distance(sorted_points[0], sorted_points[1])

        # then continue to the next
        if  (sorted_points[2] == None): # two known points
            third_points = []
            third_points.extend(self.get_next_points(second_points, sorted_points[0], side_length))
            
        # then continue to the next
        if  (sorted_points[3] == None): # three known points
            fourth_points = []
            fourth_points.extend(self.get_next_points(third_points, second_points, side_length))
        # then continue to the next
        if (sorted_points[4] == None): # four known points
            fifth_points = []
            fifth_points.extend(self.get_next_points(fourth_points, third_points, side_length))
        # all five points known handled above
        
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
    
    # reference points are the points one back. so if i'm looking for the 3rd points,
    # points is the second points and reference the first
    def get_next_points(self, points, reference_points, length):
        new_points = []
        for i in range(0, len(points)):
            new_points.extend(Geometry.calculate_point_from_angle(ANGLE, points[i], reference_points[i], length))
        return new_points
