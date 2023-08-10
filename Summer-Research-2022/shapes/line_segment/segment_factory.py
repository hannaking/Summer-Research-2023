# manages line segment construction
# only one type of line segment ('Segment') is possible

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from line_segment.segment import Segment

# SegmentFactory class 
class SegmentFactory:

    def __init__(self):
        self._types = [Segment]

    def _empty_types(self):
        self._types = []

    # determines which types of line segments are to be constructed
    # there is only one type of line segment
    #
    # type - string type of Segment to be included
    #
    # return True if type is 'Segment', otherwise False
    def _include_type(self, type):

        if type == 'Segment':
            self._types.append(Segment)
            return True

        return False

    # get all possible scenarios based on the given coords
    #
    # coords - known point(s) involved in the segment
    #
    # returns a list of lists of Points, each a valid and complete segment
    def _coordinatize(self, coords):
        
        scenarios = []
        for segment_type in self._types:

            segment = segment_type(coords)

            scenario = segment.coordinatize()
            scenarios.extend(scenario)

        return scenarios
            