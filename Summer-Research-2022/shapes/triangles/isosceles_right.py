# takes a non zero number of points and returns lists of 3 points such that they form isosceles right triangles
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# the first side is both the base and a side and will be length 1 unless it is an edge glue to something with a different length
#
# 45 45 90 triangle rules
#        /\
#       /90\
#   x  /    \  x
#     /45  45\
#    '--------'
#     x*sqrt(2)

import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *
from geometry import Geometry

DEFAULT_SIDE_LENGTH = 1

# sides of equal length, all angles are 60 degrees
class IsoscelesRight(): 
    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):

        scenarios = []

        # sort the coords , dragging along a list of indices
        # Later, sort that list of indices and drag the points along with it, which will unsort the list of Points
        # maintains Point order in the lattice which is needed in generator
        #
        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]
        sorted_points = [b[1] for b in first_sort]

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]

        # 3 Points known
        # checks if the Points given are or are not a valid isosceles right triangle
        if None not in sorted_points:
            if(self._verify_isosceles_triangle()):
                return [self._points]
            else:
                return []

        # boolean for whether this triangle is vertex glued or not. default to False.
        vertex_gluing = False

        # 1 Point known
        if point2 == None:
            # get second point
            point2 = self.get_second_point(point1)
            vertex_gluing = True

        # 2 Points known
        if point3 == None:
            third_points = self.get_third_points(point1, point2)
        # 4 options for third point: 90 degrees above and below the x axis, and 45 degrees above and below the x axis
        for i in range(len(third_points)):
            scenarios.append([point1, point2, third_points[i]])

        # you would only ever want to rotate your shape if you are vertex glued or the first shape on the board
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
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

    # calculates the second point given one point
    #  *second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # given 2 points that form one segment
    # that segment is both the base and an isosceles side (2 options)
    #      (no need for it to be an isosceles side twice because an iso right tri has symmetry down the center)
    # for each of those cases, the next point must be above and below the existing segment (2 options per)
    # Cases:
    # 1. Given base, positive angle
    #      1-------2
    #             /
    #            / <- side, length is given/sqrt(2), angle is 45
    #           /
    #          3
    # 2. Given base, negative angle
    #          3
    #           \
    #            \  <- side, length is given/sqrt(2), angle is -45
    #             \
    #      1-------2
    # 3. Given side, positive angle                (I can't draw these) (angle is +/- 90)
    # 4. Given side, negative angle     (the next side is the other side and it has the same length)
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []
        third_points.append(Geometry.calculate_point_from_angle(math.radians(90), point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(-90), point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(45), point2, point1, side_length * math.sqrt(2)))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(-45), point2, point1, side_length * math.sqrt(2)))

        return third_points
    
    # verifies the points form an isosceles right triangle
    #
    # return True if there are three points, one right angle, and two matching sides
    # return False otherwise
    def _verify_isosceles_triangle(self):
        if len(self._points) != 3:
            return False

        # Calculate the lengths of the three sides of the triangle
        side1 = Geometry.distance(self._points[0], self._points[1])
        side2 = Geometry.distance(self._points[1], self._points[2])
        side3 = Geometry.distance(self._points[2], self._points[0])

        # Check if it's an isosceles triangle
        if math.isclose(side1, side2) or math.isclose(side2, side3) or math.isclose(side3, side1):
            # Check if it's a right triangle
            if math.isclose(side1**2 + side2**2, side3**2) or math.isclose(side2**2 + side3**2, side1**2) or math.isclose(side3**2 + side1**2, side2**2):
                return True

        return False