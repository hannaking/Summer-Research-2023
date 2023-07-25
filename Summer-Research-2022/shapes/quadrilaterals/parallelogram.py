import math
import sys
import os
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

DEFAULT_SIDE_LENGTH = 1
DEFAULT_RATIO = 2
DEFAULT_ANGLES = [math.radians(30),
                  math.radians(45),
                  math.radians(60)]

class Parallelogram():
     
    def __init__(self, known_coords):
        self._points = known_coords

    # takes a non zero number of points and returns lists of 4 points such that they form parellegrams 
    # if one point is passed in the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90
    # degree roations
    # the sides have a ratio of 1:2 unless the ratio is included in the input points
    #
    # returns a list of scenarios
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
            
        # checks if a parallelogram can't be made or if the passed in points are already a parallelogram
        if None not in sorted_points:
            if(self.are_parallelograms(scenarios)):
                return [self._points]
            else:
                return []

        if point2 == None:
            scenarios = self.get_second_point_scenarios(scenarios)
            vertex_gluing = True
        
        if point3 == None:
            scenarios = self.get_third_point_scenarios(scenarios)

        if point4 == None:
            # checks if the known three points can even form a parallelogram
            if(not self.are_parallelogramable(scenarios)):
                return []
            scenarios = self.get_fourth_point_scenarios(scenarios)
        
        # makes all of the rotations around point1
        if vertex_gluing == True:
            angles = [30, 45, 60, 90, 180, -30, -45, -60, -90]
            original_scenario_len = len(scenarios)
            for i in range(original_scenario_len):
                for angle in angles:
                    new_scenario = Geometry.rotate(scenarios[i], math.radians(angle))
                    scenarios.append(new_scenario)

        # puts back it lattice order
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
            
            for i, third_point in enumerate(third_points):
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
        alt_short = side_length / DEFAULT_RATIO
        alt_long = side_length * DEFAULT_RATIO

        # angle --> small angle
        for angle in DEFAULT_ANGLES:
            other_angle = Parallelogram.get_other_angle(angle)

            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_long))
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_long))

            third_points.append(Geometry.calculate_point_from_angle(other_angle, point2, point1, alt_long))
            third_points.append(Geometry.calculate_point_from_angle(-other_angle, point2, point1, alt_long))

            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_short))
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_short))

            third_points.append(Geometry.calculate_point_from_angle(other_angle, point2, point1, alt_short))
            third_points.append(Geometry.calculate_point_from_angle(-other_angle, point2, point1, alt_short))
        
        return third_points

    # gets the scenarios that include the fourth points from the scenarios including
    # only the first, second, and third points.
    #  *there is 1 scenerio if the created sides are of different lengths and 2 if
    #   the sides are of the same length
    # 
    # scenarios - list of list of one point and three Nones
    # 
    # returns the new scenario
    def get_fourth_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]

            fourth_point = self.get_fourth_point(point1, point2, point3)
            
            new_scenarios.append([point1, point2, point3, fourth_point])
        
        return new_scenarios

    # gets the fourth point given three points
    #
    # point1 - 2d point
    # point2 - 2d point
    # point3 - 2d point
    #
    # returns the fourth point
    def get_fourth_point(self, point1, point2, point3):
        side1 = Geometry.distance(point1, point2)

        angle = Geometry.get_angle(point1, point2, point3)
        other_angle = Parallelogram.get_other_angle(angle)

        fourth_point = Geometry.calculate_point_from_angle(other_angle, point3, point2, side1)

        return fourth_point

    # verify the the points compose a parallelogram
    #
    # returns whether or not it composes a parallelogram
    def _verify_parallelogram(self):
        return Parallelogram.are_parallelograms([self._points])

    # verify the the first 3 points can form a parallelogram
    #
    # returns whether or not it can form a parallelogram
    def _verify_parallelogram_3_points(self):
        return Parallelogram.are_parallelogramable([self._points])

    # determins if all of the scenarios are posible to create a parallelogram
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 3 points that could form parallelograms
    @staticmethod
    def are_parallelogramable(scenarios):
        for scenario in scenarios:
            if len(scenario) != 4:
                return False
            
            if (scenario[0] == None or
                scenario[1] == None or
                scenario[2] == None or
                scenario[3] != None):
                print(scenario)
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]
            
            angle = abs(Geometry.get_angle(point1, point2, point3))

            if math.isclose(angle, math.pi, abs_tol=1e-9) or math.isclose(angle, 0, abs_tol=1e-9):
                return False
            
        return True
    
    @staticmethod
    def are_parallelograms(scenarios):
        for scenario in scenarios:
            
            if len(scenario) != 4:
                return False
            
            if None in scenario:
                return False
            
            point1, point2, point3, point4 = scenario

            side1 = Geometry.distance(point1, point2)
            side2 = Geometry.distance(point2, point3)
            side3 = Geometry.distance(point3, point4)
            side4 = Geometry.distance(point4, point1)

            if not math.isclose(side1, side3, abs_tol=1e-9) or not math.isclose(side2, side4, abs_tol=1e-9):
                return False
        
            angle1 = Geometry.get_angle(point1, point2, point3)
            angle2 = Geometry.get_angle(point2, point3, point4)

            alt_angle2 = Parallelogram.get_other_angle(angle1)

            if not math.isclose(angle2, alt_angle2, abs_tol=1e-9):
                return False
            
            if math.isclose(angle2, math.pi, abs_tol=1e-9) or math.isclose(angle2, 0, abs_tol=1e-9):
                return False

        return True
    
    # Math

    # gets the other angle in radians 
    #
    # angle(radians) - corrisponding angle to be converted
    #
    # returns the other angle
    @staticmethod
    def get_other_angle(angle):
        return math.copysign(1, angle) * (math.pi - abs(angle))