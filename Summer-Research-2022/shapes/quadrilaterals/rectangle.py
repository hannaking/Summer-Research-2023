import sys
import math
import collections

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from shapes.geometry import Geometry
from shapes.vector import Vector

ANGLE = math.radians(90)
DEFAULT_SIDE_LENGTH = 1

# _points = a list of Point objects that represent the starting position for the equilateral triangle

#TODO: update for rectangles. you do not need to change anything other than get_second_point, get_third_points, and get_fourth_points.
# change them so that:
# - given 1 point, get the second point as the LONG SIDE
# - given 1 point, get the second point as the SHORT SIDE
# - given 2 points, get the third point as the LONG SIDE
# - given 2 points, get the third point as the SHORT SIDE
# - given 3 points, get the fourth point as whatever side formed between the first and second points (LONG or SHORT)
class Rectangle(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        # you will start with either one point, two points, or three points.
        #
        # First, we sort the coordinates #?
        #
        # if you have one point, you will need to find the second point. There is only one option: 1 unit to the right of the start point.
        # We make this decision based on the fact that since we only know the first point, we have no knowledge of the size of the square,
        # so we default to 1 unit. It is to the right because it would look the same whether it was to the left, up, or down, so it does not make
        # much of a meaningful difference.
        #
        # once two points are found, you will need to find the third points (plural!) 
        # If you were given two points to start with, you find the distance between the two. 
        # This is the side length of the square, so you know how far away the third point should be.
        # There are two options: above the second point and below the second point.
        #
        # Once three points are found, you will need to find the fourth points.
        # There is only one option: the final corner of the square.
        # However, you need to repeat the process for each third coordinate.
        # Like before, find the side length by finding the distance between two of the points.
        # Then you'll find the points that are 90 and -90 degrees from the line formed by the third point and the second point.
        # Only one of these coordinates is correct.
        # We find the correct point by creating vectors between the first point and the second point, then the first point and the two possible third points.
        # We check which of the vectors are orthogonal to the vector between the first point and the second point.
        # The one that is orthogonal is the correct point.
        # The one that is not orthogonal is the incorrect point.
        #
        # Once you have the fourth point, you have a complete scenario.
        #
        # For each of these scenarios, we rotate the points about the origin with the angles we care about:
        # [30, 45, 60, 90, 180 ,-30, -45 ,-60 ,-90] degrees (will convert to radians)
        # Each of these is a new scenario.
        # We then unsort these scenarios, then return them.

        scenarios = []  # list of lists of Points

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        # to make it easier to understand what sorted points are
        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]
        point4 = sorted_points[3]

        # boolean that tells whether this square is vertex glued or not. default to False.
        vertex_gluing = False

        if point2 == None:
            # get second point
            point2 = self.get_second_point(point1)
            # since we only have one point, we know that the square is vertex glued.
            vertex_gluing = True

        if point3 == None:
            # get third points 
            third_points = self.get_third_points(point1, point2)
        
        if point4 == None:
            # get fourth points
            fourth_points = self.get_fourth_points(point1, point2)

        # we have two scenarios at 0 degrees: above the x axis and below the x axis
        scenarios.append([point1, point2, third_points[0], fourth_points[0]])
        scenarios.append([point1, point2, third_points[1], fourth_points[1]])

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            # 2 scenarios * 9 angles = 18 new scenarios
            # 20 scenarios in total
            # note: we are rotating the points about point 1, because we know that point 1 is either the origin or the vertex we are glued to.
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

        # a list of lists of 4 Points
        return scenarios

    # returns a Point object. there is only one option: 1 unit to the right of the start point.
    #TODO: update for rectangles
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # return a list of Point objects. 
    # finds the third points by finding the point 90 degrees and -90 degrees from the line formed by pt 1 and pt 2
    #TODO: update for rectangles
    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []
        third_points.append(Geometry.calculate_point_from_angle(ANGLE, point2, point1, side_length))
        third_points.append(Geometry.calculate_point_from_angle(-ANGLE, point2, point1, side_length))

        return third_points

    # return a Point object. there is 1 option: the final corner of the square.
    # finds the fourth points by finding the point -90 degrees and 90 degrees from the line formed by pt 2 and pt 1
    # notice how this is FLIPPED from get_third_points.
    #TODO: update for rectangles
    def get_fourth_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        fourth_points = []
        fourth_points.append(Geometry.calculate_point_from_angle(-ANGLE, point1, point2, side_length))
        fourth_points.append(Geometry.calculate_point_from_angle(ANGLE, point1, point2, side_length))

        return fourth_points
