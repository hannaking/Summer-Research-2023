import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from octagon.octagon    import Octagon

class OctagonFactory:

    def __init__(self):
        self._types = [Octagon]

    def _empty_types(self):
        self._types = []

    def _include_type(self, type):

        if type == 'RegularOct':
            self._types.append(Octagon)
            return True

        return False

    def _coordinatize(self, coords):
        scenarios = []
        
        octa = Octagon(coords)
        scenario = octa.coordinatize()
        scenarios.extend(scenario)

        return scenarios