import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import math
from shapely.geometry import *
from shapes.vector import Vector

DEFAULT_SIDE_LENGTH = 1

class Geometry():

    # rotates a scenario about the origin (0,0) given an angle (must be in radians!).
    # for each point in the scenario, it finds new_x and new_y.
    # new_x = xcosθ + ysinθ
    # new_y = ycosθ – xsinθ
    @staticmethod
    def rotate(scenario, angle):
        if not isinstance(scenario, list):
            raise TypeError("scenario must be a list")
        if not isinstance(angle, float):
            raise TypeError("angle must be a float")

        point1 = scenario[0]
        scenario_at_origin = Geometry.move_scenario_to_origin(scenario)

        new_scenario = [None] * len(scenario_at_origin)
        for i, point in enumerate(scenario_at_origin):
            new_x = point.x * math.cos(angle) + point.y * math.sin(angle)
            new_y = point.y * math.cos(angle) - point.x * math.sin(angle)
            new_scenario[i] = Point(new_x, new_y)

        new_scenario = Geometry.move_scenario_back(new_scenario, point1)
            
        return new_scenario

    # takes all Points in a scenario and moves all points OTHER than point 1 by point 1's x and y.
    # then, sets point 1 to 0,0.
    # if point 1 is already 0,0, then it does nothing, and returns the scenario unchanged.
    @staticmethod
    def move_scenario_to_origin(scenario):
        if not isinstance(scenario, list):
            raise TypeError("scenario must be a list")

        point1 = scenario[0]

        # no need to make changes if point1 is already at 0,0
        if point1.x == 0 and point1.y == 0:
            return scenario

        new_scenario = [point1]
        # move all other points (not point 1) by point 1's x and y
        for i in range(1, len(scenario)):
            new_x = scenario[i].x - point1.x
            new_y = scenario[i].y - point1.y
            new_scenario.append(Point(new_x, new_y))

        # finally, set point 1 to 0,0
        new_scenario[0] = Point(0,0)

        return new_scenario

    # takes all Points in a scenario and adds back the offset from the origin, given the original start point.
    # if the original point 1 was already at 0,0, then it does nothing, and returns the scenario unchanged.
    @staticmethod
    def move_scenario_back(scenario, original_point1):
        if not isinstance(scenario, list):
            raise TypeError("scenario must be a list")
        if not isinstance(original_point1, Point):
            raise TypeError("original_point1 must be a Point")

        if original_point1.x == 0 and original_point1.y == 0:
            return scenario

        new_scenario = [original_point1]
        for i in range(1, len(scenario)):
            new_x = scenario[i].x + original_point1.x
            new_y = scenario[i].y + original_point1.y
            new_scenario.append(Point(new_x, new_y))

        return new_scenario

    # returns the distance between two given Point objects.
    @staticmethod
    def distance(point1, point2):
        if not isinstance(point1, Point):
            raise TypeError("point1 must be a Point object")
        if not isinstance(point2, Point):
            raise TypeError("point2 must be a Point object")

        distance = math.sqrt( (point2.x - point1.x)**2 + (point2.y - point1.y)**2 )
        return distance

    # calculates all coordinates from the segment formed by the start and end point
    # from angles (in radians): 0, 30, 45, 60, 90, 180, -30, -45, -60, -90
    @staticmethod
    def calculate_all_points(start_point, end_point, magnitude):
        angles = [
            math.radians(0),
            math.radians(30),
            math.radians(45),
            math.radians(60),
            math.radians(90),
            math.radians(180),
            math.radians(-30),
            math.radians(-45),
            math.radians(-60),
            math.radians(-90)
        ]
        points = []
        for angle in angles:
            new_point = Geometry.calculate_point_from_angle(angle, start_point, end_point, magnitude)
            points.append(new_point)

        return points

    #* calculate_point_from_angle
    #@ comments need updating
    # given an angle and ref endpoint, find a point that is the given angle from the segment formed by the start point and ref endpoint.
    # param given_angle = either pi/6, pi/4, pi/3, pi/2, or pi (aka 30, 45, 60, 90, or 180 degrees... but in radians)
    # param ref_endpoint = a Point object that is connected to the start vertex. we use it as our reference to know at what angle to put the next vertex.
    # param magnitude = the distance between the start point and the point you want to find
    # returns a Point object that is the new point
    #
    # first, we must find the reference angle.
    # the reference angle is the angle between the vector version of the ref segment (the ref vector) and the x axis.
    # then, we find a goal angle, which is simply the sum of the reference angle and the given angle.
    # then, we find the new point by finding the vector that 
    # then, this new vector is used to find the coordinates we want, but they're in standard position.
    # we add the start coordinates to these coordinates to get the final coordinates.
    # --------------------------------------------------
    # * what are we finding? *
    #  vertex we want -> * 
    #                   /  
    #                  /   
    #                 /   <- given angle
    # start vertex ->/___________
    #                   ^ ref segment
    # --------------------------------------------------
    # * what is the reference angle? *
    #                   /   <- goal angle                
    # ref segment ->   /    <- ref angle
    #                 /__________
    #          ^ x-axis
    # --------------------------------------------------
    # * what is the goal angle? *
    # y-axis
    # |
    # |  / <- vector we want to find
    # | /                                * given angle = the angle in radians between the vector we want to find and the ref vector (in this image, given angle is positive)
    # |/                                 * ref angle = the angle between the ref vector and the x axis  (in this image, reg angle is negative)                               
    # |---------> x-axis                 ! goal angle = the angle between the vector we want to find and the x axis (in this image, goal angle is positive)
    # |\                                              
    # | \                                the goal angle is the sum between given angle and ref angle   
    # |  \ <- ref vector                 (goal angle = given angle + ref angle)
    # --------------------------------------------------
    #? problem for later: we need to be able to shorten the coordinate if it will intersect with another segment in the figure 
    #? will be inside _find_magnitude()
    @staticmethod
    def calculate_point_from_angle(given_angle, start_point, ref_endpoint, magnitude=DEFAULT_SIDE_LENGTH):

        if not isinstance(given_angle, float):
            raise Exception("given_angle must be a float")

        if not isinstance(ref_endpoint, Point):
            raise Exception("ref_endpoint must be a Point object")

        # 1. find ref angle
        ref_angle = Geometry._find_reference_angle(ref_endpoint, start_point)

        # 2. find "goal" angle
        goal_angle = Geometry._find_goal_angle(given_angle, ref_angle)

        # 3. find magnitude
        magnitude = Geometry._find_magnitude(magnitude) #? will this need more arguments?

        # 4. find vector
        new_vector = Geometry._find_vector(magnitude, goal_angle)

        # 5. find new coord
        new_point = Geometry._find_new_point(new_vector, start_point)

        return new_point

    # helper method for calculate_coord_from_angle 
    # finds the reference angle. step 1 of the algorithm.
    # param ref_endpoint: the endpoint of the reference segment
    # param start_point: the start point of the reference segment
    # returns the reference angle of the ref segment, in radians.
    #
    # the method first gets the vector formed by the start point to the end point.
    # then, it gets the angle between this vector and the x axis (the reference angle).
    # it then returns this angle.
    @staticmethod
    def _find_reference_angle(ref_endpoint, start_coord):
        initial = start_coord
        terminal = ref_endpoint
    
        ref_vector = Vector(terminal.x - initial.x, terminal.y - initial.y)

        # get the angle of the reference vector
        ref_angle = ref_vector.calculate_reference_angle()
        return ref_angle

    # helper method for calculate_coord_from_angle. step 2 of the algorithm.
    # finds the goal angle using the given angle and the reference angle
    # background info: a reference angle is the angle of the reference segment from the x-axis.
    # the given angle is the angle we want to use to find the next vertex. 
    # the given angle is counterclockwise from the reference angle.
    # now, we are not creating any vectors in this method, but for a mental image,
    # imagine a vector formed by the given angle and the start point. we want to find the angle between this vector and the x-axis.
    # 
    # ∧   / <- imaginary vector
    # |  /  
    # | /
    # |/| <- goal angle              given angle = angle btwn imaginary vector and ref segment
    # |--------------------->        goal angle = ref angle + given angle
    # |\| <- reference angle         (ref angle is negative, given angle is positive, so we get this difference as the goal angle)
    # | \
    # |  \ 
    # V   \
    #     ^ ref segment
    @staticmethod
    def _find_goal_angle(given_angle, ref_angle):
        if ref_angle == 0: 
            return given_angle # when the ref angle is 0, given angle will be the goal angle 
        else:
            return ref_angle + given_angle

    # helper method for calculate_coord_from_angle. step 3 of the algorithm.
    # finds the magnitude of the vector that will be between the start vertex and the coordinate we want to find.
    # by default, it is DEFAULT_SIDE_LENGTH (which is 1). but if that is too long (i.e. it will intersect another part of what is already on the plane),
    # it will be reduced until it is not. #* this still needs to be implemented
    #? will this need more parameters?
    @staticmethod
    def _find_magnitude(magnitude): #@ does not need a test until the TODO is implemented
        return magnitude
        #TODO: magnitude should by default be input magnitude, but change dynamically if it must be shorter than 1 in order to not intersect with anything else

    # helper method for calculate_coord_from_angle. step 4 of the algorithm.
    @staticmethod
    def _find_vector(magnitude, goal_angle):
        return Vector(magnitude * math.cos(goal_angle), magnitude * math.sin(goal_angle))

    # helper method for calculate_coord_from_angle. step 5 of the algorithm.
    # param vector: the vector that has the components that need to be offset
    # param start_coord: the coordinate that the vector will be offset from
    # finds the new coordinate by adding the start point's coordinates to the vector components.
    @staticmethod
    def _find_new_point(vector, start_point):  
        #   - now, we compute the offset by adding the start coordinates to the new vector's components
        new_x = vector.x + start_point.x
        new_y = vector.y + start_point.y

        #   - create new coordinate
        new_point = Point(new_x, new_y)
        return new_point

    # if you start with one point, you need to get every other point for the possible angles (30, 45, 60...).
    # this is what get_second_points accomplishes. 
    # it returns a list of Points that are the second points for the given first point.
    # it uses calculate_all_points as a helper method, which gives us these Points.
    # it does this by using a placeholder point that is 1 unit to the right of the first point. 
    # this point is used as a reference inside calculate_all_points to know where the angle is supposed to go.
    @staticmethod
    def get_second_points(jump_point): #@ fully tested
        # uses two points, so make a placeholder one straight out to the right if no one already exists
        # (it won't because if you are here you only have one point)
        # you need a placeholder to calculate angles off of when starting from a single point and not a side
        placeholder = Point(jump_point.x + 1, jump_point.y) 
        return Geometry.calculate_all_points(jump_point, placeholder, DEFAULT_SIDE_LENGTH)