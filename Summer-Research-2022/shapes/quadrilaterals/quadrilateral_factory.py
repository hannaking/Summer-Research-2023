# manages quadrilateral construction
# 8 types of quadrilaterals are supported:
#   Square
#   Rectangle               (side ratio defaults to 1:2)
#   Rhombus
#   Parallelogram
#   Kite
#   Right Trapezoid         (triangle side is a 45-45-90)
#   Isosceles Trapezoid     (top and both sides are equal. a three-sides-equal trapezoid.)
#   Dart

import sys
sys.path.insert(0, 'C:/dev/Summer Research 2022/')
from shapes.quadrilaterals.square import Square
from shapes.quadrilaterals.rectangle import Rectangle
from shapes.quadrilaterals.Rhombus import Rhombus
from shapes.quadrilaterals.parallelogram import Parallelogram
from shapes.quadrilaterals.kite import Kite
from shapes.quadrilaterals.righttrapezoid import RightTrapezoid
from shapes.quadrilaterals.isotrapezoid import IsoTrapezoid
from shapes.quadrilaterals.dart import Dart

class QuadrilateralFactory:

    def __init__(self):
        self._types = [Square, Rectangle, Rhombus, Parallelogram, Kite, RightTrapezoid, IsoTrapezoid, Dart]

    def _empty_types(self):
        self._types = []
    # determines which types of quadrialterals are to be constructed
    #
    # type - string type of Quadrilateral to be included
    #
    # return True if type is an accepted type, otherwise False
    def _include_type(self, type):
            
            if type == 'Square':
                self._types.append(Square)
                return True

            if type == 'Rectangle':
                self._types.append(Rectangle)
                return True

            if type == 'Rhombus':
               self._types.append(Rhombus)
               return True

            if type == 'Parallelogram':
                self._types.append(Parallelogram)
                return True

            if type == 'Kite':
                self._types.append(Kite)
                return True
            
            if type == 'RightTrapezoid':
                self._types.append(RightTrapezoid)
                return True

            if type == 'IsoTrapezoid':
                self._types.append(IsoTrapezoid)
                return True
            
            if type == 'Dart':
                self._types.append(Dart)
                return True
    
            return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the quadrilateral
    #
    # returns a list of lists of Points, each a valid and complete quadrilateral
    def _coordinatize(self, coords):
        scenarios = []
        for quadrilateral_type in self._types:

            quad = quadrilateral_type(coords)
            scenario = quad.coordinatize()
            scenarios.extend(scenario)

        return scenarios