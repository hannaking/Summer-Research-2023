# takes a non zero number of points and returns lists of 4 points such that they form right trapezoids 
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# interior angles 90-90-45-135 so 45-45-90 triangle rules could be used
#       x
#     *----*
#     |     \
#  2x |      \  x*sqrt(2)
#     |       \
#     *--------*
#         2x

import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from geometry import Geometry

SMALL_ANGLE = math.radians(45)
RIGHT_ANGLE = math.radians(90)
LARGE_ANGLE = math.radians(135)
DEFAULT_SIDE_LENGTH = 1

class RightTrapezoid(): 

    def __init__(self, known_coords):
        self._points = known_coords

    # get the actual points of each possible valid right trapezoid
    #
    # returns a list of lists, each containing 4 Points
    # return [] if not 4 Points used in constructor or if the Points provided cannot form a right trapezoid
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

        # 4 Points in
        # checks if the Points given are or are not a valid right trapezoid
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

        # boolean for whether this shape is vertex glued or not. default to False.
        vertex_gluing = False

        # so third points works
        second_point = pt2

        # 1 Point known
        if pt2 == None:
            # get second point
            # the segment formed will be all 4 sides
            second_point = self.get_second_point(pt1)
            vertex_gluing = True

            # fill the appropriate scenarios
            for i in range(len(scenarios)):
                scenarios[i][1] = self.get_second_point(pt1)

        side_len = Geometry.distance(pt1, second_point)

        # 2 Points known
        if pt3 == None:
            third_points = []
            third_points = self.get_third_points(pt1, second_point, side_len)

            for scenario in scenarios:
                scenario[2] = third_points.pop(0)
        
        # 3 Points known
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

    # get all possible third points (8)
    #
    # point1, point2 - 2d Point
    # side_len - length of side formed by point1 and point2
    #
    # return a list of Point objects
    def get_third_points(self, point1, point2, side_len):
        # referenced from previous side
        side_lengths = [math.sqrt(2) * side_len,
                        (2/math.sqrt(2)) * side_len,
                        .5 * side_len,
                        side_len]
        angles = [LARGE_ANGLE, SMALL_ANGLE, RIGHT_ANGLE, RIGHT_ANGLE]
        
        third_points = []
        # this will make the second side
        # t = top    a = angled side    b = base    f = flat side
        # ex t->a means point1 and point2 form the top and the next side to be formed by point2 and point3 is the angled side
        # need  t->a         a->b        b->f         f->t
        #       135, -135    45, -45     90, -90      90, -90
        for i in range(len(side_lengths)):
            # positive and negative for each
            third_points.append(Geometry.calculate_point_from_angle(angles[i], point2, point1, side_lengths[i]))
            third_points.append(Geometry.calculate_point_from_angle(-angles[i], point2, point1, side_lengths[i]))

        return third_points

    # verifies whether the points form a right trapezoid
    #
    # returns whether the Points from the constructor are a right trapezoid
    def _verify_righttrapezoid(self):
        return RightTrapezoid.are_righttrapezoids([self._points])

    # determins if the scenarios are right trapezoids
    #
    # returns whether all scenarios are right trapezoids
    @staticmethod
    def are_righttrapezoids(scenarios):
        for scenario in scenarios:
            # 4 spaces
            if len(scenario) != 4:
                return False

            # all Points defined
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

    # verifies the points are three points that can form a right trapezoid
    #
    # returns if the Points from the constructor can form a right trapezoid
    def _verify_righttrapezoid_3_points(self):
        return RightTrapezoid.are_righttrapezoidable([self._points])

    # determines whether the scenarios could form right trapezoids
    #
    # returns True if every scenario could form a right trapezoid
    @staticmethod
    def are_righttrapezoidable(scenarios):
        for scenario in scenarios:
            # 4 spaces
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

            # angle is not flat
            if math.isclose(angle, 0, abs_tol=1e-9) or math.isclose(angle, math.pi, abs_tol=1e-9):
                return False
            
        return True
    
    # ------------------------ Math ------------------------ #

    # gets the other angle in radians
    #
    # angle(radians) - corresponding angle to be converted
    #
    # returns the other angle
    @staticmethod
    def get_other_angle(angle):
        return math.copysign(1, angle) * (math.pi - abs(angle))