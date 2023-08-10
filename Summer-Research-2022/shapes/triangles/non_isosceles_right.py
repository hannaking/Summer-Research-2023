# takes a non zero number of points and returns lists of 3 points such that they form non-isosceles right triangles
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# the first side is both the base and a side and will be length 1 unless it is an edge glue to something with a different length
#
# 30 60 90 triangle rules
#             .  <- 30
#             |\
#  x*sqrt(3)  | \ 2x
#             |  \   <-60
#        90-> '---'
#               x

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import math

from shapely.geometry import *
from geometry import Geometry

DEFAULT_SIDE_LENGTH = 1

class NonIsoscelesRight(): 
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
        # checks if the Points given are or are not a valid right triangle
        if None not in sorted_points:
            if(self._verify_right_triangle()):
                return [self._points]
            else:
                return []

        vertex_gluing = False

        # 1 Point knwn
        if point2 == None:
            # get second point
            point2 = self.get_second_point(point1)
            vertex_gluing = True

        # 2 Points known
        if point3 == None:
            # 6 scenarios at 0 degrees: 30, 60, and 90 degrees each above and below the x axis
            third_points = self.get_third_points(point1, point2)
        for i in range(len(third_points)):
            scenarios.append([point1, point2, third_points[i]])

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

    # given 2 Points that form one segment of the triangle
    # is the base, hypotenuse, and leg of the triangle
    # the next side will be the...
    # 1. given hypotenuse, 30      leg
    # 2. given hypotenuse, -30     leg
    # 3. given base, 60            hypotenuse
    # 4. given base, -60           hypotenuse
    # 5. given leg, 90             base
    # 6. given leg, -90            base
    #
    # return a list of 6 Point objects. there are six options: 30, -30, 60, -60, 90, -90 degrees.
    # when each point is calculated, side_length is used to find what the length of the new side should be according to the proportions of
    # a 30-60-90 non-isosceles right triangle.
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []

        third_points.append(Geometry.calculate_point_from_angle(math.radians(30), point2, point1, side_length * (2/math.sqrt(3))))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(-30), point2, point1, side_length * (2/math.sqrt(3))))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(60), point2, point1, side_length * 2))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(-60), point2, point1, side_length * 2))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(90), point2, point1, side_length * math.sqrt(3)))
        third_points.append(Geometry.calculate_point_from_angle(math.radians(-90), point2, point1, side_length * math.sqrt(3)))

        return third_points

    # verifies the points form a right triangle
    #
    # returns True if 3 Points and right (using pythagorean theorum)
    def _verify_right_triangle(self):
        if len(self._points) != 3:
            return False

        # Calculate the lengths of the three sides of the triangle
        side1 = Geometry.distance(self._points[0], self._points[1])
        side2 = Geometry.distance(self._points[1], self._points[2])
        side3 = Geometry.distance(self._points[2], self._points[0])

        # Check if it's a right triangle
        if math.isclose(side1**2 + side2**2, side3**2) or math.isclose(side2**2 + side3**2, side1**2) or math.isclose(side3**2 + side1**2, side2**2):
            return True

        return False