# takes a non zero number of points and returns lists of 4 points such that they form kites
# a kite has two equal angles and two pairs of adjacent equal-length sides
#
# if only one point is used in construction, the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# if less than 3 points in, uses 60-90-120-90 angles

import math
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from quadrilaterals.dart import Dart
from geometry import Geometry

# if less than 3 points in, use 60-90-120-90 angles
DEFAULT_ANGLE_MIDDLE = math.radians(90)
DEFAULT_ANGLE_SMALL = math.radians(60)
DEFAULT_ANGLE_LARGE = math.radians(120)

DEFAULT_SIDE_LENGTH = 1
DEFAULT_RATIO = math.sqrt(3)

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

    # get the actual points of each possible valid kite
    #
    # returns a list of lists, each containing 4 Points
    # return [] if not 4 Points used in constructor or if the Points provided cannot form a kite
    def coordinatize(self):

        scenarios = []

        # sorts to be traversible in order
        # (so Points are built in a path order around the shape, not in the order they occur on the lattice)
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
            
        # 4 Points in
        # checks if the Points given are or are not a valid kite
        if None not in sorted_points:
            if(self.are_kites(scenarios)):
                return [self._points]
            else:
                return []

        # 1 Point known
        if point2 == None:
            scenarios = self.get_second_point_scenarios(scenarios)
            vertex_gluing = True

        # 2 Points known
        if point3 == None:
            # get third and fourth points together
            #
            # the existing side is every side of the kite
            # next side needs to be equal, longer, and shorter
            #       /\
            #      /  \
            #   a /    \ b       short sides
            #    /      \
            #   /        \
            #   \        /
            #  d \      / c        long sides          (ascii limitations)
            #     \    / 
            #      \  /
            #       \/
            # need to go a -> b   (short side, short side) (large angle)
            #            b -> c   (short side, long side)  (middle/duplicated angle)
            #            c -> d   (long side, long side)   (small angle)
            #            d -> a   (long side, short side)  (middle, duplicated angle)
            # and each of those need to be done with both positive and negative angles
            # total = 8 possible third points
            # each third point has one possible fourth point
            new_scenarios = []
            for scenario in scenarios:
                next_side_length_a = Geometry.distance(scenario[0], scenario[1]) * DEFAULT_RATIO
                next_side_length_b = Geometry.distance(scenario[0], scenario[1]) / DEFAULT_RATIO
                next_side_length_c = Geometry.distance(scenario[0], scenario[1])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_a),
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_SMALL, Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_a), scenario[1], next_side_length_a)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_b),
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_LARGE, Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_b), scenario[1], next_side_length_b)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_SMALL, scenario[1], scenario[0], next_side_length_c),
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, Geometry.calculate_point_from_angle(DEFAULT_ANGLE_SMALL, scenario[1], scenario[0], next_side_length_c), scenario[1], next_side_length_b)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_LARGE, scenario[1], scenario[0], next_side_length_c),
                                      Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE, Geometry.calculate_point_from_angle(DEFAULT_ANGLE_LARGE, scenario[1], scenario[0], next_side_length_c), scenario[1], next_side_length_a)])
                
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_a),
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_SMALL, Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_a), scenario[1], next_side_length_a)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_b),
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_LARGE, Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, scenario[1], scenario[0], next_side_length_b), scenario[1], next_side_length_b)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_SMALL, scenario[1], scenario[0], next_side_length_c),
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_SMALL, scenario[1], scenario[0], next_side_length_c), scenario[1], next_side_length_b)])
                new_scenarios.append([scenario[0],
                                      scenario[1],
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_LARGE, scenario[1], scenario[0], next_side_length_c),
                                      Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_MIDDLE, Geometry.calculate_point_from_angle(-DEFAULT_ANGLE_LARGE, scenario[1], scenario[0], next_side_length_c), scenario[1], next_side_length_a)])

            scenarios = new_scenarios

        # 3 Points known
        elif point4 == None:

            if not self._verify_kite_3_points(): return []

            for scenario in scenarios:
                # pick the appropriate side length
                past_side_lengths = [abs(Geometry.distance(scenario[0], scenario[1])),
                                     abs(Geometry.distance(scenario[1], scenario[2]))]
                # if the 2 existing sides are of equal length, this next one will be *ratio and /ratio of that length
                # if the 2 existing sides are not equal, this next one will be the length of the second side

                angle_sign_multiplier = Geometry.get_angle(scenario[0], scenario[1], scenario[2]) / abs(Geometry.get_angle(scenario[0], scenario[1], scenario[2]))

                # if you know two non-equal sides, you can solve the kite w SSS triangle proof
                # long side, short side
                # uses the large angle to go from short to short
                if past_side_lengths[0] > past_side_lengths[1]:
                    next_angle = max(self.all_angles(past_side_lengths[1],
                                                     past_side_lengths[0],
                                                     Geometry.distance(scenario[0], scenario[2])))
                    scenario[3] = Geometry.calculate_point_from_angle(next_angle * angle_sign_multiplier, scenario[2], scenario[1], Geometry.distance(scenario[1], scenario[2]))
                
                # short side, long side
                # uses the small angle to go from long to long
                elif past_side_lengths[0] < past_side_lengths[1]:
                    next_angle = min(self.all_angles(past_side_lengths[1],
                                                     past_side_lengths[0],
                                                     Geometry.distance(scenario[0], scenario[2])))
                    scenario[3] = Geometry.calculate_point_from_angle(next_angle * angle_sign_multiplier, scenario[2], scenario[1], Geometry.distance(scenario[1], scenario[2]))
                
                # two equal sides
                # always uses the middle / duplicated angle
                else:                    
                    scenario[3] = Geometry.calculate_point_from_angle(DEFAULT_ANGLE_MIDDLE * -angle_sign_multiplier, scenario[2], scenario[1], Geometry.distance(scenario[1], scenario[2]) * math.tan(Geometry.get_angle(scenario[0], scenario[1], scenario[2]) / 2))

        # makes all of the rotations around point1
        if vertex_gluing == True:
            scenarios = self.get_rotated_scenarios(scenarios)

        # put back in lattice order
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        return scenarios

    # gets the scenarios with their new second points
    # the second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    # 
    # scenarios - list of lists of 1 Point and 5 Nones
    # 
    # returns the list of lists, each with 2 Points and 4 Nones (the new scenarios)
    def get_second_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]

            second_point = self.get_second_point(point1)
            
            new_scenarios.append([point1, second_point, None, None])

        return new_scenarios
    
    # calculates the second point given one point
    #  *second point is placed DEFAULT_SIDE_LENGTH units to the right (1 unit)
    #
    # point1 - 2d point
    #
    # returns the second point
    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)
    
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

    # determins if all of the scenarios area ble to create a kite
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 3 points that could form kites
    @staticmethod
    def are_kiteable(scenarios):
        for scenario in scenarios:
            # 4 spaces
            if len(scenario) != 4:
                return False
            
            # order (first three are Points and last is None)
            if (scenario[0] == None or
                scenario[1] == None or
                scenario[2] == None or
                scenario[3] != None):
                return False

            point1 = scenario[0]
            point2 = scenario[1]
            point3 = scenario[2]            
            
            #
            # matching up the intersection I
            #        ^
            #       /|\ 
            #      / | \     r = right   (below)
            #     /  |  \    l = left    (below)
            #    /   |   \
            #   /____|____\ 
            #   \  r |  l /
            #    \   |   /
            #     \  |  /
            #      \ | /
            #       \|/
            #        v
            #

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
    
    # determins if all of the scenarios are a kite
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 4 points that form kites
    @staticmethod
    def are_kites(scenarios):
        for scenario in scenarios:
            # 4 spaces
            if len(scenario) != 4:
                return False
            
            # all Points filled
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
    # ------------------------------------------------ MATH ----------------------------------------------- #
    # returns all three unique angles involved in the kite
    def all_angles(self, short_side, long_side, diag):
        return [self.get_a1(short_side, long_side, diag),
                self.get_a2(short_side, long_side, diag),
                self.get_a3(self.get_a1(short_side, long_side, diag),
                            self.get_a2(short_side, long_side, diag))]

    # these use the SSS triangle proof on half the kite to solve for the angles
    # first two could be either depending on kite orientation
    #
    # top / large angle (or bottom / small angle)
    def get_a1(self, short_side, long_side, diag):
        return 2 * math.acos((math.pow(short_side, 2) + math.pow(diag, 2) - math.pow(long_side, 2)) / 
                         (2 * short_side * diag))

    # bottom / small angle (or top / large angle)
    def get_a2(self, short_side, long_side, diag):
        return 2 * math.acos((math.pow(long_side, 2) + math.pow(diag, 2) - math.pow(short_side, 2)) / 
                         (2 * long_side * diag))

    #other angle (duplicated / middle angle)
    def get_a3(self, a1, a2):
        return 180 - (a1/2) - (a2/2)
