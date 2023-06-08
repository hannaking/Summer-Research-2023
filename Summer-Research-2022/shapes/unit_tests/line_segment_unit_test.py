import unittest
import sys

sys.path.insert(0, 'C:/Users/hgkin/OneDrive/Documents/GitHub/Summer-Research-2023/Summer-Research-2022/')

from shapes.line_segment import LineSegment

class TestLineSegment(unittest.TestCase):
    #too many coords, too few coords, 2 coords
    def test_verify_line_segment_too_many_coords(self):
        coords = [(0,0), (1,0), (0,1)]
        shape = LineSegment(coords)
        self.assertFalse(shape._verify_line_segment())

    def test_verify_line_segment_too_few_coords(self):
        coords = [(0,0)]
        shape = LineSegment(coords)
        self.assertFalse(shape._verify_line_segment())

    def test_verify_line_segment_2_coords(self):
        coords = [(0,0), (1,0)]
        shape = LineSegment(coords)
        self.assertTrue(shape._verify_line_segment())

if __name__ == "__main__":
    unittest.main()