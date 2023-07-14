import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from triangles.equilateral               import Equilateral
from triangles.isosceles_right           import IsoscelesRight
from triangles.non_isosceles_right       import NonIsoscelesRight
from triangles.isosceles                 import Isosceles

#TODO remeber to add back all other triangle types
# TriangleFactory class 
class TriangleFactory:

    def __init__(self):
        self._types = [Equilateral, IsoscelesRight, NonIsoscelesRight, Isosceles]

    def _empty_types(self):
        self._types = []

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

    def _coordinatize(self, coords):
        
        scenarios = []
        for triangle_type in self._types:

            triangle = triangle_type(coords)

            scenario = triangle.coordinatize()
            scenarios.extend(scenario)

        return scenarios
            