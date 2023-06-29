import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
import stellargraph as sg
from stellargraph.mapper import PaddedGraphGenerator
from stellargraph.layer import GCNSupervisedGraphClassification
from stellargraph import StellarGraph
from stellargraph import datasets
from sklearn import model_selection
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.callbacks import EarlyStopping

from to_stellar_graph import ToStellarGraph

class GraphClassifier:

    """
    The Graph Classifier can create a model that predicts a label for a list of graphs, or
    use a model to predict the labels of never-before-seen graphs.

    stellar_graphs - a list of stellar graphs that the graph classifier will be working on
    graphs_labels - the label indicating, for each graph, whether the graph is from a textbook
    model - the model that predicts whether a graph is textbook-like or not.
    """
    def __init__(self, stellar_graphs:StellarGraph, graph_labels:pd.Series=None, model=None):
        self.set_graphs(stellar_graphs, graph_labels)
        self.model = model
        self.es = EarlyStopping()
        
        self.set_parameters(epochs=200, folds=10, n_repeats=5, monitor="val_loss",
                            min_delta=0, patience=25, restore_best_weights=True,
                            test_size=0.2, batch_size=30)

    # Gets a graph and it's corresponding label using their index.
    #
    # index - the index of the graph / graph label
    #
    # returns the graph and corresponding graph label
    def get_graph(self, index:int):
        return self.graphs[index], self.graph_labels[index]

    # sets the list graphs to something else
    # 
    # stellar_graphs - the list of new graphs
    # graph_labels - the corresponding list of new graph labels
    def set_graphs(self, stellar_graphs:StellarGraph, graph_labels:pd.Series=None):
        self.graphs = stellar_graphs
        self.generator = PaddedGraphGenerator(graphs=self.graphs)
        
        if graph_labels is not None:
            self.graph_labels = graph_labels
    
    # retrieves the graphs and graph labels
    # 
    # returns the list of graphs and list of labels
    def get_graphs(self):
        return self.graphs, self.graph_labels

    # loads the model from a save at a given path
    #
    # path - the path to the saved model
    #
    # model - the model that can determine labels
    def load_model(self, path):
        self.model = Model.load_model(path)
    
    # sets the model to something else
    #
    # model - the model that can determine labels
    def set_model(self, model):
        self.model = model

    # saves the model as files at a given path
    # 
    # path - path the model is saved to
    #
    # returns the model
    def save_model(self, path):
        self.model.save(path, False)
    
    # retrieves the model that is used for prediction
    #
    # returns the model
    def get_model(self):
        return self.model
    
    # sets the input parameters to the training algorithm
    # 
    # epochs(200)                - maximum number of repitions (per fold in evaluate)
    # folds(10)                  - number of groups for evaluation
    # n-repeats(5)               - number of number of times all folds are cycled for evaluation
    # monitor("val_loss")        - what it looks for to adjust
    # min_delta(0)               - minimum change for an improvement
    # patience(25)               - how long it will wait for an improvement before moving on
    # restore_best_weights(True) - whether to restore the best observed weights
    # test_size(0.2)             - proportion of the graphs that are used for testing
    # batch_size(30)             - the number of graphs that are evaluated as one
    def set_parameters(self, epochs:int=None, folds:int=None, n_repeats:int=None, monitor:str=None,
                       min_delta:int=None, patience:int=None, restore_best_weights:bool=None,
                       test_size:float=None, batch_size:int=None):
        if epochs is not None:               self.epochs = epochs
        if folds is not None:                self.folds = folds
        if n_repeats is not None:            self.n_repeats = n_repeats
        if monitor is not None:              self.es.monitor = monitor
        if min_delta is not None:            self.es.min_delta = min_delta
        if patience is not None:             self.es.patience = patience
        if restore_best_weights is not None: self.es.restore_best_weights = restore_best_weights
        if test_size is not None:            self.test_size = test_size
        if batch_size is not None:           self.batch_size = batch_size

    # returns the epochs
    def get_epochs(self):
        return self.epochs
    
    # returns the folds
    def get_folds(self):
        return self.folds
    
    # returns the number of repeats
    def get_n_repeats(self):
        return self.es.min_delta
    
    # returns the monitor
    def get_monitor(self):
        return self.es.monitor

    # returns the minimum delta
    def get_min_delta(self):
        return self.es.min_delta
    
    # returns the patience
    def get_patience(self):
        return self.es.patience
    
    # returns whether it restores the best weights
    def get_restore_best_weights(self):
        return self.es.restore_best_weights
    
    # returns the proportionate test size
    def get_test_size(self):
        return self.test_size
    
    # returns the batch size
    def get_batch_size(self):
        return self.batch_size

    # reads all JSON files contained in a given path.
    # 
    # directory - directory the json files are located in
    # 
    # saves all of the contents as stellar graphs
    def read_json_graphs(self, directory):
        graphs = []
        graph_labels = pd.DataFrame()

        if os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith('.json'):
                        with open(os.path.join(dirpath, filename)) as f:
                            graph, label = ToStellarGraph.from_json(f.name)
                            graphs.append(graph)
                            graph_labels = pd.concat([graph_labels, label])
        else:
            print("File does not exist.")
        
        self.set_graphs(graphs, graph_labels)
    
    # creates the classification model
    # the model is composed of:
    # 2 supervised graph graph convolutional networks of 64 nodes each
    # 1 mean pooling layer
    # 2 compleatly connected layers of 32 and 16 nodes
    # 1 output layer with 1 node
    #
    # returns the created model
    def _create_graph_classification_model(self):
        gc_model = GCNSupervisedGraphClassification(
            layer_sizes=[64, 64],
            activations=["relu", "relu"],
            generator=self.generator,
            dropout=0
        )
        x_inp, x_out = gc_model.in_out_tensors()
        predictions = Dense(units=64, activation="relu")(x_out)
        predictions = Dense(units=64, activation="relu")(predictions)
        predictions = Dense(units=1, activation="sigmoid")(predictions)

        model = Model(inputs=x_inp, outputs=predictions)
        model.compile(optimizer=Adam(0.01), loss=binary_crossentropy, metrics=["acc"])

        return model
    
    # trains one fold of the algorithm
    #
    # train_gen - the generator associated with the training graphs
    # test_gen - the generator assocated with the testing graphs (used for validation)
    # 
    # returns the testing accuracy
    def _train_model(self, train_gen, test_gen):
        self.model.fit(
            train_gen, epochs=self.epochs, validation_data=test_gen, verbose=0, callbacks=[self.es],
        )
    
    # calculates the performance on the test data
    # 
    # test_gen - the generator assocated with the testing graphs
    # 
    # returns the testing accuracy
    def _test_model(self, test_gen):
        # calculate performance on the test data and return
        test_metrics = self.model.evaluate(test_gen, verbose=0)
        test_acc = test_metrics[self.model.metrics_names.index("acc")]

        return test_acc
    
    # gets the generator associated with the training graphs
    # 
    # train_index - the indexes in the list of graphs that are being trained on
    # batch_size - the number of graphs that are evaluated as one
    # 
    # returns the generators
    def _get_training_generator(self, train_index):
        train_gen = self.generator.flow(
            train_index, targets=self.graph_labels.iloc[train_index].values, batch_size=self.batch_size
        )

        return train_gen
    
    # gets the generator associated with the testing graphs
    # 
    # test_index - the indexes in the list of graphs that are being tested on
    # batch_size - the number of graphs that are evaluated as one
    # 
    # returns the generators
    def _get_testing_generator(self, test_index):
        test_gen = self.generator.flow(
            test_index, targets=self.graph_labels.iloc[test_index].values, batch_size=self.batch_size
        )

        return test_gen
    
    # trains the model to predict the label using the graphs
    def train(self):
        graphs_i = list(range(0, len(self.graphs)))

        train_index, test_index = train_test_split(graphs_i, test_size = self.test_size)

        train_gen = self._get_training_generator(train_index)
        test_gen = self._get_testing_generator(test_index)

        self.model = self._create_graph_classification_model()

        self._train_model(train_gen, test_gen)

    # generates and evaluates the accuracy of a model at predicting graph labels using the graphs
    #
    # returns the mean accuracy and standered deviation
    def evaluate(self):
        test_accs = []

        stratified_folds = model_selection.RepeatedStratifiedKFold(
            n_splits=self.folds, n_repeats=self.n_repeats
        ).split(self.graph_labels, self.graph_labels)

        for i, (train_index, test_index) in enumerate(stratified_folds):
            test_gen = self._get_testing_generator(test_index)

            acc = self._test_model(test_gen)

            test_accs.append(acc)
        
        plt.figure(figsize=(8, 6))
        plt.hist(test_accs)
        plt.xlabel("Accuracy")
        plt.ylabel("Count")
        plt.show()
        return float(np.mean(test_accs)), float(np.std(test_accs))

    # makes a prediction for the graphs using the model
    # 
    # returns the predictions for all graphs
    def predict(self):
        gen = self.generator.flow(self.graphs, targets=[0 for graph in self.graphs])
        return self.model.predict(x=gen, verbose=0)

classifier = GraphClassifier([], pd.Series())
classifier.read_json_graphs("Summer-Research-2022")
print(len(classifier.graphs))
print(len(classifier.graph_labels))
classifier.train()
print(classifier.evaluate())