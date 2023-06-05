import sys
sys.path.insert(0, 'C:/Users/lilyb/Desktop/College Stuff/Summer Research (2022)/Summer-Research-2022-displaying-geometry-figures')

from shapes.pentagon.pentagon    import Pentagon

class PentagonFactory:

    def __init__(self):
        self._types = [Pentagon]

    def _coordinatize(self, coords):
        scenarios = []
        for quadrilateral_type in self._types:

            quad = quadrilateral_type(coords)
            scenario = quad.coordinatize()
            scenarios.extend(scenario)

        return scenarios