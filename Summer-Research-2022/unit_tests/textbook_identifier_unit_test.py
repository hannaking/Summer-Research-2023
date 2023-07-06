import sys
import unittest
import networkx as nx

sys.path.insert(0, './Summer-Research-2022/')

from lattice import Lattice
from lattice_generator import LatticeGenerator
from face_graphs.face_graph_generator import FaceGraphGenerator

from textbook_identifier import TextbookIdentifier

class TestToStellarGraph(unittest.TestCase):
    
    def test_identify(self):
        input_shape_list = [0, 1, 1, 0, 0, 0, 0]
        lattice_generator = LatticeGenerator(input_shape_list)
        lattices = lattice_generator.glue_shapes()._lattice_matrix
        face_graphs = FaceGraphGenerator.from_lattices(lattices)
        
        results = TextbookIdentifier.identify(face_graphs, "model__1")
        
        self.assertEqual(type(results), list)
        for group in results:
            self.assertEqual(type(group), list)
            for result in group:
                self.assertEqual(type(result), bool)

    def test_identify_group(self):
        input_shape_list = [0, 1, 0, 0, 0, 0, 0]
        lattice_generator = LatticeGenerator(input_shape_list)
        lattices = lattice_generator.glue_shapes()._lattice_matrix
        face_graphs = FaceGraphGenerator.from_lattices(lattices)[0]

        results = TextbookIdentifier.identify_group(face_graphs, "model__1")
        
        self.assertEqual(type(results), list)
        for result in results:
            self.assertEqual(type(result), bool)


    def test_identify_graph(self):
        g = nx.MultiGraph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        nx.set_node_attributes(g, {'A' : [23, 4], 'B' : [23, 4], 'C' : [23, 4]}, 'default')

        result = TextbookIdentifier.identify_graph(g, "model__1")
        
        self.assertEqual(type(result), bool)
    
    def test_get_only_in_textbook(self):
        input_shape_list = [0, 1, 1, 1, 0, 0, 0]
        lattice_generator = LatticeGenerator(input_shape_list)

        lattices = lattice_generator.glue_shapes()._lattice_matrix
        face_graphs = FaceGraphGenerator.from_lattices(lattices)
        labels = TextbookIdentifier.identify(face_graphs, "model__1")
        
        filtered_lattices, filtered_graphs = TextbookIdentifier.get_only_in_textbook(lattices[-1], face_graphs, labels)

        self.assertEqual(len(filtered_lattices), len(filtered_graphs))

        self.assertEqual(type(filtered_lattices), list)
        for f_lattice in filtered_lattices:
            self.assertEqual(type(f_lattice), tuple)
            self.assertEqual(type(f_lattice[0]), Lattice)
            self.assertEqual(type(f_lattice[1]), list)
            for num_list in f_lattice[1]:
                self.assertEqual(num_list, 0)
        
        self.assertEqual(type(filtered_graphs), list)
        for f_group in filtered_graphs:
            self.assertEqual(type(f_group), list)
            for f_graph in f_group:
                self.assertEqual(type(f_graph), nx.MultiGraph)

    def test_get_group_only_in_textbook(self):
        input_shape_list = [0, 1, 0, 0, 0, 0, 0]
        lattice_generator = LatticeGenerator(input_shape_list)

        lattices = lattice_generator.glue_shapes()._lattice_matrix
        face_graphs = FaceGraphGenerator.from_lattices(lattices)[0]
        labels = TextbookIdentifier.identify_group(face_graphs, "model__1")

        filtered_graphs = TextbookIdentifier.get_group_only_in_textbook(face_graphs, labels)

        self.assertEqual(type(filtered_graphs), list)
        for f_graph in filtered_graphs:
            self.assertEqual(type(f_graph), nx.MultiGraph)

if __name__ == '__main__':
    unittest.main()