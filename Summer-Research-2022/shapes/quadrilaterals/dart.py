# takes a non zero number of points and returns lists of 4 points such that they form darts

# if one point is passed in the scenerios include 30, 45, 60, 90, 180, -30, -45, -60, and -90 degree rotations
#
# the sides have a ratio of 1:2 if possible otherwise the small angle = (180 - top angle) / 4
#
#
# s  --> small angle
# b  --> big angle
# b' --> angle opposite of big angle
# t  --> top angle
# I  --> short side
# L  --> large side
#               / \
#             /  t  \
#           /         \
#       L /     _b_     \ L
#       /     /  b' \     \
#     / s /             \ s \
#   / /  I               I  \ \
# //                           \\

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
DEFAULT_ANGLES = [#math.radians(30),
                  #math.radians(45),
                  #math.pi - (math.radians(330) + 2*math.asin(math.sin(math.radians(330)/2)/2))/2,
                  #math.pi - (math.radians(315) + 2*math.asin(math.sin(math.radians(315)/2)/2))/2,
                  math.pi - (math.radians(300) + 2*math.asin(math.sin(math.radians(300)/2)/2))/2,
                  math.pi - (math.radians(270) + 2*math.asin(math.sin(math.radians(270)/2)/2))/2]

class Dart():
     
    def __init__(self, known_coords):
        self._points = known_coords

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
            
        # checks if a dart can't be made or if the passed in points are already a dart
        if None not in sorted_points:
            if(self.are_darts(scenarios)):
                return [self._points]
            else:
                return []

        if point2 == None:
            scenarios = self.get_second_point_scenarios(scenarios)
            vertex_gluing = True
        
        if point3 == None:
            scenarios = self.get_third_and_fourth_point_scenarios(scenarios)

        elif point4 == None:
            # checks if the known three points can even form a dart
            if(not self.are_dartable([sorted_points])):
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

    # gets the scenarios that include the third and fourth points from the scenario including
    # only the first point and the second point.
    #  *there are 48 new scenarios per pair of first and second points
    #   6 angles * 8 arrangements
    # 
    # scenarios - list of list of one point and three Nones
    # 
    # returns the new scenario
    def get_third_and_fourth_point_scenarios(self, scenarios):
        new_scenarios = []
        for scenario in scenarios:
            point1 = scenario[0]
            point2 = scenario[1]

            third_points, fourth_points = self.get_third_and_fourth_points(point1, point2)
            
            for i, third_point in enumerate(third_points):
                new_scenarios.append([point1, point2, third_point, fourth_points[i]])
        
        return new_scenarios
    
    # gets the third and fourth points given two points
    #
    # point1 - 2d point
    # point2 - 2d point
    #
    # returns the third and fourth points
    def get_third_and_fourth_points(self, point1, point2):
        third_points = []
        fourth_points = []
        side_length = Geometry.distance(point1, point2)
        
        # angle --> small angle
        for angle in DEFAULT_ANGLES:
            alt_lng_sl = side_length * DEFAULT_RATIO
            alt_sml_sl = side_length / DEFAULT_RATIO

            diagonal_sl = self.get_diagonal(small_side_length=alt_sml_sl, ratio=DEFAULT_RATIO, small_angle=angle)
            top_angle = self.get_top_angle(small_side_length=alt_sml_sl, diagonal=diagonal_sl, small_angle=angle)
            big_angle = self.get_big_angle(top_angle=top_angle, small_angle=angle)
            
            #  I / \                 L
            #   / s \ L    and    -------
            #      t \                t /
            #  -------             \ s / L
            #     L               I \ /
            #
            # side_length --> long side length
            third_points.append(Geometry.calculate_point_from_angle(top_angle, point2, point1, side_length))
            fourth_points.append(Geometry.calculate_point_from_angle(angle, third_points[-1], point2, alt_sml_sl))

            third_points.append(Geometry.calculate_point_from_angle(-top_angle, point2, point1, side_length))
            fourth_points.append(Geometry.calculate_point_from_angle(-angle, third_points[-1], point2, alt_sml_sl))
            
            #  I / \                 L
            #   / b \ I    and    -------
            #      s \                s /
            #  -------             \ b / I
            #     L               I \ /
            #
            # side_length --> long side length
            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_sml_sl))
            fourth_points.append(Geometry.calculate_point_from_angle(big_angle, third_points[-1], point2, alt_sml_sl))
            
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_sml_sl))
            fourth_points.append(Geometry.calculate_point_from_angle(-big_angle, third_points[-1], point2, alt_sml_sl))

            diagonal_sl = self.get_diagonal(small_side_length=side_length, ratio=DEFAULT_RATIO, small_angle=angle)
            top_angle = self.get_top_angle(small_side_length=side_length, diagonal=diagonal_sl, small_angle=angle)
            big_angle = self.get_big_angle(top_angle=top_angle, small_angle=angle)


            #  L / \                 I
            #   / t \ L    and    -------
            #      s \                s /
            #  -------             \ t / L
            #     I               L \ /
            #
            # side_length --> short side length
            third_points.append(Geometry.calculate_point_from_angle(angle, point2, point1, alt_lng_sl))
            fourth_points.append(Geometry.calculate_point_from_angle(top_angle, third_points[-1], point2, alt_lng_sl))
            
            third_points.append(Geometry.calculate_point_from_angle(-angle, point2, point1, alt_lng_sl))
            fourth_points.append(Geometry.calculate_point_from_angle(-top_angle, third_points[-1], point2, alt_lng_sl))
            
            #  L / \                 I
            #   / s \ I    and    -------
            #      b \                b /
            #  -------             \ s / I
            #     I               L \ /
            #
            # side_length --> short side length
            third_points.append(Geometry.calculate_point_from_angle(big_angle, point2, point1, side_length))
            fourth_points.append(Geometry.calculate_point_from_angle(angle, third_points[-1], point2, alt_lng_sl))
            
            third_points.append(Geometry.calculate_point_from_angle(-big_angle, point2, point1, side_length))
            fourth_points.append(Geometry.calculate_point_from_angle(-angle, third_points[-1], point2, alt_lng_sl))
        
        return third_points, fourth_points

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

            fourth_points = self.get_fourth_points(point1, point2, point3)
            
            for fourth_point in fourth_points:
                new_scenarios.append([point1, point2, point3, fourth_point])
        
        return new_scenarios

    # gets the fourth points given three points
    #
    # point1 - 2d point
    # point2 - 2d point
    # point3 - 2d point
    #
    # returns the fourth points
    def get_fourth_points(self, point1, point2, point3):
        side1 = Geometry.distance(point1, point2)
        side2 = Geometry.distance(point2, point3)
        angle = Geometry.get_angle(point1, point2, point3)
        fourth_points = []

        if math.isclose(side1, side2, abs_tol=1e-9):
            alt_lng_sl = side1 * DEFAULT_RATIO
            alt_sml_sl = side1 / DEFAULT_RATIO

            out_diagonal = self.get_outer_diagonal(side_length=side1, angle=angle)
            
            # excepts when the DEFAULT_RATIO isn't long enough to bridge the gap (diagonal does not exist)
            try:
                diagonal = self.get_diagonal2(large_side_length=side1, small_side_length=alt_sml_sl, outer_diagonal=out_diagonal)
                sml_angle = self.get_small_angle(top_angle=angle, small_side_length=alt_sml_sl, diagonal=diagonal)
                
                # have:
                #    / \
                # L / t \ L
                #  /     \
                #
                # side1 = side2 --> long side length
                # angle         --> top angle
                fourth_points.append(Geometry.calculate_point_from_angle(sml_angle, point3, point2, alt_sml_sl))
            except:
                # half the angle needed to create a triangle
                alt_small_angle = math.copysign(1, angle) * (math.pi - abs(angle)) / (2 * DEFAULT_RATIO)
                
                big_angle = self.get_big_angle(top_angle=angle, small_angle=alt_small_angle)
                alt_sml_sl = self.get_small_side_length(large_side_length=side1, top_angle=angle, big_angle=big_angle)

                # have:
                #    / \
                # L / t \ L
                #  /     \
                #
                # side1 = side2 --> long side length
                # angle         --> top angle
                fourth_points.append(Geometry.calculate_point_from_angle(alt_small_angle, point3, point2, alt_sml_sl))

            diagonal = self.get_diagonal2(large_side_length=alt_lng_sl, small_side_length=side1, outer_diagonal=out_diagonal)
            top_angle = self.get_top_angle2(outer_angle=angle, ratio=DEFAULT_RATIO)
            sml_angle = self.get_small_angle(top_angle=top_angle, small_side_length=side1, diagonal=diagonal)
            
            # have:
            #    / \
            # I / b'\ I
            #  /     \
            #
            # side1 = side2 --> short side length
            # angle         --> angle opposite of big angle
            fourth_points.append(Geometry.calculate_point_from_angle(sml_angle, point3, point2, alt_lng_sl))
        
        elif side1 > side2:
            ratio = side1 / side2
            
            diagonal = self.get_diagonal(small_side_length=side2, ratio=ratio, small_angle=angle)
            top_angle = self.get_top_angle(small_side_length=side2, diagonal=diagonal, small_angle=angle)
            big_angle = self.get_big_angle(top_angle=top_angle, small_angle=angle)

            # have:
            #    / \
            # L / s \ I
            #  /     
            #
            # side1 --> long side length
            # side2 --> short side length
            # angle --> small angle
            fourth_points.append(Geometry.calculate_point_from_angle(big_angle, point3, point2, side2))

        elif side1 < side2:
            ratio = side2 / side1
            
            diagonal = self.get_diagonal(small_side_length=side1, ratio=ratio, small_angle=angle)
            top_angle = self.get_top_angle(small_side_length=side1, diagonal=diagonal, small_angle=angle)
            big_angle = self.get_big_angle(top_angle=top_angle, small_angle=angle)

            # have:
            #    / \
            # I / s \ L
            #        \
            #
            # side1 --> short side length
            # side2 --> long side length
            # angle --> small angle
            fourth_points.append(Geometry.calculate_point_from_angle(top_angle, point3, point2, side2))
        
        return fourth_points
    
    # gets the angle in degrees between three points
    #  *angle is signed and between (-180, 180) degrees
    #
    # point1 - 2d point | one side of the angle
    # mid_point - 2d point | mid point of the angle
    # point3 - 2d point | other side of the angle
    #
    # returns the angle in degrees
    @staticmethod
    def get_angle(point1, mid_point, point3):
        a = np.array([point1.x, point1.y])
        b = np.array([mid_point.x, mid_point.y])
        c = np.array([point3.x, point3.y])

        ba = a - b
        bc = c - b
        
        angle = np.degrees(math.atan2(ba[0] * bc[1] - ba[1] * bc[0],
                                      ba[0] * bc[0] + ba[1] * bc[1]))

        return angle
    
    # finds the point that the line created by point1 and point2 intersects with
    # a perpendicular line that passes through point3.
    # if point1 == point2 returns point1
    #
    # point1 - 2d point that helps define the line
    # point2 - 2d point that helps define the line
    # point3 - 2d point that the perpendicular line falls under
    #
    # returns the intersect point
    @staticmethod
    def find_intersect(point1, point2, point3):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        x3, y3 = point3.x, point3.y

        px = x2 - x1
        py = y2 - y1
        
        dAB = px * px + py * py
        
        if dAB != 0:
            u = ((x3 - x1) * px + (y3 - y1) * py) / dAB
        else:
            return Point(x1, y1)

        x = x1 + u * px
        y = y1 + u * py

        return Point(x, y)

    # verify the the points compose a dart
    #
    # returns whether or not it composes a dart
    def _verify_dart(self):
        return Dart.are_darts([self._points])

    # verify the the first 3 points can form a dart
    #
    # returns whether or not it can form a dart
    def _verify_dart_3_points(self):
        p1 = self._points[0]
        p2 = self._points[0]
        p3 = self._points[0]
        return Dart.are_dartable([[p1, p2, p3, None]])

    # determins if all of the scenarios are posible to create a dart
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 3 points that could form darts
    @staticmethod
    def are_dartable(scenarios):
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
            
            diagonal = Geometry.distance(point1, point3)
            right = Geometry.distance(point1, intersect_point)
            left = Geometry.distance(intersect_point, point3)
            
            # the intersect must be off of the diagonal or be its midpoint
            if(not math.isclose(right, left, abs_tol=1e-9) and math.isclose(right + left, diagonal, abs_tol=1e-9)):
                return False

        return True
    
    # determins if all of the scenarios are posible are a dart
    # 
    # scenarios - list of lists of points
    # 
    # returns whether the scenarios are 4 points that form darts
    @staticmethod
    def are_darts(scenarios):
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
            if((not math.isclose(right1, left1, abs_tol=1e-9) or (diagonal2 >= right2 and diagonal2 >= left2)) and
               (not math.isclose(right2, left2, abs_tol=1e-9) or (diagonal1 >= right1 and diagonal1 >= left1))):
                return False

        return True
    
    # ------------- Math ------------- #

    # gets the length of the interior diagonal
    #
    # small_side_length - the length of the shorter side
    # ratio - the ratio between the larger and smaller side lengths
    # small_angle(radians) - the angle that there are two of
    #
    # returns the length of the interior diagonal
    def get_diagonal(self, small_side_length, ratio, small_angle):
        return small_side_length * math.sqrt(ratio**2 + 1 - 2 * ratio * math.cos(small_angle))

    # gets the length of the interior diagonal
    #
    # large_side_length - the length of the longer side
    # small_side_length - the length of the shorter side
    # outer_diagonal - the length of the outer diagonal
    #
    # returns the length of the interior diagonal
    def get_diagonal2(self, large_side_length, small_side_length, outer_diagonal):
        return math.sqrt(large_side_length**2 - (outer_diagonal**2 / 4)) - math.sqrt(small_side_length**2 - (outer_diagonal**2 / 4))

    # gets the angle in radians of the top angle
    #
    # small_side_length - the length of the shorter side
    # diagonal - the length of the interior diagonal
    # small_angle(radians) - the angle that there are two of
    #
    # returns the angle in radians of the top angle
    def get_top_angle(self, small_side_length, diagonal, small_angle):
        return 2 * math.asin((small_side_length * math.sin(small_angle)) / diagonal)
    
    # gets the angle in radians of the top angle
    #
    # outer_angle(radians) - the angle opposing the angle that is above 180 degrees
    # ratio - the ratio between the larger and smaller side lengths
    #
    # returns the angle in radians of the top angle
    def get_top_angle2(self, outer_angle, ratio):
        return math.copysign(1, -outer_angle) * math.acos((math.cos(outer_angle) - 1) / ratio**2 + 1)

    # gets the angle in radians of the big angle
    #
    # top_angle(radians) - the angle that there is one of that is less than 180 degrees
    # small_angle(radians) - the angle that there are two of
    #
    # returns the angle in radians of the big angle
    def get_big_angle(self, top_angle, small_angle):
        return 2 * math.pi - top_angle - 2 * small_angle

    # gets the length of the outer diagonal
    #
    # side_length - the length of the the sides the angle is between
    # angle(radians) - the angle between the sides
    #
    # returns the length of the outer diagonal
    def get_outer_diagonal(self, side_length, angle):
        return side_length * math.sqrt(2 - 2 * math.cos(angle))

    # gets the angle in radians of the small angle
    #
    # top_angle(radians) - the angle that there is one of that is less than 180 degrees
    # small_side_length - the length of the shorter side
    # diagonal - the length of the interior diagonal
    #
    # returns the the angle in radians of the small angle
    def get_small_angle(self, top_angle, small_side_length, diagonal):
        return math.asin((diagonal * math.sin(top_angle / 2)) / small_side_length)

    # gets the length of the small side
    # 
    # large_side_length - the length of the longer side
    # top_angle(radians) - the angle that there is one of that is less than 180 degrees
    # big_angle(radians) - the angle that there is one of that is more than 180 degrees
    # 
    # returns the length of the small side
    def get_small_side_length(self, large_side_length, top_angle, big_angle):
        return (large_side_length * math.sin(top_angle / 2) / math.sin(big_angle / 2))