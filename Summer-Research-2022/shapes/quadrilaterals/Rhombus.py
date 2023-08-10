# takes a non zero number of points and returns lists of 6 points such that they form a rhombus
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# all sides will be of equal length, defaulting to side length 1
# to differentiate from squares, it has 2 pairs of equal angles (default 80 and 100)

import sys
import math
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry
from vector import Vector

DEFAULT_SIDE_LENGTH = 1
SMALL_ANGLE = math.radians(80)
LARGE_ANGLE = math.radians(100)

class Rhombus(): 

    def __init__(self, known_coords):
        self._points = known_coords

    # get the actual points of each possible valid rhombus
    #
    # returns a list of lists, each containing 4 Points
    # return [] if not 4 Points used in constructor or if the Points provided cannot form a rhombus
    def coordinatize(self):

        scenarios = []

        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]
        sorted_points = [b[1] for b in first_sort]

        # 4 points known
        # checks if the Points given are or are not a valid rhombus
        if None not in sorted_points:
            if(self._verify_rhombi()):
                return [self._points]
            else:
                return []

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]

        # boolean for whether this rhombus is vertex glued or not. default to False.
        vertex_gluing = False

        # 1 Point known
        if point2 == None:
            # get second point
            point2 = self.get_second_point(point1)
            vertex_gluing = True

        # 2 Points known
        if point3 == None:
            # get third points
            third_points = self.get_third_points(point1, point2)
        
        # 3 Points known
        else:
            third_points = [point3]
        
        # we have two scenarios at 0 degrees: above the x axis and below the x axis
        for third_point in third_points:
            if point4 == None:
                # get fourth points
                fourth_point = self.get_fourth_points(point1, point2, third_point)
                scenarios.append([point1, point2, third_point, fourth_point])

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

    # calculates the second point given one point
    #  *second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # return a list of Point objects
    # 2 possible angles (large and small), each positive and negative
    # total = 4 options
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []

        third_points.append(Geometry.calculate_point_from_angle(SMALL_ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-SMALL_ANGLE, point2, point1, side_length))

        third_points.append(Geometry.calculate_point_from_angle(LARGE_ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-LARGE_ANGLE, point2, point1, side_length))

        return third_points

    # return a Point object. there is 1 option: the final corner of the rhombus.
    def get_fourth_points(self, point1, point2, point3):
        side_length = Geometry.distance(point2, point3)
        angle = Geometry.get_angle(point1, point2, point3)
        other_angle = math.copysign(1, angle) * (math.pi - abs(angle))
        fourth_point = []

        fourth_point = Geometry.calculate_point_from_angle(other_angle, point3, point2, side_length)

        return fourth_point

    # verifies that the points form a rhombus
    #
    # returns whether it is a rhombus
    def _verify_rhombus(self):
        return Rhombus.are_rhombi([self._points])

    # determines if the scenarios all form rhombi
    #
    # returns whether all scenarios are rhombi
    @staticmethod
    def are_rhombi(scenarios):
        for scenario in scenarios:
            # 4 spaces
            if len(scenario) != 4:
                return False

            # all points filled
            if None in scenario:
                return False

            point1, point2, point3, point4 = scenario

            sides = [Geometry.distance(point1, point2),
                     Geometry.distance(point2, point3),
                     Geometry.distance(point3, point4),
                     Geometry.distance(point4, point1)]

            # all sides equal
            for side in sides:
                if not math.isclose(sides[0], side):
                    return False
            
            # no overlapped points
            if ((math.isclose(point1.x, point3.x) and math.isclose(point1.y, point3.y)) or 
                (math.isclose(point2.x, point4.x) and math.isclose(point2.y, point4.y))):
                return False

            # Calculate angles
            angle1 = Geometry.get_angle(point1, point2, point3)
            angle2 = Geometry.get_angle(point2, point3, point4)
            angle3 = Geometry.get_angle(point3, point4, point1)
            angle4 = Geometry.get_angle(point4, point1, point2)

            # angle pairs
            if not math.isclose(angle1, angle3) or not math.isclose(angle2, angle4):
                return False
            
            # no flat angles
            for angle in [angle1, angle2, angle3, angle4]:
                if math.isclose(angle, math.radians(180)) or math.isclose(angle, math.radians(0), abs_tol=1e-9):
                    return False

        return True
