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

    def _coordinatize(self, coords, lattice):
        
        scenarios = []
        for segment_type in self._types:

            segment = segment_type(coords)

            scenario = segment.coordinatize(lattice)
            scenarios.extend(scenario)

        return scenarios
            