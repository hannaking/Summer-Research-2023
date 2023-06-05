import sys
sys.path.insert(0, 'C:/Users/lilyb/Desktop/College Stuff/Summer Research (2022)/Summer-Research-2022-displaying-geometry-figures')

from shapes.quadrilaterals.square    import Square

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
    
            return False

    def _coordinatize(self, coords):
        scenarios = []
        for quadrilateral_type in self._types:

            quad = quadrilateral_type(coords)
            scenario = quad.coordinatize()
            scenarios.extend(scenario)

        return scenarios