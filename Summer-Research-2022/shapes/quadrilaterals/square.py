import sys
import math
import collections
import numpy as np

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from geometry import Geometry
from vector import Vector

ANGLE = math.radians(90)
DEFAULT_SIDE_LENGTH = 1
ROTATE_ANGLES = [math.radians(30),
                 math.radians(45),
                 math.radians(60),
                 math.radians(90),
                 math.radians(180),
                 math.radians(-30),
                 math.radians(-45),
                 math.radians(-60),
                 math.radians(-90)]

# _points = a list of Point objects that represent the starting position for the equilateral triangle

# 4 sides of equal length, all angles are 90 degrees
class Square(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        scenarios = []

        # sorts to be traversible in order
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None)]
        sorted_points = [b[1] for b in first_sort]

        # checks if there are the correct number of points
        if len(sorted_points) != 5:
            return []

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]

        vertex_gluing = False

        scenarios = [[point1, point2, point3, point4]]
            
        # 4 points in
        # checks if a square can't be made or if the passed in points are already a square
        if None not in sorted_points:
            if(self._verify_square()):
                return [self._points]
            else:
                return []

        if point2 == None:
            scenarios[0][1] = self.get_second_point(point1)
            vertex_gluing = True
        
        if point3 == None:
            scenarios = self.get_third_points(scenarios[0][0], scenarios[0][1])
            # now scenarios has len 2
        else:
            # checks if the known n points can even form a square
            if(not self._verify_square_3_points()):
                return []

        if point4 == None:            
            scenarios = self.get_next_point_scenarios(scenarios, 3)

        # makes all of the rotations around point1
        if vertex_gluing == True:
            scenarios = self.get_rotated_scenarios(scenarios)

        # put back in lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        return scenarios
    
    # returns a Point object. there is only one option: 1 unit to the right of the start point.
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # gets the scenarios that include the third points from the scenario including
    # only the first point and the second point.
    # 
    # scenarios - list of list of one point and three Nones
    # 
    # returns the new scenario
    def get_third_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]
            point2 = scenario[1]

            third_points = self.get_third_points(point1, point2)
            
            for third_point in third_points:
                new_scenarios.append([point1, point2, third_point, None])

        return new_scenarios
    
    # gets the third points given two points
    #
    # point1 - 2d point
    # point2 - 2d point
    #
    # returns the third and fourth points
    def get_third_points(self, point1, point2):
        third_points = []
        side_length = Geometry.distance(point1, point2)

        third_points.append(Geometry.calculate_point_from_angle(ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-ANGLE, point2, point1, side_length))
        
        return third_points

    # gets the scenarios that include the next points from the scenarios including
    # 
    # scenarios - list of list of one point and three Nones
    # place - int, the index of the new point
    # 
    # returns the new scenario
    def get_next_point_scenarios(self, scenarios, place):
        new_scenarios = []
        for scenario in scenarios:
            point_prev3 = scenario[place - 3]
            point_prev2 = scenario[place - 2]
            point_prev1 = scenario[place - 1]

            new_point = self.get_next_point(point_prev3, point_prev2, point_prev1)
            
            new_scenario = []
            for i, point in enumerate(scenario):
                if i == place:
                    new_scenario.append(new_point)
                else:
                    new_scenario.append(point)
            new_scenarios.append(new_scenario.copy())
        
        return new_scenarios

    # gets the next point given the prior three points
    #
    # point_prev3 - 2d point | point before the point before the prior point
    # point_prev2 - 2d point | point before the prior point
    # point_prev1 - 2d point | prior point
    #
    # returns the fourth point
    def get_next_point(self, point_prev3, point_prev2, point_prev1):
        side_length = Geometry.distance(point_prev3, point_prev2)

        angle = Geometry.get_angle(point_prev3, point_prev2, point_prev1)

        next_point = Geometry.calculate_point_from_angle(angle, point_prev1, point_prev2, side_length)

        return next_point

    def _verify_square_3_points(self):
        if len(self._points) != 4:
                return False
            
        if(self._points[0] == None or
           self._points[1] == None or
           self._points[2] == None or
           self._points[3] != None):
            return False

        point1 = self._points[0]
        point2 = self._points[1]
        point3 = self._points[2]

        side1 = Geometry.distance(point1, point2)
        side2 = Geometry.distance(point2, point3)
            
        angle = abs(Geometry.get_angle(point1, point2, point3))

        if not math.isclose(abs(angle), math.pi / 2, abs_tol=1e-9) or not math.isclose(side1, side2, abs_tol=1e-9):
            return False
            
        return True

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
    
    def _verify_square(self):
        if len(self._points) != 4:
            return False
            
        if None in self._points:
            return False
            
        point1, point2, point3, point4 = self._points

        side1 = Geometry.distance(point1, point2)
        side2 = Geometry.distance(point2, point3)
        side3 = Geometry.distance(point3, point4)
        side4 = Geometry.distance(point4, point1)

        if not math.isclose(side1, side3, abs_tol=1e-9) or not math.isclose(side2, side4, abs_tol=1e-9):
            return False
        
        angle = Geometry.get_angle(point1, point2, point3)

        if(not math.isclose(side1, side2, abs_tol=1e-9) or
           not math.isclose(side2, side3, abs_tol=1e-9) or
           not math.isclose(side3, side4, abs_tol=1e-9)):
            return False
            
        if not math.isclose(angle, math.pi / 2, abs_tol=1e-9):
            return False

        return True