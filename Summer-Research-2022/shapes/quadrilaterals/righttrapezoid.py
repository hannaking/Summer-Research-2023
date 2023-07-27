import math

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

# i decided to use 45 and 135 for the non-right angles
# i also decided the top and angled sides would be equal
# (both so I could determine side lengths -> 45-45-90 tri rules are nice)
SMALL_ANGLE = math.radians(45)
RIGHT_ANGLE = math.radians(90)
LARGE_ANGLE = math.radians(135)
DEFAULT_SIDE_LENGTH = 1
# top side = x
# angled side = sqrt(2)x
# flat side = x
# bottom = 2x
# *----*
# |     \
# |      \
# |       \
# *--------*

class RightTrapezoid(): 

    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        # you will start with either one point, two points, or three points.
        #
        # First, we sort the coordinates
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

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords , dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # but this does get a sorted points list
        sorted_points = [b[1] for b in first_sort]

        # to make it easier to understand what sorted points are
        pt1 = sorted_points[0]
        pt2 = sorted_points[1]
        pt3 = sorted_points[2]
        pt4 = sorted_points[3]

        # checks if a right trapezoid can't be made or if the passed in points are already a right trapezoid
        if None not in sorted_points:
            if(self._verify_righttrapezoid()):
                return [self._points]
            else:
                return []

        scenarios = [[pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4],
                     [pt1, pt2, pt3, pt4]]  # list of lists of Points
        # maximum possible scenarios is 80 -> 1 option for first point
        #                                     1 options for second point for every first point
        #                                     8 options for third point for every second point
        #                                     1 option for fourth point for every third point
        #                                     = 8 before rotations
        #                                     * (this + 9 angles) = 80 max scenarios

        # boolean that tells whether this shape is vertex glued or not. default to False.
        vertex_gluing = False

        # so third points works
        second_point = pt2

        if pt2 == None:
            # get second point
            # will be all 4 sides
            second_point = self.get_second_point(pt1)
            # since we only have one point, we know that the rectangle is vertex glued.
            vertex_gluing = True
            # fill the appropriate scenarios
            for i in range(len(scenarios)):
                scenarios[i][1] = self.get_second_point(pt1)

        side_len = Geometry.distance(pt1, second_point)

        if pt3 == None:
            # get third points
            third_points = []
            third_points = self.get_third_points(pt1, second_point, side_len)
            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
        
        if pt4 == None:
            if(pt3 != None and not self._verify_righttrapezoid_3_points()):
                return []
            # get fourth points
            for scenario in scenarios:
                # get angle between points
                past_angle = Geometry.get_angle(scenario[0], scenario[1], scenario[2])
                past_side_len = Geometry.distance(scenario[1], scenario[2])
                # +/-45
                if math.isclose(math.degrees(abs(past_angle)), 45):
                    scenario[3] = Geometry.calculate_point_from_angle((past_angle / abs(past_angle)) * math.radians(90), scenario[2], scenario[1], 0.5 * past_side_len)
                    # +/- 135
                elif math.isclose(math.degrees(abs(past_angle)), 135):
                    scenario[3] = Geometry.calculate_point_from_angle((past_angle / abs(past_angle)) * math.radians(45), scenario[2], scenario[1], math.sqrt(2) * past_side_len)
                # either 90
                else:
                    first_side_len = Geometry.distance(scenario[0], scenario[1])
                    if math.isclose(past_side_len, first_side_len):
                        scenario[3] = Geometry.calculate_point_from_angle((past_angle / abs(past_angle)) * math.radians(135), scenario[2], scenario[1], math.sqrt(2) * past_side_len)
                    else:
                        scenario[3] = Geometry.calculate_point_from_angle((past_angle / abs(past_angle)) * math.radians(90), scenario[2], scenario[1], 1 * past_side_len)

        # get rid of any unused / empty / repeated scenarios
        # necessary?
        scenarios = [x for x in scenarios if None not in x]

        # you would only ever want to rotate your shape if you are vertex glued.
        # if you are already given two or three points, there is no point in rotating your shape.
        if vertex_gluing == True:
            # now we will rotate each scenario by [30,45,60,90,180,-30-45,-60,-90] degrees (will convert to radians),
            # creating a new scenario, and add it to the list of scenarios
            # 8 scenarios * 9 angles = 72 new scenarios
            # 80 scenarios in total
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

    # returns a list of 2  Point objects.
    # if you get here, you are vertex glued. use default side values
    # you need to have this first side be the short side and the long side (so a list)
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    # return a list of Point objects. 
    def get_third_points(self, point1, point2, side_len):
        side_lengths = [math.sqrt(2) * side_len,
                        (2/math.sqrt(2)) * side_len,
                        .5 * side_len,
                        side_len]
        angles = [LARGE_ANGLE, SMALL_ANGLE, RIGHT_ANGLE, RIGHT_ANGLE]
        
        third_points = []
        # this will make the second side
        # so, need  t->a       a->b      b->f        f->t
        #           135, -135  45, -45   90, -90     90, -90
        for i in range(len(side_lengths)):
            third_points.append(Geometry.calculate_point_from_angle(angles[i], point2, point1, side_lengths[i]))
            third_points.append(Geometry.calculate_point_from_angle(-angles[i], point2, point1, side_lengths[i]))

        return third_points

    def _verify_righttrapezoid(self):
        return RightTrapezoid.are_righttrapezoids([self._points])

    @staticmethod
    def are_righttrapezoids(scenarios):
        for scenario in scenarios:
            if len(scenario) != 4:
                return False

            if None in scenario:
                return False

            point1, point2, point3, point4 = scenario

            angle1 = Geometry.get_angle(point1, point2, point3)
            angle2 = Geometry.get_angle(point2, point3, point4)
            angle3 = Geometry.get_angle(point3, point4, point1)
            angle4 = Geometry.get_angle(point4, point1, point2)

            if (not((math.isclose(angle1, RightTrapezoid.get_other_angle(angle2)) and
                     math.isclose(angle3, angle4) and
                     math.isclose(angle3, math.pi / 2)) or 
                    (math.isclose(angle1, RightTrapezoid.get_other_angle(angle4)) and
                     math.isclose(angle2, angle3) and
                     math.isclose(angle2, math.pi / 2))
                     )):
                print(angle1, angle2, angle3, angle4)
                return False
                

        return True

    def _verify_righttrapezoid_3_points(self):
        return RightTrapezoid.are_righttrapezoidable([self._points])

    @staticmethod
    def are_righttrapezoidable(scenarios):
        for scenario in scenarios:
            if len(scenario) != 4:
                    return False
            
            if(scenario[0] == None or
               scenario[1] == None or
               scenario[2] == None or
               scenario[3] != None):
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]
            
            angle = abs(Geometry.get_angle(point1, point2, point3))

            if math.isclose(angle, 0, abs_tol=1e-9) or math.isclose(angle, math.pi, abs_tol=1e-9):
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