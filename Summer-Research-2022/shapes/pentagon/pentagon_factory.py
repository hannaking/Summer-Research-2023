# manages pentagon construction
# only regular pentagons are supported, so only one type of pentagon is possible

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

    # determines which types of pentagons are to be constructed
    # pentagons can only be regular pentagons
    #
    # type - string type of Pentagon to be included
    #
    # return True if type is 'RegularPent', otherwise False
    def _include_type(self, type):

        if type == 'RegularPent':
            self._types.append(Pentagon)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the pentagon
    #
    # returns a list of lists of Points, each a valid and complete pentagon
    def _coordinatize(self, coords):
        scenarios = []
        
        pent = Pentagon(coords)
        scenario = pent.coordinatize()
        scenarios.extend(scenario)

        return scenarios