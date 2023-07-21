import math

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

# i decided to use 60 and 120
SMALL_ANGLE = math.radians(60)
LARGE_ANGLE = math.radians(120)
DEFAULT_SIDE_LENGTH = 1
# longer side will be 2 * short from 30-60-90 rules

# _points = a list of Point objects that represent the starting position for the rectangle

#TODO: update for rectangles. you do not need to change anything other than get_second_point, get_third_points, and get_fourth_points.
# change them so that:
# - given 3 points, get the fourth point as whatever side formed between the first and second points (LONG or SHORT)
class IsoTrapezoid(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        # you will start with either one point, two points, or three points.
        #
        # First, we sort the coordinates
        #
        # if you have one point, you will need to find the second point. There is only one option: 1 unit to the right of the start point.
        # We make this decision based on the fact that since we only know the first point, we have no knowledge of the size of the square,
        # so we default to 1 unit. It is to the right because it would look the same whether it was to the left, up, or down, so it does not make
        # much of a meaningful difference.
        #
        # once two points are found, you will need to find the third points (plural!) 
        # If you were given two points to start with, you find the distance between the two. 
        # This is the side length of the square, so you know how far away the third point should be.
        # There are two options: above the second point and below the second point.
        #
        # Once three points are found, you will need to find the fourth points.
        # There is only one option: the final corner of the square.
        # However, you need to repeat the process for each third coordinate.
        # Like before, find the side length by finding the distance between two of the points.
        # Then you'll find the points that are 90 and -90 degrees from the line formed by the third point and the second point.
        # Only one of these coordinates is correct.
        # We find the correct point by creating vectors between the first point and the second point, then the first point and the two possible third points.
        # We check which of the vectors are orthogonal to the vector between the first point and the second point.
        # The one that is orthogonal is the correct point.
        # The one that is not orthogonal is the incorrect point.
        #
        # Once you have the fourth point, you have a complete scenario.
        #
        # For each of these scenarios, we rotate the points about the origin with the angles we care about:
        # [30, 45, 60, 90, 180 ,-30, -45 ,-60 ,-90] degrees (will convert to radians)
        # Each of these is a new scenario.
        # We then unsort these scenarios, then return them.

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        # to make it easier to understand what sorted points are
        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]

        scenarios = [[pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4]]  # list of lists of Points
        # maximum possible scenarios is 80 -> 1 option for first point
        #                                     2 options for second point for every first point
        #                                     2 options for third point for every second point
        #                                     1 option for fourth point for every third point
        #                                     = 4 before rotations
        #                                     * (this + 9 angles) = 40 max scenarios

        # boolean that tells whether this shape is vertex glued or not. default to False.
        vertex_gluing = False

        # so third points works
        second_points = pt2

        if pt2 == None:
            # get second point
            second_points = self.get_second_point(pt1)
            # since we only have one point, we know that the rectangle is vertex glued.
            vertex_gluing = True
            # fill the appropriate scenarios
            for i in range(len(scenarios)):
                scenarios[i][1] = self.get_second_point(pt1)

        if pt3 == None:
            # get third points
            # will be short sides
            # will be 120, -120, 60, and -60
            third_points = []
            third_points = self.get_third_points(pt1, second_points)
            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
        
        if pt4 == None:
            # get fourth points
            angles = [-60, 60, -120, 120]
            for i in range(len(scenarios)):
                scenarios[i][3] = self.get_fourth_points(scenario[0], scenario[1], scenario[2], math.radians(angles[i]))

        # get rid of any unused / empty / repeated scenarios
        # necessary?
        scenarios = [x for x in scenarios if None not in x]

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

        # a list of lists of 4 Points
        return scenarios

    # returns a list of 2  Point objects.
    # if you get here, you are vertex glued. use default side values
    # you need to have this first side be the short side and the long side (so a list)
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # return a list of Point objects. 
    # finds the third points by finding the point 90 degrees and -90 degrees from the line formed by pt 1 and pt 2
    # i need this to be the other of what the first two points are
    #     so, if points one and 2 are a short side, this needs to be a long side and vice versa
    #     how do I know? i don't :/
    #     we decided to use a factor of 2 for the side lengths. so I can return both length first / 2 and first * 2 i think
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []
        # long side = 2 * short side
        third_points.append(Geometry.calculate_point_from_angle(SMALL_ANGLE, point2, point1, side_length / 2))
        third_points.append(Geometry.calculate_point_from_angle(-SMALL_ANGLE, point2, point1, side_length / 2))
        third_points.append(Geometry.calculate_point_from_angle(LARGE_ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-LARGE_ANGLE, point2, point1, side_length))

        return third_points

    # return a Point object. there is 1 option: the final corner of the square.
    # finds the fourth points by finding the point 90 degrees from the line formed by pt 2 and pt 1
    # notice how this is FLIPPED from get_third_points.
    # need the if... negative angle to avoid twists -> be on the right side of the first segment
    # returns None if any input point is None
    def get_fourth_points(self, point1, point2, point3, angle):
        if point1 == None or point2 == None or point3 == None: return None
        side_length = Geometry.distance(point1, point2) / 2 if abs(angle) == math.radians(60) else Geometry.distance(point1, point2)
        return Geometry.calculate_point_from_angle(angle, point1, point2, side_length)

