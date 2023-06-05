import sys
sys.path.insert(0, 'C:/dev/Summer Research 2022/')

from shapes.line_segment.segment import Segment

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
            