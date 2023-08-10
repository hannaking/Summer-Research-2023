# manages triangle construction
# 4 types of triangles are supported:
# Equilateral    Isosceles Right     Isosceles     Non-Isosceles Right
#                  (45-45-90)                          (30-60-90)

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from triangles.equilateral               import Equilateral
from triangles.isosceles_right           import IsoscelesRight
from triangles.non_isosceles_right       import NonIsoscelesRight
from triangles.isosceles                 import Isosceles

class TriangleFactory:

    def __init__(self):
        self._types = [Equilateral, IsoscelesRight, NonIsoscelesRight, Isosceles]

    def _empty_types(self):
        self._types = []

    # determines which types of triangles are to be constructed
    # 4 types: Equilateral, IsoscelesRight, NonIsoscelesRight, Isosceles
    #
    # type - string type of Triangle to be included
    #
    # return True if type is a valid triangle type, otherwise False
    def _include_type(self, type):

        if type == 'Equilateral':
            self._types.append(Equilateral)
            return True

        elif type == 'IsoscelesRight':
            self._types.append(IsoscelesRight)
            return True

        elif type == 'NonIsoscelesRight':
            self._types.append(NonIsoscelesRight)
            return True
        
        elif type == 'Isosceles':
            self._types.append(Isosceles)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the triangle
    #
    # returns a list of lists of Points, each a valid and complete triangle
    def _coordinatize(self, coords):
        
        scenarios = []
        for triangle_type in self._types:

            triangle = triangle_type(coords)

            scenario = triangle.coordinatize()
            scenarios.extend(scenario)

        return scenarios
            