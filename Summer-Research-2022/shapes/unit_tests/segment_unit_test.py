import unittest
import sys
import numpy as np

sys.path.insert(0, './Summer-Research-2022/')

from shapes.segment                  import Segment
from shapes.coordinate               import Coordinate
from shapes.segment                  import Segment
from shapes.vector                   import Vector
from node import Node

class TestSegment(unittest.TestCase):
    #-----------------------------init------------------------------------
    def test_init_coord1_not_coordinate(self):
        with self.assertRaises(TypeError):
            segment = Segment(0, Coordinate(1,1))

    def test_init_coord2_not_coordinate(self):
        with self.assertRaises(TypeError):
            segment = Segment(Coordinate(1,1), 0)

    def test_init_edge_not_node(self):
        with self.assertRaises(TypeError):
            segment = Segment(Coordinate(0,0), Coordinate(1,1), "not a node")

    def test_init_edge_not_on_edge_layer(self):
        with self.assertRaises(ValueError):
            segment = Segment(Coordinate(0,0), Coordinate(1,1), Node(0))

#-----------------------calculate slope----------------------------------------

    def test_calculate_slope_1(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,1))
        self.assertEqual(segment._slope, 1)

    def test_calculate_slope_0(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,0))
        self.assertEqual(segment._slope, 0)

    def test_calculate_slope_none(self):
        segment = Segment(Coordinate(0,0), Coordinate(0,1))
        self.assertEqual(segment._slope, None)
        
#-------------------------calculate length-----------------------------------------

    def test_calculate_length_horizontal(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,0))
        self.assertEqual(segment.calculate_length(), 1)

    def test_calculate_length_horizontal_swapped(self):
        segment = Segment(Coordinate(1,0), Coordinate(0,0))
        self.assertEqual(segment.calculate_length(), 1)

    def test_calculate_length_vertical(self):
        segment = Segment(Coordinate(0,0), Coordinate(0,1))
        self.assertEqual(segment.calculate_length(), 1)

    def test_calculate_length_vertical_swapped(self):
        segment = Segment(Coordinate(0,1), Coordinate(0,0))
        self.assertEqual(segment.calculate_length(), 1)

    def test_calculate_length_diagonal(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,1))
        self.assertEqual(segment.calculate_length(), 1)

    def test_calculate_length_diagonal_swapped(self):
        segment = Segment(Coordinate(1,1), Coordinate(0,0))
        self.assertEqual(segment.calculate_length(), 1)

#------------------------calculate vector-----------------------------------------------

    def test_calculate_vector_quadrant_1(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,1))
        vector = segment.calculate_vector()
        expected = [1,1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_1_swapped(self):
        segment = Segment(Coordinate(1,1), Coordinate(0,0))
        vector = segment.calculate_vector()
        expected = [-1,-1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_2(self):
        segment = Segment(Coordinate(0,0), Coordinate(-1,1))
        vector = segment.calculate_vector()
        expected = [-1,1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_2_swapped(self):
        segment = Segment(Coordinate(-1,1), Coordinate(0,0))
        vector = segment.calculate_vector()
        expected = [1,-1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_3(self):
        segment = Segment(Coordinate(0,0), Coordinate(-1,-1))
        vector = segment.calculate_vector()
        expected = [-1,-1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_3_swapped(self):
        segment = Segment(Coordinate(-1,-1), Coordinate(0,0))
        vector = segment.calculate_vector()
        expected = [1,1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_4(self):
        segment = Segment(Coordinate(0,0), Coordinate(1,-1))
        vector = segment.calculate_vector()
        expected = [1,-1]
        self.assertEqual(vector, expected)

    def test_calculate_vector_quadrant_4_swapped(self):
        segment = Segment(Coordinate(1,-1), Coordinate(0,0))
        vector = segment.calculate_vector()
        expected = [-1,1]
        self.assertEqual(vector, expected)
#------------------------intersects--------------------------------------------
    # intersects in middle
    # meets at an endpoint
    # does not intersect (parallel)
    # does not intersect in range but would
    # same segment
    def test_intersects_middle(self):
        segment1 = Segment(Coordinate(0,0), Coordinate(1,1))
        segment2 = Segment(Coordinate(1,0), Coordinate(0,1))
        self.assertTrue(Segment.intersects(segment1, segment2))

    def test_intersects_endpoint(self):
        segment1 = Segment(Coordinate(0,0), Coordinate(1,1))
        segment2 = Segment(Coordinate(1,1), Coordinate(2,0))
        self.assertTrue(Segment.intersects(segment1, segment2))

    def test_intersects_parallel(self):
        segment1 = Segment(Coordinate(0,0), Coordinate(1,1))
        segment2 = Segment(Coordinate(0,1), Coordinate(1,2))
        self.assertFalse(Segment.intersects(segment1, segment2))

    def test_intersects_out_of_range(self):
        segment1 = Segment(Coordinate(0,0), Coordinate(1,1))
        segment2 = Segment(Coordinate(1,3), Coordinate(3,1))
        self.assertFalse(Segment.intersects(segment1, segment2))

    def test_intersects_same_segment(self):
        segment1 = Segment(Coordinate(0,0), Coordinate(1,1))
        segment2 = Segment(Coordinate(0,0), Coordinate(1,1))
        self.assertTrue(Segment.intersects(segment1, segment2))

if __name__ == "__main__":
    unittest.main()