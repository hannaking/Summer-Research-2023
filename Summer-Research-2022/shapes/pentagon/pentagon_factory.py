import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from pentagon.pentagon    import Pentagon

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