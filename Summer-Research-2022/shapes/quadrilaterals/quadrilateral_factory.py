import sys
sys.path.insert(0, 'C:/dev/Summer Research 2022/')
from shapes.quadrilaterals.square    import Square
from shapes.quadrilaterals.rectangle import Rectangle
from shapes.quadrilaterals.kite import Kite
from shapes.quadrilaterals.isotrapezoid import IsoTrapezoid

# QuadrilateralFactory class 
class QuadrilateralFactory:

    def __init__(self):
        self._types = [Square]

    def _empty_types(self):
        self._types = []

    def _include_type(self, type):
            
            if type == 'Square':
                self._types.append(Square)
                return True

            if type == 'Rectangle':
                self._types.append(Rectangle)
                return True

            if type == 'Kite':
                self._types.append(Kite)
                return True

            if type == 'IsoTrapezoid':
                self._types.append(IsoTrapezoid)
                return True
    
            return False

    def _coordinatize(self, coords):
        scenarios = []
        for quadrilateral_type in self._types:

            quad = quadrilateral_type(coords)
            scenario = quad.coordinatize()
            scenarios.extend(scenario)

        return scenarios