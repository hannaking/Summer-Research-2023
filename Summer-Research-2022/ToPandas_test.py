import json
import sys
import pandas as pd
import unittest

sys.path.insert(0, './Summer-Research-2022/')

from ToPandas import ToPandas


class TestToPandas_test(unittest.TestCase):
    def test_simpleShape(self):
        df1 = pd.Series(
            [1],
        )
        df2 = pd.DataFrame(
            {"point 1" : ['A', 'A', 'B', 'C'],
             "point 2" : ['B', 'D', 'C', 'D']},
             index = [0, 1, 2, 3])

        df3 = pd.DataFrame(
            {"shape" : [13,13,13,13],
             "sides" : [3, 3, 3, 3]},
             index = ["A","B","C","D"])
        
        textbook, nodes, edges = ToPandas.ToPanda('Summer-Research-2022/Json shapes/TestShape.json')

        self.assertTrue(df1.equals(textbook))
        self.assertTrue(df2.equals(nodes))
        self.assertTrue(df3.equals(edges))

    def test_Kite(self):
        df1 = pd.Series(
            [1],
        )
        df2 = pd.DataFrame(
            {"point 1" : ['A', 'A', 'C', 'B'],
             "point 2" : ['B', 'C', 'D', 'D']},
             index = [0, 1, 2, 3])

        df3 = pd.DataFrame(
            {"shape" : [11,11,13,13],
             "sides" : [3, 3, 3, 3]},
             index = ["A","B","C","D"])
        
        textbook, nodes, edges = ToPandas.ToPanda('Summer-Research-2022/Json shapes/Kite.json')

        self.assertTrue(df1.equals(textbook))
        self.assertTrue(df2.equals(nodes))
        self.assertTrue(df3.equals(edges))

    def test_ConcaveTriangles(self):
        df1 = pd.Series(
            [1],
        )
        df2 = pd.DataFrame(
            {"point 1" : ['A', 'A'],
             "point 2" : ['B', 'C']},
             index = [0, 1])

        df3 = pd.DataFrame(
            {"shape" : [13,12,12],
             "sides" : [3, 3, 3]},
             index = ["A","B","C"])
        
        textbook, nodes, edges = ToPandas.ToPanda('Summer-Research-2022/Json shapes/ConcaveTriangles.json')
        
        self.assertTrue(df1.equals(textbook))
        self.assertTrue(df2.equals(nodes))
        self.assertTrue(df3.equals(edges))

    def test_OctoSquares(self):
        df1 = pd.Series(
            [1],
        )

        df2 = pd.DataFrame(
            {"point 1" : ['A','A','A','B','E','E','E','E','E','F','F','I','I','I','I','I','J','J'],
             "point 2" : ['B','C','D','D','F','C','D','G','H','D','H','J','G','H','K','L','H','L']},
             index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

        df3 = pd.DataFrame(
            {"shape" : [60, 60, 20, 20, 60, 60, 20, 20, 60, 60 , 20, 20],
             "sides" : [8, 8, 4, 4, 8, 8, 4, 4, 8, 8, 4, 4]},
             index = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
        
        textbook, nodes, edges = ToPandas.ToPanda('Summer-Research-2022/Json shapes/OctoSquares 617-6.json')
        
        self.assertTrue(df1.equals(textbook))
        self.assertTrue(df2.equals(nodes))
        self.assertTrue(df3.equals(edges))

    
if __name__ == '__main__':
    unittest.main()
        

        
    

