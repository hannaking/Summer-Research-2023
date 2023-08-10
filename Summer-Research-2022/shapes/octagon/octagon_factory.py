# manages octagon construction
# only regular octagons are supported, so only one type of octagon is possible

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

    # determines which types of octagons are to be constructed
    # octagons can only be regular octagons
    #
    # type - string type of Octagon to be included
    #
    # return True if type is 'RegularOct', otherwise False
    def _include_type(self, type):

        if type == 'RegularOct':
            self._types.append(Octagon)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the octagon
    #
    # returns a list of lists of Points, each a valid and complete octagon
    def _coordinatize(self, coords):
        scenarios = []
        
        octa = Octagon(coords)
        scenario = octa.coordinatize()
        scenarios.extend(scenario)

        return scenarios