import math
import sys
import shapely as sh

sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapely.geometry import *
from shapes.geometry import Geometry
from shapes.vector import Vector

ANGLE           = math.radians(72)
TO_CENTER_ANGLE = math.radians(54)
RAY             = 0.8507 #math.sqrt((5 + math.sqrt(5))/10) #1 / (2 * math.sin(math.radians(36)))

# 5 sides of equal length, all angles are 108 degrees

class Pentagon(): 
    # take a list of 1-5 Points, the unknown Points being None
    # known information about the starting position of the pentagon
    def __init__(self, known_coords):
        self._points = known_coords

    # Get Points to make up the Pentagon
    #
    # returns a list of lists of Points, each list is one possible coordinatization of the pentagon
    def coordinatize(self):
        scenarios = [] # list of lists of Points

        # start with anywhere from 1 to 5 points
        # if all Points are given (5 points), just return that one scenario
        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        # I need to sort the coords, dragging along a list of indices.
        first_sort = [ b for b in sorted(enumerate(self._points), key=lambda e: e[1] is None ) ]

        # this gets a sorted points list
        sorted_points = [b[1] for b in first_sort]

        second_points = [sorted_points[1]]

        # get all possible next point for the given single point
        if (sorted_points[1] == None): # one known point
            print("one known point")
            second_points = []
            # 10 possible second points
            second_points.extend(Geometry.get_second_points(sorted_points[0]))
            for point in second_points:
                # the center will be stored in the final position
                # it will be removed later
                scenarios.append([sorted_points[0], point, None, None, None, None])

        # now have at least 2 points, so side length can be determined
        # fine to be second_points[0] because there will be Points in there
        side_length = Geometry.distance(sorted_points[0], second_points[0])
        print(side_length)

        # now that I have side_length, calculate the center for every scenario
        # each will have 2 possible centers (up and down)
        temp = []
        for scenario in scenarios:
            temp.append([scenario[0], scenario[1], None, None, None,
                         Geometry.calculate_point_from_angle(TO_CENTER_ANGLE, scenario[0], scenario[1], RAY * side_length)])
            temp.append([scenario[0], scenario[1], None, None, None,
                         Geometry.calculate_point_from_angle(-TO_CENTER_ANGLE, scenario[0], scenario[1], RAY * side_length)])
        scenarios = temp
        print(scenarios)
        print()
        
        i = 1
        # so I can alternate for upper center / lower center
        track = 0

        # fill remaining points
        # will rewrite point 2, but it should be the same values (?)
        for scenario in scenarios:
            if scenario[2] == None: i = 1
            elif scenario[3] == None: i = 2
            elif scenario[4] == None: i = 3
            print(scenario[5])
            print(scenario)
            while i < 4:                                                   # center
                if track == 0:
                    scenario[i+1] = Geometry.calculate_point_from_angle(ANGLE, scenario[5], scenario[i], side_length)
                else: 
                    scenario[i+1] = Geometry.calculate_point_from_angle(0-ANGLE, scenario[5], scenario[i], side_length)
                i = i + 1
            track = 0 if track == 1 else 1
            print(scenario)
            print()
            

        # all five points known handled above

        # get rid of the center points
        for scenario in scenarios:
            scenario = scenario[0:4]

        # unsort all scenarios
        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        # a list of lists of 5 Points
        return scenarios