# takes a non zero number of points and returns lists of 3 points such that they form isosceles triangles
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# the first side is both the non-matching and matchong side and will be length 1 unless it is an edge glue to something with a different length

import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

DEFAULT_SIDE_LENGTH = 1

class Isosceles():
    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):

        scenarios = []
        
        if len(self._points) != 3:
            return []
        
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
        # checks if the Points given are or are not a valid isosceles triangle
        if None not in sorted_points:
            if(self.are_isosceles_triangles([sorted_points])):
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
            # get third points (two because it could be above or below the start line)
            third_points = self.get_third_points(point1, point2)

        for i in range(len(third_points)):
            scenarios.append([point1, point2, third_points[i]])

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
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

    # each first-second point pair gets 6 possible third points
    #
    # point1 - 2d Point
    # point2 - 2d Point
    #
    # return list of 6 third points
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        angles = [math.radians(30.0), math.radians(75.0), math.radians(67.5)]
        third_points = []
        for angle in angles:
            alt_hyp_side_length = side_length / (2.0 * math.cos(angle))
            alt_base_side_length = 2.0 * math.cos(angle) * side_length
            alternate_angle = math.pi - 2.0 * angle

            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_base_side_length))
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_base_side_length))

            third_points.append(Geometry.calculate_point_from_angle(alternate_angle, point2, point1, side_length))
            third_points.append(Geometry.calculate_point_from_angle(-alternate_angle, point2, point1, side_length))

            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_hyp_side_length))
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_hyp_side_length))

        return third_points

    # verifies the points form an isosceles triangle
    #
    # returns whether Points given on construction are an isosceles triangle
    def _verify_isosceles_triangle(self):
        return Isosceles.are_isosceles_triangles([self._points])
    
    # determines wheter the scenarios form isosceles triangles
    #
    # scenarios - list of lists of 3 points
    #
    # return True if 3 Points and isosceles
    @staticmethod
    def are_isosceles_triangles(scenarios):
        for scenario in scenarios:
            if len(scenario) != 3:
                return False
        
            if None in scenario:
                return False

            point1, point2, point3 = scenario

            side1 = Geometry.distance(point1, point2)
            side2 = Geometry.distance(point1, point3)
            side3 = Geometry.distance(point2, point3)
            
            if (not math.isclose(side1, side2) and
                not math.isclose(side1, side3) and
                not math.isclose(side2, side3)):
                return False

        return True