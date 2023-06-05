import sys
sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapes.triangles.equilateral               import Equilateral
from shapes.triangles.isosceles_right           import IsoscelesRight
from shapes.triangles.non_isosceles_right       import NonIsoscelesRight

#TODO remeber to add back all other triangle types
# TriangleFactory class 
class TriangleFactory:

    def __init__(self):
        self._types = [Equilateral, IsoscelesRight, NonIsoscelesRight]

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

        return False

    def _coordinatize(self, coords):
        
        scenarios = []
        for triangle_type in self._types:

            triangle = triangle_type(coords)

            scenario = triangle.coordinatize()
            scenarios.extend(scenario)

        return scenarios
            