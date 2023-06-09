import unittest
import sys

sys.path.insert(0, './Summer-Research-2022/')

from facegraphgenerator import FaceGraphGenerator
from lattice import Lattice

class unitTest(unittest.TestCase):
    # single shape lattice
    # edge glue
    # vertex glue
    # fill gap
    # anything larger, probably a few
    # 3+ shapes
    def test_build_single_segment(self):
        segment = Lattice(2)
        gen = FaceGraphGenerator()
        
        graph = gen.build(segment, [1], ("Segment"))

        self.assertEqual(len(graph.nodes), 1)
        self.assertTrue(graph.has_node(0))
        self.assertEquals(graph.get_node_attributes(0, "size"), 1)
        self.assertEquals(graph.get_node_attributes(0, "type"), "Segment")
        self.assertEquals(len(graph.edges), 0)
    
    if __name__ == "__main__":
        unittest.main()
