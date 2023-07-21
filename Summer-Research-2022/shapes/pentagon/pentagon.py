import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *

from geometry import Geometry

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
            print("five known point")
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        side_length = DEFAULT_SIDE_LENGTH
        vertex_gluing = False
        
        over_half = True if sum(_ is not None for _ in self._points) > len(self._points) / 2 else False
        # add stuff here so it leaves if angle formed by over_half pointsis not 108
        
        # to make it easier to understand what sorted points are
        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]
        pt5 = sorted_points[4]

        # pre-rotate, there is only 2 options
        # third point down or third point up
        scenarios = [[pt1, pt2, pt3, pt4, pt5],
                     [pt1, pt2, pt3, pt4, pt5]]
        print(scenarios)

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            print("one known point")
            scenarios[0][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            scenarios[1][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            vertex_gluing = True

        # now have at least 2 points, so side length can be determined
        side_length = Geometry.distance(pt1, scenarios[1][1])

        # then continue to the next
        if  (sorted_points[2] == None): # two known points
            print("two known point")
            # 2 possible third points
            scenarios[0][2] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][1], pt1, side_length)
            scenarios[1][2] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][1], pt1, side_length)

        # then continue to the next
        if  (sorted_points[3] == None): # three known points
            print("three known point")
            # each third point has one possible fourth point
            scenarios[0][3] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][2], scenarios[0][1], side_length)
            scenarios[1][3] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][2], scenarios[1][1], side_length)


        # then continue to the next
        if (sorted_points[4] == None): # four known points
            print("four known point")
            # each fourth point has one possible fifth point
            scenarios[0][4] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][3], scenarios[0][2], side_length)
            scenarios[1][4] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][3], scenarios[1][2], side_length)

        # all five points known handled above

        if over_half:
            scenarios = [scenarios[0]] if Geometry.calculate_point_from_angle(ANGLE, scenarios[0][4], scenarios[0][3], side_length) == scenarios[0][0] else [scenarios[1]]

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            # 8 scenarios * 9 angles = 72 new scenarios
            # 80 scenarios in total
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

        # a list of lists of 5 Points
        return scenarios