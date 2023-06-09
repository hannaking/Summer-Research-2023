import pandas as pd
import json
class ToPandas():
    
    def ToPanda(JsonFile):

        SHAPE_NUMBER_MAP = {"Line Segment": 00,
                            "Isosceles Right Triangle": 10, "Right Triangle" : 11, "Equilateral Triangle" : 12,
                                "Isosceles Triangle" : 13,
                            "Square" : 20, "Rectangle" : 21, "Rhombus" : 22, "Parallelogram" : 23, "Kite" : 24,
                                "Right Trapezoid" : 25, "Isosceles Trapezoid" : 26, "Dart" : 27,
                            "Regular Pentagon" : 30,
                            "Regular Hexagon" : 40,
                            "Regular Septagon" : 50,
                            "Regular Octogon" : 60}
        
        with open(JsonFile,'r') as f:
            data = json.loads(f.read())

        try:
            edges = pd.json_normalize(data, record_path=['edges'],errors='ignore')
            nodes = pd.json_normalize(data, record_path=['nodes'],errors='ignore')
        except KeyError as e:
            print(f"Unable to normalize json: {json.dumps(data, indent=4)}")

        for i, num in enumerate(edges['count'].values):
            for j in range(num-1):
                edges.loc[len(edges.index)] = edges.iloc[i]
        edges = edges.drop("count", axis=1)

        nodes = nodes.rename(nodes["ID"])
        nodes = nodes.drop("ID", axis=1)
        nodes = nodes["shape"].replace(SHAPE_NUMBER_MAP)


        return edges, nodes
    
    print(ToPanda('C:/Users/awgar/Desktop/JsonShapes/ConcaveTriangles.json'))