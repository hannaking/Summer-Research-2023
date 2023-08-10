# manages hexagon construction
# only regular hexagons are supported, so only one type of hexagon is possible

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

    # determines which types of hexagons are to be constructed
    # hexagons can only be regular hexagons
    #
    # type - string type of Hexagon to be included
    #
    # return True if type is 'RegularHex', otherwise False
    def _include_type(self, type):

        if type == 'RegularHex':
            self._types.append(Hexagon)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the hexagon
    #
    # returns a list of lists of Points, each a valid and complete hexagon
    def _coordinatize(self, coords):
        scenarios = []
        
        hex = Hexagon(coords)
        scenario = hex.coordinatize()
        scenarios.extend(scenario)

        return scenarios