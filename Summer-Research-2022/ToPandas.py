import pandas as pd
import json
class ToPandas():
    
    def ToPanda(JsonFile):

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


        return edges, nodes
    
    print(ToPanda('C:/Users/awgar/Desktop/JsonShapes/ConcaveTriangles.json'))