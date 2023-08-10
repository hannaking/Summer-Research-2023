# takes a non zero number of points and returns lists of 4 points such that they form isosceles trapezoids
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# 3 sides will be of equal length (adheres to definition of isosceles but makes it easier to graph)
# angles are 120-60-60-120 so 30-60-90 rules can be applied
#          x
#      *-------*
#  x  /60       \  x
#    /        120\
#   *-------------*
#          2x          <- from 30-60-90 rules

# based on rectangle code

import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

# decided to use 60 and 120
SMALL_ANGLE = math.radians(60)
LARGE_ANGLE = math.radians(120)
DEFAULT_SIDE_LENGTH = 1
# longer side will be 2 * short from 30-60-90 rules

# _points = a list of Point objects that represent the starting position for the isotrapezoid

class IsoTrapezoid(): 

    def __init__(self, known_coords):
        self._points = known_coords

    # get the actual points of each possible valid iso trapezoid
    #
    # returns a list of lists, each containing 4 Points
    # return [] if not 4 Points used in constructor or if the Points provided cannot form an iso trapezoid
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

        # checks if there are the correct number of points
        if len(sorted_points) != 4:
            return []

        # 4 Points in
        # checks if the Points given are or are not a valid iso trapezoid
        if None not in sorted_points:
            if(self._verify_isotrapezoid()):
                return [self._points]
            else:
                return []

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

        # boolean for whether this shape is vertex glued or not. default to False.
        vertex_gluing = False

        # so third points works
        second_points = pt2

        # 1 Point known
        if pt2 == None:
            second_points = self.get_second_point(pt1)
            vertex_gluing = True

            # fill the appropriate scenarios
            for i in range(len(scenarios)):
                scenarios[i][1] = self.get_second_point(pt1)

        # 2 Points known
        if pt3 == None:
            # will be short sides
            # will be 120, -120, 60, and -60
            third_points = []
            third_points = self.get_third_points(pt1, second_points)
            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
        
        # 3 Points known
        if pt4 == None:
            if(pt3 != None and not self._verify_isotrapezoid_3_points()):
                return []
            
            # get fourth points
            angles = [-60, 60, -120, 120]
            for i in range(len(scenarios)):
                scenarios[i][3] = self.get_fourth_points(scenarios[i][0], scenarios[i][1], scenarios[i][2], math.radians(angles[i]))

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

    # calculates the second point given one point
    #  *second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # first 2 points for a segment that is both a duplicated side and the base
    # third point forms both a duplicated side and the base
    # side length ratio is 1:2 
    #
    # point1, point2 - 2d Points
    #
    # return a list of Point objects
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []

        third_points.append(Geometry.calculate_point_from_angle(SMALL_ANGLE, point2, point1, side_length / 2))
        third_points.append(Geometry.calculate_point_from_angle(-SMALL_ANGLE, point2, point1, side_length / 2))
        third_points.append(Geometry.calculate_point_from_angle(LARGE_ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-LARGE_ANGLE, point2, point1, side_length))

        return third_points

    # one possible fourth point
    #
    # point1, point2, point3 - 2d Point
    # angle - float, angle to be used in contructing the final segment
    # 
    # return a Point object, None if any point passed in is None
    def get_fourth_points(self, point1, point2, point3, angle):
        if point1 == None or point2 == None or point3 == None: return None
        side_length = Geometry.distance(point1, point2) / 2 if abs(angle) == math.radians(60) else Geometry.distance(point1, point2)
        return Geometry.calculate_point_from_angle(angle, point1, point2, side_length)

    # verifies that the points are an isoscles trapezoid
    #
    # returns whether Points from construction are an isosceles trapezoid
    def _verify_isotrapezoid(self):
        return IsoTrapezoid.are_isotrapezoids([self._points])

    # finds if the scenarios are isosceles trapezoids
    #
    # scenarios - list of lists of points
    #
    # returns True if 4 Points with 2 pairs of matching angles, otherwise False
    @staticmethod
    def are_isotrapezoids(scenarios):
        for scenario in scenarios:
            # 4 spaces in the scenario list
            if len(scenario) != 4:
                return False

            # no point is None
            if None in scenario:
                return False

            point1, point2, point3, point4 = scenario

            angle1 = Geometry.get_angle(point1, point2, point3)
            angle2 = Geometry.get_angle(point2, point3, point4)
            angle3 = Geometry.get_angle(point3, point4, point1)
            angle4 = Geometry.get_angle(point4, point1, point2)

            # 2 pairs of matching angles
            if (not((math.isclose(angle1, angle2) and math.isclose(angle3, angle4)) or 
                    (math.isclose(angle1, angle4) and math.isclose(angle2, angle3)))):
                return False
        
        return True

    # verifies whether the points are 3 points that could form an isosceles trapezoid
    #
    # returns whether Points used in construction could form an iso trapezoid
    def _verify_isotrapezoid_3_points(self):
        return IsoTrapezoid.are_isotrapezoidable([self._points])

    # gets whether the scenarios could form an isosceles trapezoid
    #
    # returns True if all scenarios could form an isosceles trapezoid
    @staticmethod
    def are_isotrapezoidable(scenarios):
        for scenario in scenarios:
            # 4 spaces in scenario
            if len(scenario) != 4:
                    return False
            
            # order
            if(scenario[0] == None or
               scenario[1] == None or
               scenario[2] == None or
               scenario[3] != None):
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]
            
            angle = abs(Geometry.get_angle(point1, point2, point3))

            # existing angle is not flat
            if math.isclose(angle, 0, abs_tol=1e-9) or math.isclose(angle, math.pi, abs_tol=1e-9):
                return False
            
        return True