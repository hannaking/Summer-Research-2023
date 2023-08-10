# manages septagon construction
# only regular septagons are supported, so only one type of septagon is possible
#
# septagon sounds better than heptagon so they are called septagons. it's the same shape.

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

    # determines which types of septagons are to be constructed
    # septagons can only be regular septagons
    #
    # type - string type of Septagon to be included
    #
    # return True if type is 'RegularSept', otherwise False
    def _include_type(self, type):

        if type == 'RegularSept':
            self._types.append(Septagon)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the septagon
    #
    # returns a list of lists of Points, each a valid and complete septagon
    def _coordinatize(self, coords):
        scenarios = []
        
        sept = Septagon(coords)
        scenario = sept.coordinatize()
        scenarios.extend(scenario)

        return scenarios