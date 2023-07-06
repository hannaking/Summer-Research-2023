
from gcn_graph_classification import GraphClassifier
from to_stellar_graph import ToStellarGraph

class TextbookIdentifier():

    # determines whether each graph belongs in a textbook according to a given model
    #
    # graphs - list of lists of networkx dual graphs ("face graphs")
    # model_name - name of the folder the model is saved in
    # 
    # returns the labels for each graph at the same indices
    @staticmethod
    def identify(graphs, model_name):
        labels= []
        
        for graph_group in graphs:
            labels.append(TextbookIdentifier.identify_group(graph_group, model_name))

        return labels

    # determines whether each graph belongs in a textbook according to a given model
    #
    # graph_group - list of networkx dual graphs ("face graphs")
    # model_name - name of the folder the model is saved in
    # 
    # returns the labels for each graph at the same indices
    @staticmethod
    def identify_group(graph_group, model_name):
        graphs = []
        for nx_graph in graph_group:
            graphs.append(ToStellarGraph.from_networkx(nx_graph, 'default'))
            
        classifier = GraphClassifier(graphs)
        classifier.load_model("Summer-Research-2022/models/" + model_name + "/model_save__1")
        
        predictions = classifier.predict()

        labels = []
        for pred in predictions:
            labels.append(bool(round(pred[0])))

        return labels
    
    # determines whether a graph belongs in a textbook according to a given model
    #
    # nx_graph - networkx dual graph ("face graph")
    # model_name - name of the folder the model is saved in
    # 
    # returns the label for the graph
    @staticmethod
    def identify_graph(nx_graph, model_name):
        graph = [ToStellarGraph.from_networkx(nx_graph, 'default')]
            
        classifier = GraphClassifier(graph)
        classifier.load_model("Summer-Research-2022/models/" + model_name + "/model_save__1")
        
        return bool(round(classifier.predict()[0][0]))
    
    # gets the lattices and dual graphs that are predicted to be from a textbook
    # 
    # lattices - list of lattice figures
    # graphs - list of lists of dual graphs ("face graphs")
    #            *each index in outer list is associated with one lattice
    # labels - parallel labels for each dual graph ("face graph")
    # 
    # returns a filtered list of lattices and list of lists of dual graphs ("face graphs")
    @staticmethod
    def get_only_in_textbook(lattices, graphs, labels):
        textbook_lattices = []
        textbook_graphs = []
        
        for i, graph_group in enumerate(graphs):

            filtered_group = TextbookIdentifier.get_group_only_in_textbook(graph_group, labels[i])
            
            if filtered_group != []:
                textbook_lattices.append(lattices[i])
                textbook_graphs.append(filtered_group)
        
        return textbook_lattices, textbook_graphs
    
    # gets the dual graphs that are predicted to be from a textbook
    # 
    # graph_groups - list of dual graphs ("face graphs")
    # labels - parallel labels for each dual graph ("face graph")
    # 
    # returns a filtered list of dual graphs ("face graphs")
    @staticmethod
    def get_group_only_in_textbook(face_graph_group, labels):
        textbook_graphs = []
        
        for i, face_graph in enumerate(face_graph_group):
            if labels[i]:
                textbook_graphs.append(face_graph)
        
        return textbook_graphs