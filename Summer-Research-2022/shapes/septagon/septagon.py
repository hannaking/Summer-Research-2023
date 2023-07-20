import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *

from geometry import Geometry

ANGLE = math.radians(128 + (4/7))
DEFAULT_SIDE_LENGTH = 1

# 7 sides of equal length, all angles are 128 and 4/7 degrees

class Septagon(): 
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
        vertex_gluing = False
        
        # to make it easier to understand what sorted points are
        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]
        pt5 = sorted_points[4]
        pt6 = sorted_points[5]
        pt7 = sorted_points[6]

        scenarios = [[pt1, pt2, pt3, pt4, pt5, pt6, pt7],
                     [pt1, pt2, pt3, pt4, pt5, pt6, pt7]]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            scenarios[0][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            scenarios[1][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            vertex_gluing = True

        # now have at least 2 points, so side length can be determined
        side_length = Geometry.distance(pt1, scenarios[1][1])

        # then continue to the next
        if  (sorted_points[2] == None): # two known points
            third_points = []
            # 2 possible third points
            third_points.append(Geometry.calculate_point_from_angle(ANGLE, scenarios[1][1], pt1, side_length))
            third_points.append(Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][1], pt1, side_length))
            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
            
        # then continue to the next
        if  (sorted_points[3] == None): # three known points
            # each third point has one possible fourth point
            for i in range(0, len(scenarios)):
                scenarios[i][3] = Geometry.calculate_point_from_angle(ANGLE, scenarios[i][2], scenarios[i][1], side_length)

        # then continue to the next
        if (sorted_points[4] == None): # four known points
            # each fourth point has one possible fifth point
            for i in range(0, len(scenarios)):
                scenarios[i][4] = Geometry.calculate_point_from_angle(ANGLE, scenarios[i][3], scenarios[i][2], side_length)

        # then continue to the next
        if (sorted_points[5] == None): # five known points
            # each fifth point has one possible sixth point
            for i in range(0, len(scenarios)):
                scenarios[i][5] = Geometry.calculate_point_from_angle(ANGLE, scenarios[i][4], scenarios[i][3], side_length)

        # then continue to the next
        if (sorted_points[6] == None): # six known points
            # each fifth point has one possible sixth point
            for i in range(0, len(scenarios)):
                scenarios[i][6] = Geometry.calculate_point_from_angle(ANGLE, scenarios[i][5], scenarios[i][4], side_length)

        # all seven points known handled above

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

        temp = []
        for s in scenarios:
            if s not in temp: temp.append(s)
        scenarios = temp

        # unsort all scenarios
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 7 Points
        return scenarios