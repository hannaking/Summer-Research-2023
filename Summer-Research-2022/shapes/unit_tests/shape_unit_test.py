import unittest
import sys
import numpy as np

sys.path.insert(0, './Summer-Research-2022/')

from shapes.triangles.right_triangle import RightTriangle
from shapes.line_segment                  import Segment
from pygeom                          import Axes, Point
from lattice                         import Lattice
from shapes.coordinate               import Coordinate
from shapes.line_segment                  import Segment
from node                            import Node

EDGE_LATTICE_LAYER = 2

class TestShape(unittest.TestCase):
    # def test_init_square(self):
    #     pass
    
#---------------------------init---------------------------------------------
    def test_init_coords_not_a_list(self):
        with self.assertRaises(Exception):
            RightTriangle(0)

#-----------------------find coordinate pairs---------------------------------
    def test_find_coordinate_pairs_two_pairs(self):
        coord1 = Coordinate(0,0)
        coord2 = Coordinate(1,0)
        coords = [coord1, coord2]
        shape = RightTriangle(coords) # the shape doesnt matter

        coord_pairs = shape._find_coordinate_pairs()

        expected = [
            [coord1, coord2],
        ]

        self.assertEqual(len(coord_pairs), 1) # make sure we have one pair
        for i in range(len(coord_pairs)):
            
            self.assertEqual(len(coord_pairs[i]), 2)    # each pair should have two vectors (hence the use of the word "pair")

            self.assertCountEqual(coord_pairs[i], expected[i]) # each pair should have the same pair in expected at the same index (disregarding the order)

    def test_find_coordinate_pairs_three_pairs(self):
        coord1 = Coordinate(0,0)
        coord2 = Coordinate(1,0)
        coord3 = Coordinate(0,1)
        coords = [coord1, coord2, coord3]
        shape = RightTriangle(coords) # the shape doesnt matter
        coord_pairs = shape._find_coordinate_pairs()

        expected = [
            [coord1, coord2],
            [coord1, coord3],
            [coord2, coord3],
        ]

        self.assertEqual(len(coord_pairs), 3) # make sure we have three pairs
        for i in range(len(coord_pairs)):
            
            self.assertEqual(len(coord_pairs[i]), 2)    # each pair should have two vectors (hence the use of the word "pair")

            self.assertCountEqual(coord_pairs[i], expected[i]) # each pair should have the same pair in expected at the same index (disregarding the order)
        
    def test_find_coordinate_pairs_four_pairs(self):
        coord1 = Coordinate(-1,1)
        coord2 = Coordinate(1,1)
        coord3 = Coordinate(-1,-1)
        coord4 = Coordinate(1,-1)
        coords = [coord1, coord2, coord3, coord4]
        shape = RightTriangle(coords) # the shape doesnt matter
        coord_pairs = shape._find_coordinate_pairs()

        expected = [
            [coord1, coord2],
            [coord1, coord3],
            [coord1, coord4],
            [coord2, coord3],
            [coord2, coord4],
            [coord3, coord4],
        ]

        self.assertEqual(len(coord_pairs), 6) # make sure we have six pairs
        for i in range(len(coord_pairs)):
            
            self.assertEqual(len(coord_pairs[i]), 2)    # each pair should have two vectors (hence the use of the word "pair")

            self.assertCountEqual(coord_pairs[i], expected[i]) # each pair should have the same pair in expected at the same index (disregarding the order)
    
 #----------------------------create segment------------------------------
    def test_create_segment_simple(self):
        coord_pair = [Coordinate(0,0), Coordinate(1,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) # shape and init doesnt matter
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(0,0), (1,0), [1,0]]

        self.assertEqual(segment, expected)

    def test_create_segment_simple_swapped(self):
        coord_pair = [Coordinate(1,0), Coordinate(0,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(1,0), (0,0), [-1,0]]

        self.assertEqual(segment, expected)

    def test_create_segment_neg(self):
        coord_pair = [Coordinate(0,0), Coordinate(-1,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(0,0), (-1,0), [-1,0]]

        self.assertEqual(segment, expected)

    def test_create_segment_neg_swapped(self):
        coord_pair = [Coordinate(-1,0), Coordinate(0,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(-1,0), (0,0), [1,0]]

        self.assertEqual(segment, expected)

    def test_create_segment_opposite_neg(self):
        coord_pair = [Coordinate(0,0), Coordinate(-1,-1)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(0,0), (-1,-1), [-1,-1]]

        self.assertEqual(segment, expected)

    def test_create_segment_opposite_neg_swapped(self):
        coord_pair = [Coordinate(-1,-1), Coordinate(0,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(-1,-1), (0,0), [1,1]]

        self.assertEqual(segment, expected)

    def test_create_segment_same_point(self):
        coord_pair = [Coordinate(0,0), Coordinate(0,0)]
        edge = Node(EDGE_LATTICE_LAYER)
        shape = RightTriangle([(0,0)]) 
        segment = shape._create_segment(coord_pair, edge)
        segment = segment.toArr()
        expected = [(0,0), (0,0), [0,0]]

        self.assertEqual(segment, expected)

    #--------------------------create all segments----------------------------
    def test_create_all_segments_one_pair(self):
        coords = [Coordinate(0,0), Coordinate(1,0)]
        shape = RightTriangle(coords) # the shape doesnt matter (there just to instantiate a Shape), but coords do
        segments = shape._create_all_segments()
        
        # turning the segments into array representations so it's easier to write in expected. we only care about contents.
        for i in range(len(segments)):
            segments[i] = segments[i].toArr()

        # a valid segment could be in either direction, so we check both directions
        expected = [
            [(0,0), (1,0), [1,0]]
        ]
        expected_swapped = [ 
            [(1,0), (0,0), [-1,0]]
        ]

        self.assertEqual(len(segments), 1) # we should have found exactly one segment
        for segment in segments: 
            self.assertTrue(segment in expected or segment in expected_swapped)

    def test_create_all_segments_three_pairs(self):
        coords = [(0,0), (1,0), (0,1)]
        shape = RightTriangle(coords) # the shape doesnt matter (there just to instantiate a Shape), but coords do
        segments = shape._create_all_segments()
        
        # turning the segments into array representations so it's easier to write in expected. we only care about contents.
        for i in range(len(segments)):
            segments[i] = segments[i].toArr()

        expected = [
            [(0,0), (1,0), [1,0]],
            [(0,0), (0,1), [0,1]],
            [(0,1), (1,0), [1,-1]]
        ]
        expected_swapped = [ 
            [(1,0), (0,0), [-1,0]],
            [(0,1), (0,0), [0,-1]],
            [(1,0), (0,1), [-1,1]]
        ]

        self.assertEqual(len(segments), 3) # we should have found exactly three segments
        for segment in segments: 
            self.assertTrue(segment in expected or segment in expected_swapped)

    def test_create_all_segments_four_pairs(self):
        coords = [(-1,1), (1,1), (-1,-1), (1,-1)]
        shape = RightTriangle(coords) # the shape doesnt matter (there just to instantiate a Shape), but coords do
        segments = shape._create_all_segments()
        
        # turning the segments into array representations so it's easier to write in expected. we only care about contents.
        for i in range(len(segments)):
            segments[i] = segments[i].toArr()

        expected = [
            [(-1,1), (1,1), [2,0]],
            [(-1,1), (-1,-1), [0,-2]],
            [(-1,1), (1,-1), [2,-2]],
            [(1,1), (-1,-1), [-2,-2]],
            [(1,1), (1,-1), [0,-2]],
            [(-1,-1), (1,-1), [2,0]],
        ]
        expected_swapped = [ 
            [(1,1), (-1,1), [-2,0]],
            [(-1,-1), (-1,1), [0,2]],
            [(1,-1), (-1,1), [-2,2]],
            [(-1,-1), (1,1), [2,2]],
            [(1,-1), (1,1), [0,2]],
            [(1,-1), (-1,-1), [-2,0]],
        ]

        self.assertEqual(len(segments), 6) 
        for segment in segments: 
            print(segment)
            self.assertTrue(segment in expected or segment in expected_swapped)


if __name__ == "__main__":
    unittest.main()