import json
import pandas as pd
from ToPandas import ToPandas
import unittest

class TestToPandas_test(unittest.TestCase):
    def test_simpleShape(self):
        df = pd.DataFrame(
            {"point 1" : ['A', 'A', 'B', 'C'],
            "point 2" : ['B', 'D', 'C', 'D']},
            index = [0, 1, 2, 3])

        df2 = pd.DataFrame(
            {"shape" : ['Isosceles Triangle','Isosceles Triangle','Isosceles Triangle','Isosceles Triangle' ],
            "sides" : [3, 3, 3, 3]},
            index = ["A","B","C","D"])
        
        nodes, edges = ToPandas.ToPanda('C:/Users/awgar/Desktop/JsonShapes/TestShape.json')

        self.assertTrue(df.equals(nodes))
        self.assertTrue(df2.equals(edges))

    def test_Kite(self):
        df = pd.DataFrame(
            {"point 1" : ['A', 'A', 'C', 'B'],
            "point 2" : ['B', 'C', 'D', 'D']},
            index = [0, 1, 2, 3])

        df2 = pd.DataFrame(
            {"shape" : ['Right Triangle','Right Triangle','Isosceles Triangle','Isosceles Triangle' ],
            "sides" : [3, 3, 3, 3]},
            index = ["A","B","C","D"])
        
        nodes, edges = ToPandas.ToPanda('C:/Users/awgar/Desktop/JsonShapes/Kite.json')

        self.assertTrue(df.equals(nodes))
        self.assertTrue(df2.equals(edges))

    def test_ConcaveTriangles(self):
        df = pd.DataFrame(
            {"point 1" : ['A', 'B'],
            "point 2" : ['A', 'C']},
            index = [0, 1])

        df2 = pd.DataFrame(
            {"shape" : ['Isosceles Triangle','Equilateral Triangle','Equilateral Triangle' ],
            "sides" : [3, 3, 3]},
            index = ["A","B","C"])
        
        nodes, edges = ToPandas.ToPanda('C:/Users/awgar/Desktop/JsonShapes/ConcaveTriangles.json')

        self.assertTrue(df.equals(nodes))
        self.assertTrue(df2.equals(edges))

    
if __name__ == '__main__':
    unittest.main()
        

        
    

