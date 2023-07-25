import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from shapely.geometry import Point
from line_segment.segment import Segment

class TestLineSegment(unittest.TestCase):
    #too many coords, too few coords, 2 coords
    def test_verify_line_segment_too_many_coords(self):
        coords = [Point(0,0), Point(1,0), Point(0,1)]
        shape = Segment(coords)
        self.assertFalse(shape._verify_line_segment())

    def test_verify_line_segment_too_few_coords(self):
        coords = [Point(0,0)]
        shape = Segment(coords)
        self.assertFalse(shape._verify_line_segment())

    def test_verify_line_segment_2_coords(self):
        coords = [Point(0,0), Point(1,0)]
        shape = Segment(coords)
        self.assertTrue(shape._verify_line_segment())

if __name__ == "__main__":
    unittest.main()