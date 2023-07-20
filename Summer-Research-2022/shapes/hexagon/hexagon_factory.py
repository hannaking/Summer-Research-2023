import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from hexagon.hexagon    import Hexagon

class HexagonFactory:

    def __init__(self):
        self._types = [Hexagon]

    def _empty_types(self):
        self._types = []

    def _include_type(self, type):

        if type == 'RegularHex':
            self._types.append(Hexagon)
            return True

        return False

    def _coordinatize(self, coords):
        scenarios = []
        
        hex = Hexagon(coords)
        scenario = hex.coordinatize()
        scenarios.extend(scenario)

        return scenarios