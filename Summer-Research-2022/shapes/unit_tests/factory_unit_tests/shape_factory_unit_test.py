import unittest
import sys

sys.path.insert(0, './Summer-Research-2022/')

from lattice                                import Lattice
from shapes.triangles.triangle_factory      import TriangleFactory
from shapes.shape_factory                   import ShapeFactory
from unit_tests.shape_helpers               import ShapeHelpers    

class TestShapeFactory(unittest.TestCase):
    # ---------------------- init ---------------------- #
    def test_init_not_enough_edges(self):
        with self.assertRaises(ValueError):
            ShapeFactory(0)

    def test_init_correct_factory_found_triangle(self):
        factory = ShapeFactory(3)
        self.assertEqual(type(factory._shape_type_factory ), TriangleFactory)

    # ---------------------- coordinatize -------------------------- #
    #TODO



        





if __name__ == "__main__":
    unittest.main()