import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from septagon.septagon    import Septagon

class SeptagonFactory:

    def __init__(self):
        self._types = [Septagon]

    def _empty_types(self):
        self._types = []

    def _include_type(self, type):

        if type == 'RegularSept':
            self._types.append(Septagon)
            return True

        return False

    def _coordinatize(self, coords):
        scenarios = []
        
        sept = Septagon(coords)
        scenario = sept.coordinatize()
        scenarios.extend(scenario)

        return scenarios