import sys
sys.path.insert(0, 'C:/Users/lilyb/Desktop/College Stuff/Summer Research (2022)/Summer-Research-2022-displaying-geometry-figures')

from shapes.pentagon.pentagon    import Pentagon

class PentagonFactory:

    def __init__(self):
        self._types = [Pentagon]

    def _empty_types(self):
        self._types = []

    def _include_type(self, type):

        if type == 'RegularPent':
            self._types.append(Pentagon)
            return True

        return False

    def _coordinatize(self, coords):
        scenarios = []
        
        pent = Pentagon(coords)
        scenario = pent.coordinatize()
        scenarios.extend(scenario)

        return scenarios