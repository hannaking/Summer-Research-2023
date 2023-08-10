# takes a non zero number of points and returns lists of 4 points such that they form rectangles 
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# all sides will be of equal length, defaulting to side length 1
# default side ratio is 1:2
# all interior angles are 90 degrees

import sys
import math
import os
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry
from vector import Vector

ANGLE = math.radians(90)
DEFAULT_SIDE_LENGTH_SHORT = 1
DEFAULT_SIDE_LENGTH_LONG = 2

# _points = a list of Point objects that represent the starting position for the rectangle

class Rectangle(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        scenarios = []

        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]
        sorted_points = [b[1] for b in first_sort]

        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]

        # 4 Points known
        # checks if the Points given are or are not a valid rectangle
        if None not in sorted_points:
            if(self._verify_rectangle()):
                return [self._points]
            else:
                return []

        scenarios = [[pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4]]  # list of lists of Points
        # maximum possible scenarios is 80 -> 1 option for first point
        #                                     2 options for second point for every first point
        #                                     4 options for third point for every second point
        #                                     1 option for fourth point for every third point
        #                                     = 8 before rotations
        #                                     * (this + 9 angles) = 80 max scenarios

        vertex_gluing = False

        # so third points works if 2 in
        second_points = [pt2, pt2]
        
        # 1 Point known
        if pt2 == None:
            # get second point
            second_points = self.get_second_point(pt1)
            vertex_gluing = True

            # fill the appropriate scenarios
            for i in range(0, len(scenarios)):
                if i < len(scenarios) / 2: scenarios[i][1] = second_points[0]
                else: scenarios[i][1] = second_points[1]

        # 2 Points known
        if pt3 == None:
            third_points = []
            third_points = self.get_third_points(pt1, second_points[0])
            third_points.extend(self.get_third_points(pt1, second_points[1]))
            
            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
        
        # 3 Points known
        if pt4 == None:
            if(pt3 != None and not self._verify_rectangle_3_points()):
                return []
            # get fourth points
            for scenario in scenarios:
                scenario[3] = self.get_fourth_points(scenario[0], scenario[1], scenario[2])

        # get rid of any unused / empty / repeated scenarios
        # necessary?
        scenarios = [x for x in scenarios if None not in x]

        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            angles = [30, 45, 60, 90, 180, -30, -45, -60, -90]
            original_scenario_len = len(scenarios)
            for i in range(original_scenario_len):
                for angle in angles:
                    new_scenario = Geometry.rotate(scenarios[i], math.radians(angle))
                    scenarios.append(new_scenario)

        # unsort all scenarios to lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 4 Points
        return scenarios

    # returns a list of 2 Point objects
    #
    # point1 - 2d Point
    #
    # vertex glued. use default side values
    # this first side is the short side and the long side
    def get_second_point(self, point1):
        return [Point(point1.x + DEFAULT_SIDE_LENGTH_SHORT, point1.y), 
                Point(point1.x + DEFAULT_SIDE_LENGTH_LONG, point1.y)]

    # 
    # point1 - 2d Point
    # point2 - 2d Point
    #
    # return a list of Point objects. 
    # finds the third points by finding the point 90 degrees and -90 degrees from the line formed by pt 1 and pt 2
    # if points one and 2 are a short side, this needs to be a long side and vice versa
    # decided to use a factor of 2 for the side lengths. so I can return both length first / 2 and first * 2
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []
        # this is the long side
        third_points.append(Geometry.calculate_point_from_angle(ANGLE, point2, point1, side_length * 2))
        third_points.append(Geometry.calculate_point_from_angle(ANGLE, point2, point1, side_length / 2))
        # this is the short side
        third_points.append(Geometry.calculate_point_from_angle(-ANGLE, point2, point1, side_length * 2))
        third_points.append(Geometry.calculate_point_from_angle(-ANGLE, point2, point1, side_length / 2))

        return third_points

    # point1, point2, point3 - 2d Point 
    #
    # return a Point object
    # 
    # 1 option: the final corner of the rectangle.
    # finds the fourth points by finding the point 90 degrees from the line formed by pt 2 and pt 1
    #
    # need the if... negative angle to avoid twists -> be on the right side of the first segment
    #
    # returns None if any input point is None
    def get_fourth_points(self, point1, point2, point3):
        if point1 == None or point2 == None or point3 == None: return None
        side_length = Geometry.distance(point2, point3)
        if (point3.x, point3.y) < (point2.x, point2.y): return Geometry.calculate_point_from_angle(-ANGLE, point1, point2, side_length)
        return Geometry.calculate_point_from_angle(ANGLE, point1, point2, side_length)
    
    # verifies if the points forms a rectangle
    #
    # returns if Points given on construction are a rectangle
    def _verify_rectangle(self):
        return Rectangle.are_rectangles([self._points])

    # finds if the scenarios are rectangles
    #
    # returns whether all scenarios are rectangles
    @staticmethod
    def are_rectangles(scenarios):
        for scenario in scenarios:
            # 4 spaces in scenario list
            if len(scenario) != 4:
                return False

            # all 4 Points filled
            if None in scenario:
                return False

            point1, point2, point3, point4 = scenario

            side1 = Geometry.distance(point1, point2)
            side2 = Geometry.distance(point2, point3)
            side3 = Geometry.distance(point3, point4)
            side4 = Geometry.distance(point4, point1)

            diagonal1 = Geometry.distance(point1, point3)
            diagonal2 = Geometry.distance(point2, point4)

            # 2 pairs of equal sides
            if (not math.isclose(side1, side3) or
                not math.isclose(side2, side4) or
                not math.isclose(diagonal1, diagonal2)):
                return False

        return True

    # verifies if the points are 3 points that could form a rectangle
    #
    # returns if 3 of the Points given on construction could form a rectangle
    def _verify_rectangle_3_points(self):
        return Rectangle.are_rectangleable([self._points])

    # finds if the scenarios can form rectangles
    #
    # returns whether they are rectangleable
    @staticmethod
    def are_rectangleable(scenarios):
        for scenario in scenarios:
            # 4 spaces in scenario list
            if len(scenario) != 4:
                    return False
            
            # points in order
            if(scenario[0] == None or
               scenario[1] == None or
               scenario[2] == None or
               scenario[3] != None):
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]
            
            angle = abs(Geometry.get_angle(point1, point2, point3))

            # 90 degree angle
            if not math.isclose(angle, math.pi / 2, abs_tol=1e-9):
                return False
            
        return True