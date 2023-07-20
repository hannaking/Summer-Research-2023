# fix comments
# currently right kite only

import math

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

ANGLES = [math.radians(-120), math.radians(120), math.radians(-90),math.radians(90),
          math.radians(-90), math.radians(90), math.radians(-60), math.radians(60)]
ANGLES2 = [math.radians(-90), math.radians(90), math.radians(-60),math.radians(60),
          math.radians(-120), math.radians(120), math.radians(-90), math.radians(90)]
DEFAULT_SIDE_LENGTH_SHORT = 1
DEFAULT_SIDE_LENGTH_LONG = math.sqrt(3) * DEFAULT_SIDE_LENGTH_SHORT # from 30-60-90 triangle definition

# _points = a list of Point objects that represent the starting position for the rectangle

#TODO: update for rectangles. you do not need to change anything other than get_second_point, get_third_points, and get_fourth_points.
# change them so that:
# - given 3 points, get the fourth point as whatever side formed between the first and second points (LONG or SHORT)
class Kite(): 

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
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4]]  # list of lists of Points
        # maximum possible scenarios is 80 -> 1 option for first point
        #                                     8 options for second point for every first point
        #                                         first point could be one of 4, so second has 4 options of shape orientation, each has 2 (up/down)
        #                                     1 option for third point for every second point
        #                                     1 option for fourth point for every third point
        #                                     = 10 before rotations
        #                                     * (this + 9 angles) = 80 max scenarios

        # boolean that tells whether this square is vertex glued or not. default to False.
        vertex_gluing = False

        # so third points works if 2 in
        second_points = [pt2, pt2]
        side_short = DEFAULT_SIDE_LENGTH_SHORT
        side_long = DEFAULT_SIDE_LENGTH_LONG

        if pt2 == None:
            # get second point
            second_points = self.get_second_point(pt1)
            # since we only have one point, we know that the rectangle is vertex glued.
            vertex_gluing = True
            # fill the appropriate scenarios
            for i in range(0, len(scenarios)):
                if i < len(scenarios) / 2: scenarios[i][1] = second_points[0]
                else: scenarios[i][1] = second_points[1]

        

        # need to get fourth points before third points :/
        # so, if no third point, get fourth and get third
        # elif no fourth point, get fourth

        # two points in
        if pt3 == None:

            # get fourth point
            # jump-off: point 0
            # ref segment end: point 1
            # angle, length:
            #         -120, short
            #          120, short
            #         -90, long
            #          90, long
            #         -90, short
            #          90, short
            #          60, long
            #         -60, long
            for i in range(len(scenarios)):
                # i know, i'll try to fix it in a second
                # just want to see if this pattern works
                length = side_short if i in [0,1,4,5] else side_long
                scenarios[i][3] = Geometry.calculate_point_from_angle(ANGLES[i], scenarios[i][0], scenarios[i][1], length)

            

            # get third points
            # jump-off: point 3
            # ref segment end: point 0
            # angle, length:
            #         -90, long
            #          90, long
            #         -60, long
            #          60, long
            #         -120, short
            #          120, short
            #         -90, short
            #          90, short
            for i in range(len(scenarios)):
                length = side_short if Geometry.distance(scenarios[i][0], scenarios[i][1]) == side_long else side_long
                scenarios[i][2] = Geometry.calculate_point_from_angle(ANGLES2[i], scenarios[i][3], scenarios[i][0], length)

            
        
        elif pt4 == None:
            # get fourth points
            # same as above
            for i in range(len(scenarios)):
                length = side_short if Geometry.distance(scenarios[i][0], scenarios[i][1]) == side_long else side_long
                scenarios[i][3] = Geometry.calculate_point_from_angle(ANGLES[i], scenarios[i][0], scenarios[i][1], length)


        print(scenarios)
        # get rid of any unused / empty / repeated scenarios
        # necessary?
        scenarios = [x for x in scenarios if None not in x]
        print(scenarios)

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
        return [Point(point1.x + DEFAULT_SIDE_LENGTH_SHORT, point1.y), 
                Point(point1.x + DEFAULT_SIDE_LENGTH_LONG, point1.y)]


