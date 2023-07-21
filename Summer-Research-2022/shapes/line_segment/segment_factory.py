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

    def _include_type(self, type):

        if type == 'Segment':
            self._types.append(Segment)
            return True

        return False

    def _coordinatize(self, coords):
        
        scenarios = []
        for segment_type in self._types:

            segment = segment_type(coords)

            scenario = segment.coordinatize()
            scenarios.extend(scenario)

        return scenarios
            