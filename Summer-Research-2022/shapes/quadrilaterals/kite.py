# fix comments
# currently right kite only

import math

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.dart import Dart
from geometry import Geometry

ANGLES = [math.radians(-120), math.radians(120), math.radians(-90),math.radians(90),
          math.radians(-90), math.radians(90), math.radians(-60), math.radians(60)]
ANGLES2 = [math.radians(-90), math.radians(90), math.radians(-60),math.radians(60),
          math.radians(-120), math.radians(120), math.radians(-90), math.radians(90)]

DEFAULT_SIDE_LENGTH = 1
DEFAULT_RATIO = 2
ROTATE_ANGLES = [math.radians(30),
                 math.radians(45),
                 math.radians(60),
                 math.radians(90),
                 math.radians(180),
                 math.radians(-30),
                 math.radians(-45),
                 math.radians(-60),
                 math.radians(-90)]

# _points = a list of Point objects that represent the starting position for the rectangle

class Kite(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):

        scenarios = []

        # sorts to be traversible in order
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None)]
        sorted_points = [b[1] for b in first_sort]

        # checks if there are the correct number of points
        if len(sorted_points) != 4:
            return []

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]

        vertex_gluing = False

        scenarios = [[point1, point2, point3, point4]]
            
        # checks if a kite can't be made or if the passed in points are already a kite
        if None not in sorted_points:
            if(self.are_kites(scenarios)):
                return [self._points]
            else:
                return []

        if point2 == None:
            scenarios = self.get_second_point_scenarios(scenarios)
            vertex_gluing = True

        # have 2 points
        if point3 == None:
            for scenario in scenarios:
                next_side_length_a = Geometry.distance(scenario[0], scenario[1]) * 2
                next_side_length_b = Geometry.distance(scenario[0], scenario[1]) / 2




        # makes all of the rotations around point1
        if vertex_gluing == True:
            scenarios = self.get_rotated_scenarios(scenarios)

        # put back in lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        return scenarios

    # gets the scenario that include the second point from the scenario including
    # only the first point.
    #  *second point is placed +1 to the x
    # 
    # scenarios - list of list of one point and three Nones
    # 
    # returns the new scenario
    def get_second_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]

            second_point = self.get_second_point(point1)
            
            new_scenarios.append([point1, second_point, None, None])

        return new_scenarios
    
    # gets the second point given one point
    #  *second point is placed +1 to the x
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)
    
    # gets 10 scenarios rotated around the first point
    #
    # scenarios - the non-rotated scenarios 
    #
    # returns the rotated scenarios
    def get_rotated_scenarios(self, scenarios):
        new_scenarios = scenarios.copy()
        for scenario in scenarios:
            for angle in ROTATE_ANGLES:
                new_scenarios.append(Geometry.rotate(scenario, angle))
        return new_scenarios

    # verify the the points compose a kite
    #
    # returns whether or not it composes a kite
    def _verify_kite(self):
        return Kite.are_kites([self._points])

    # verify the the first 3 points can form a kite
    #
    # returns whether or not it can form a kite
    def _verify_kite_3_points(self):
        p1 = self._points[0]
        p2 = self._points[1]
        p3 = self._points[2]
        return Kite.are_kiteable([[p1, p2, p3, None]])

    # determins if all of the scenarios are posible to create a kite
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 3 points that could form kites
    @staticmethod
    def are_kiteable(scenarios):
        for scenario in scenarios:

            if len(scenario) != 4:
                return False
            
            if (scenario[0] == None or
                scenario[1] == None or
                scenario[2] == None or
                scenario[3] != None):
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]
            
            intersect_point = Dart.find_intersect(point1, point3, point2)
            
            if((math.isclose(intersect_point.x, point1.x, abs_tol=1e-9) and
                math.isclose(intersect_point.y, point1.y, abs_tol=1e-9)) or
               (math.isclose(intersect_point.x, point3.x, abs_tol=1e-9) and
                math.isclose(intersect_point.y, point3.y, abs_tol=1e-9))):
                return False
            
            diagonal = Geometry.distance(point1, point3)
            right = Geometry.distance(point1, intersect_point)
            left = Geometry.distance(intersect_point, point3)
            
            # the intersect must be off of the diagonal or be its midpoint
            if(not math.isclose(right + left, diagonal, abs_tol=1e-9)):
                return False

        return True
    
    # determins if all of the scenarios are posible are a kite
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 4 points that form kites
    @staticmethod
    def are_kites(scenarios):
        for scenario in scenarios:

            if len(scenario) != 4:
                return False
            
            if None in scenario:
                return False
            
            point1, point2, point3, point4 = scenario

            intersect_point1 = Dart.find_intersect(point1, point3, point2)
            intersect_point2 = Dart.find_intersect(point2, point4, point1)
            
            # both intersect points must be the same
            if(not math.isclose(intersect_point1.x, intersect_point2.x, abs_tol=1e-9) or
               not math.isclose(intersect_point1.y, intersect_point2.y, abs_tol=1e-9)):
                return False
            
            diagonal1 = Geometry.distance(point1, point3)
            right1, left1 = Geometry.distance(point1, intersect_point1), Geometry.distance(point3, intersect_point1)
            
            diagonal2 = Geometry.distance(point2, point4)
            right2, left2 = Geometry.distance(point2, intersect_point1), Geometry.distance(point4, intersect_point1)

            # one of the intersect points must be the midpoint its other diagonal
            # and the other must be off of its other diagonal, but not both
            if(not math.isclose(right1+left1, diagonal1, abs_tol=1e-9) or
               not math.isclose(right2+left2, diagonal2, abs_tol=1e-9)):
                return False

        return True
    #------------------------------------------------MATH-----------------------------------------------

    # theta in radians
    def get_long_diag(self, short_side, long_side, theta):
        return math.sqrt(math.pow(long_side, 2) - (math.pow(short_side, 2) * math.pow(math.sin(theta/2)))) + (short_side * math.cos(theta/2))

    def all_angles(self, short_side, long_side, diag):
        return [self.get_a1(short_side, long_side, diag),
                self.get_a2(short_side, long_side, diag),
                self.get_a3(self.get_a1(short_side, long_side, diag), self.get_a2(short_side, long_side, diag))]

    def get_a1(short_side, long_side, diag):
        return 2 * math.acos((math.pow(short_side, 2) + math.pow(diag, 2) - math.pow(long_side, 2)) / 
                         (2 * short_side * diag))

    def get_a2(short_side, long_side, diag):
        return 2 * math.acos((math.pow(long_side, 2) + math.pow(diag, 2) - math.pow(short_side, 2)) / 
                         (2 * long_side * diag))

    def get_a3(self, a1, a2):
        return 180 - (a1/2) - (a2/2)
