import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import *

from geometry import Geometry

ANGLE = math.radians(108)
DEFAULT_SIDE_LENGTH = 1

# 5 sides of equal length, all angles are 108 degrees

class Pentagon(): 
    # take a list of 1-5 Points, the unknown Points being None
    # known information about the starting position of the pentagon
    def __init__(self, known_coords):
        self._points = known_coords

    # Get Points to make up the Pentagon
    #
    # returns a list of lists of 5 Points, each list is one possible coordinatization of the pentagon
    def coordinatize(self):
        scenarios = [] # list of lists of Points

        # start with anywhere from 1 to 5 points
        # if all Points are given (5 points), return that one scenario
        if None not in self._points:
            if(self._verify_pentagon()):
                return [self._points]
            else:
                return []

        # sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # get the sorted points list out of that sort
        sorted_points = [b[1] for b in first_sort]

        side_length = DEFAULT_SIDE_LENGTH
        vertex_gluing = False
        
        over_half = True if sum(_ is not None for _ in self._points) > len(self._points) / 2 else False
        # add stuff here so it leaves if angle formed by over_half points is not 108
        # and so it doesn't try getting angle with Nones
        if over_half and not math.isclose(Geometry.get_angle(sorted_points[0], sorted_points[1], sorted_points[2]), ANGLE): return []
        
        # to make it easier to understand what sorted points are
        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]
        pt5 = sorted_points[4]

        # pre-rotate, there is only 2 options
        # third point up or third point down (pos and neg ANGLE)
        # so 2 scenarios
        scenarios = [[pt1, pt2, pt3, pt4, pt5],
                     [pt1, pt2, pt3, pt4, pt5]]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            scenarios[0][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            scenarios[1][1] = Point(pt1.x + DEFAULT_SIDE_LENGTH, pt1.y)
            vertex_gluing = True

        # now have at least 2 points, so side length can be determined
        #                                    both will be same, doesn't matter which one
        side_length = Geometry.distance(pt1, scenarios[1][1])

        # then continue to the next
        if  (sorted_points[2] == None): # two known points
            # 2 possible third points - pos and neg
            scenarios[0][2] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][1], pt1, side_length)
            scenarios[1][2] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][1], pt1, side_length)


        # fix these next 2. coming in with >=3 points, it might not be in this order


        # then continue to the next
        if  (sorted_points[3] == None): # three known points
            # each third point has one possible fourth point
            scenarios[0][3] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][2], scenarios[0][1], side_length)
            scenarios[1][3] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][2], scenarios[1][1], side_length)


        # then continue to the next
        if (sorted_points[4] == None): # four known points
            # each fourth point has one possible fifth point
            scenarios[0][4] = Geometry.calculate_point_from_angle(ANGLE, scenarios[0][3], scenarios[0][2], side_length)
            scenarios[1][4] = Geometry.calculate_point_from_angle(-ANGLE, scenarios[1][3], scenarios[1][2], side_length)

        # all five points known handled above

        if over_half:
            scenarios = [scenarios[0]] if Geometry.calculate_point_from_angle(ANGLE, scenarios[0][4], scenarios[0][3], side_length) == scenarios[0][0] else [scenarios[1]]

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            # note: rotate about point 1, because point 1 is either the origin or the vertex it is glued to.
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

        # a list of lists of 5 Points
        return scenarios

    def _verify_pentagon(self):
        if len(self._points) != 5:
            return False

        # Calculate the lengths of the five sides of the triangle
        side1 = Geometry.distance(self._points[0], self._points[1])
        side2 = Geometry.distance(self._points[1], self._points[2])
        side3 = Geometry.distance(self._points[2], self._points[3])
        side4 = Geometry.distance(self._points[3], self._points[4])
        side5 = Geometry.distance(self._points[4], self._points[0])
        
        # Check side length equality
        if not math.isclose(side1, side2) or not math.isclose(side2, side3) or not math.isclose(side3, side4) or not math.isclose(side4, side5) or not math.isclose(side5, side1):
            return False

        # calculate angles
        angle1 = Geometry.get_angle(self._points[0], self._points[1], self._points[2])
        angle2 = Geometry.get_angle(self._points[1], self._points[2], self._points[3])
        angle3 = Geometry.get_angle(self._points[2], self._points[3], self._points[4])
        angle4 = Geometry.get_angle(self._points[3], self._points[4], self._points[0])
        angle5 = Geometry.get_angle(self._points[4], self._points[0], self._points[1])

        # check angle equalities
        if not math.isclose(angle1, angle2) or not math.isclose(angle2, angle3) or not math.isclose(angle3, angle4) or not math.isclose(angle4, angle5) or not math.isclose(angle5, angle1):
            return False

        return True