# takes a non zero number of points and returns lists of 8 points such that they form regular octagons 
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# all sides will be of equal length, defaulting to side length 1
# all interior angles are 135 degrees
#
# all uses of "octagon" refer to a regular octagon, even if not specified

import math
import sys
import os
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

NUM_SIDES = 8
DEFAULT_SIDE_LENGTH = 1
ANGLE = math.radians(135)
ROTATE_ANGLES = [math.radians(30),
                 math.radians(45),
                 math.radians(60),
                 math.radians(90),
                 math.radians(180),
                 math.radians(-30),
                 math.radians(-45),
                 math.radians(-60),
                 math.radians(-90)]

class Octagon():
     
    def __init__(self, known_coords):
        self._points = known_coords

    # get the actual points of each possible valid octagon
    #
    # returns a list of lists, each containing 8 Points
    # return [] if not 8 Points used in constructor or if the Points provided cannot form a regular octagon
    def coordinatize(self):

        scenarios = []

        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None)]
        sorted_points = [b[1] for b in first_sort]

        # checks if there are the correct number of points
        if len(sorted_points) != NUM_SIDES:
            return []

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]
        point5 = sorted_points[4]
        point6 = sorted_points[5]
        point7 = sorted_points[6]
        point8 = sorted_points[7]

        vertex_gluing = False

        scenarios = [[point1, point2, point3, point4, point5, point6, point7, point8]]
            
        # 8 Points in
        # checks if a pentagon can't be made or if the passed in points are already a pentagon
        if None not in sorted_points:
            if(self._verify_octagon()):
                return [self._points]
            else:
                return []

        # 1 Point in
        if point2 == None:
            scenarios = self.get_second_point_scenario(scenarios)
            vertex_gluing = True
        
        # 2 Points in
        if point3 == None:
            scenarios = self.get_third_point_scenarios(scenarios)
        else:
            # checks if the known n points can even form an octagon
            if(not self._verify_octagon_n_points()):
                return []

        # 3 Points in
        if point4 == None:            
            scenarios = self.get_next_point_scenarios(scenarios, 3)

        # 4 Points in
        if point5 == None:
            scenarios = self.get_next_point_scenarios(scenarios, 4)

        # 5 Points in
        if point6 == None:
            scenarios = self.get_next_point_scenarios(scenarios, 5)

        # 6 Points in
        if point7 == None:
            scenarios = self.get_next_point_scenarios(scenarios, 6)

        # 7 Points in
        if point8 == None:
            scenarios = self.get_next_point_scenarios(scenarios, 7)
        
        # makes all of the rotations around point1
        if vertex_gluing == True:
            scenarios = self.get_rotated_scenarios(scenarios)

        # puts back in lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        return scenarios

    # gets the scenarios with their new second points
    # the second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    # 
    # scenarios - list of lists of 1 Point and 7 Nones
    # 
    # returns the list of lists, each with 2 Points and 6 Nones (the new scenarios)
    def get_second_point_scenario(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]

            second_point = self.get_second_point(point1)
            
            new_scenarios.append([point1, second_point, None, None, None, None, None, None])

        return new_scenarios
    
    # calculates the second point given one point
    #  *second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # get the scenarios with their new third points
    # each first and second point pair has 2 possible third points, 
    # so number of scenarios will double
    # 
    # scenarios - list of lists of 2 Points and 6 Nones
    # 
    # returns the list of lists, each with 3 Points and 5 Nones (the new scenarios)
    def get_third_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]
            point2 = scenario[1]

            third_points = self.get_third_points(point1, point2)
            
            for third_point in third_points:
                new_scenarios.append([point1, point2, third_point, None, None, None, None, None])

        return new_scenarios
    
    # calculates the third points given two points
    # each first and second point pair has 2 possible third points
    # third point 1:
    #   1----2
    #         \
    #          3     positive angle
    # third point 2:
    #          3     negative angle
    #         /
    #   1----2
    #
    # point1 - 2d point
    # point2 - 2d point
    #
    # returns a list of the 2 possible third points
    def get_third_points(self, point1, point2):
        third_points = []
        side_length = Geometry.distance(point1, point2)

        third_points.append(Geometry.calculate_point_from_angle(ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-ANGLE, point2, point1, side_length))
        
        return third_points

    # get the scenarios that include their new next points
    # must know at least 3 points already
    # each scenario will have only one possible next point
    # 
    # scenarios - list of lists containing at least one None and the rest Points, length 6
    # place - int, the index of the new point
    #         place = 3 means you want to get the fourth point
    # 
    # returns the new scenario
    def get_next_point_scenarios(self, scenarios, place):
        new_scenarios = []
        for scenario in scenarios:
            # determine past 3 points
            point_prev3 = scenario[place - 3]
            point_prev2 = scenario[place - 2]
            point_prev1 = scenario[place - 1]

            # calculate this point
            new_point = self.get_next_point(point_prev3, point_prev2, point_prev1)
            
            # build the new scenario
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
    
    # rotates each scenario around the first point at the 10 predetermined angles
    # only used for shapes with only one Point provided on construction
    #
    # scenarios - the non-rotated scenarios
    #
    # returns the rotated scenarios and the original scenarios passed in, as a list
    def get_rotated_scenarios(self, scenarios):
        new_scenarios = scenarios.copy()
        for scenario in scenarios:
            for angle in ROTATE_ANGLES:
                new_scenarios.append(Geometry.rotate(scenario, angle))
        return new_scenarios

    # verify the the points compose a regular octagon
    #
    # returns whether or not the Points provided on construction compose a regular octagon
    def _verify_octagon(self):
        return Octagon.are_octagons([self._points])

    # verify the the points can form a regular octagon
    #
    # returns whether or not the points provided on construction can form a regular octagon
    def _verify_octagon_n_points(self):
        return Octagon.are_octagonable([self._points])

    # determines if all of the scenarios could create a regular octagon
    # 
    # scenarios - list of lists of Points and (possibly) Nones
    # 
    # returns whether the scenarios are n points that could form regular octagons
    @staticmethod
    def are_octagonable(scenarios):
        for scenario in scenarios:
            # not 8 scapes in the scenario list
            if len(scenario) != NUM_SIDES:
                return False
            
            num_present_sides = sum(_ is not None for _ in scenario)
            
            # no need to consider if only 2 points provided - a line segment with room for 6 more points can always become an oct
            if num_present_sides >= 3:
                # whether the loop has seen a none
                has_noned = False

                points = []
                for point in scenario:
                    # points out of order
                    # ex Point, Point, None, Point, None, None, None, None
                    if has_noned and point != None:
                        return False
                    if point == None:
                        has_noned = True
                    else:
                        points.append(point)
            
                angles = []
                sides = []
                # collect angles and side lengths
                for i in range(len(points)-2):
                    angles.append(Geometry.get_angle(points[i], points[i+1], points[i+2]))
                for i in range(len(points)-1):
                    sides.append(Geometry.distance(points[i], points[i+1]))
                
                # check that all angles match ANGLE and all side lengths match
                if not math.isclose(abs(angles[0]), ANGLE, abs_tol=1e-9):
                    return False           
                for angle in angles[1:]:
                    if not math.isclose(angle, angles[0], abs_tol=1e-9):
                        return False
                for side in sides[1:]:
                    if not math.isclose(side, sides[0], abs_tol=1e-9):
                        return False
            
        return True
    
    # determines if all of the scenarios are a regular octagon
    # checks number of sides, that no point is None, and then calls are_octagonable
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are regular octagons
    @staticmethod
    def are_octagons(scenarios):
        for scenario in scenarios:
            
            if len(scenario) != NUM_SIDES:
                return False
            
            if None in scenario:
                return False
        
        return Octagon.are_octagonable(scenarios)