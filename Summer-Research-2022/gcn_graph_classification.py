import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from stellargraph.mapper import PaddedGraphGenerator
from stellargraph.layer import GCNSupervisedGraphClassification
from stellargraph import StellarGraph
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from tensorflow import keras
from keras import Model
from keras.optimizers import Adam
from keras.layers import Dense
from keras.losses import binary_crossentropy
from keras.callbacks import EarlyStopping
import keras_tuner
from keras.utils.vis_utils import plot_model
from ann_visualizer.visualize import ann_viz;
import visualkeras

from to_stellar_graph import ToStellarGraph
from graph_hyper_model import CVTuner

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
    def set_graphs(self, stellar_graphs:list[StellarGraph], graph_labels:pd.Series=None):
        self.graphs = stellar_graphs
        self.generator = PaddedGraphGenerator(graphs=self.graphs)
        
        if graph_labels is not None:
            self.graph_labels = graph_labels

    # adds graphs to the list and labels if any are passed in
    # 
    # stellar_graphs - the list of new graphs
    # graph_labels - the corresponding list of new graph labels
    def add_graphs(self, stellar_graphs:list[StellarGraph], graph_labels:pd.Series=None):
        self.graphs.extend(stellar_graphs)
        self.generator = PaddedGraphGenerator(graphs=self.graphs)
        
        if graph_labels is not None:
            self.graph_labels = pd.concat([self.graph_labels, graph_labels])
    
    # retrieves the graphs and graph labels
    # 
    # returns the list of graphs and list of labels
    def get_graphs(self):
        return self.graphs, self.graph_labels

    # loads the model from a save at a given path
    #
    # path - the path to the saved model
    #
    def load_model(self, path):
        self.model = keras.models.load_model(path)
    
    # sets the model to something else
    #
    # model - the model that can determine labels
    #
    def set_model(self, model):
        self.model = model

    # saves the model as files at a given path
    # creates a subfolder called model__#
    # (# is the number of models that have been saved in the file)
    # 
    # path - path the model is saved to
    #
    def save_model(self):
        superpath = self._create_folder("Summer-Research-2022/models", "model")
        
        subpath1 = self._create_folder(superpath, "model_save")
        self.model.save(subpath1)
        
        subpath2 = self._create_folder(superpath, "model_visual")
        self._save_model_visual(subpath2)
    
    # saves the model visual as a file at a given path
    # creates a subfolder called model_visual__1
    # 
    # returns the path to (and including) the new subfolder
    def _save_model_visual(self, path):
        plot_model(
            self.model,
            to_file=path + "/visual.png",
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=96,
            layer_range=None,
            show_layer_activations=True,
            show_trainable=True,  
        )

    def _create_folder(self, path, name):
        all_folders = next(os.walk(path + '/.'))[1]
        
        current = 0
        for folder in all_folders:
            splits = folder.split("__")
            if name in splits and splits[-1].isdigit() and int(splits[-1]) > current:
                current = int(splits[-1])
        
        file_path = path + "/" + name + "__" + str(current+1)
        os.mkdir(file_path)

        return file_path


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
        
        self.add_graphs(graphs, graph_labels)
    
    # creates the classification model
    # the model is composed of:
    # 2 supervised graph graph convolutional networks
    # 1 mean pooling layer
    # 2 compleatly connected layers
    # 1 output layer with 1 node
    # 
    # dropout - dropout rate of the model
    # learning_rate - learning rate of the model
    # layer_1_size - size of the first layer
    # layer_1_activation - activation of the first layer
    # layer_2_size -  size of the second layer
    # layer_2_activation - activation of the second layer
    # layer_3_size -  size of the third layer
    # layer_3_activation - activation of the third layer
    # layer_4_size -  size of the fourth layer
    # layer_4_activation - activation of the fourth layer
    #
    # returns the created model
    def _construct_model(self, dropout, learning_rate,
                         layer_1_size, layer_1_activation,
                         layer_2_size, layer_2_activation,
                         layer_3_size, layer_3_activation,
                         layer_4_size, layer_4_activation):
        gc_model = GCNSupervisedGraphClassification(
            layer_sizes = [layer_1_size,       layer_2_size],
            activations = [layer_1_activation, layer_2_activation],
            generator   = self.generator,
            dropout     = dropout
        )
        x_inp, x_out = gc_model.in_out_tensors()
        predictions = Dense(units = layer_3_size, activation = layer_3_activation)(x_out)
        predictions = Dense(units = layer_4_size, activation = layer_4_activation)(predictions)
        predictions = Dense(units = 1,            activation="sigmoid"           )(predictions)

        model = Model(inputs=x_inp, outputs=predictions)
        model.compile(optimizer=Adam(learning_rate), loss=binary_crossentropy, metrics=["acc"])

        return model
    
    # creates a model that has its hyperparameters tuned.
    #
    # returns the model
    def _create_graph_classification_model(self, hp):

        dropout = hp.Float("dropout", min_value=0, max_value=0.5)
        learning_rate = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")
        
        layer_1_size = hp.Int("units_1", min_value=16, max_value=512, step=16)
        layer_2_size = hp.Int("units_2", min_value=16, max_value=512, step=16)
        layer_3_size = hp.Int("units_3", min_value=16, max_value=512, step=16)
        layer_4_size = hp.Int("units_4", min_value=16, max_value=512, step=16)
        
        layer_1_activation = hp.Choice("activation_1", ["relu", "tanh"])
        layer_2_activation = hp.Choice("activation_2", ["relu", "tanh"])
        layer_3_activation = hp.Choice("activation_3", ["relu", "tanh"])
        layer_4_activation = hp.Choice("activation_4", ["relu", "tanh"])
        
        model = self._construct_model(
            dropout, learning_rate,
            layer_1_size, layer_1_activation,
            layer_2_size, layer_2_activation,
            layer_3_size, layer_3_activation,
            layer_4_size, layer_4_activation
        )
        return model
    
    # gets the hyperparmeter tuner
    #
    def _get_tuner(self, does_overwrite):
        tuner = CVTuner(
            hypermodel= self._create_graph_classification_model,
            objective=keras_tuner.Objective('eval', direction='max'),
            max_trials=10,
            executions_per_trial=2,
            overwrite=does_overwrite,
            directory="Summer-Research-2022/models",
            project_name="tuning",
        )
        return tuner

    # trains one fold of the algorithm
    #
    # model - model that is being trained
    # train_gen - the generator associated with the training graphs
    # test_gen - the generator assocated with the testing graphs (used for validation)
    # 
    # returns the testing accuracy
    def _train_model(self, model, train_gen, test_gen):
        history = model.fit(
            train_gen, epochs=self.epochs, validation_data=test_gen, verbose=0, callbacks=[self.es],
        )

        return history
    
    # calculates the performance on the test data
    # 
    # model - model that is being tested
    # test_gen - the generator assocated with the testing graphs
    # 
    # returns the testing accuracy
    def _test_model(self, model, test_gen):
        # calculate performance on the test data and return
        test_metrics = model.evaluate(test_gen, verbose=0)
        test_acc = test_metrics[model.metrics_names.index("acc")]

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
    
    # trains a model while being able to tune hyperperamenters
    #
    # train_index - the indices of the graphs used for training
    # test_index - the indices of the graphs used for testing
    # does_tune - whether the model is tuned as part of the training
    #
    # returns the trained model, the traing history and the testing accuracy
    def _trainer(self, train_index, test_index, does_tune):
        train_gen = self._get_training_generator(train_index)
        test_gen = self._get_testing_generator(test_index)

        tuner = self._get_tuner(does_tune)
        if does_tune:
            tuner.search(
                    generator=self.generator,
                    graphs=self.graphs,
                    labels=self.graph_labels,
                    k=self.n_repeats, 
                    folds=self.folds, 
                    batch_size=self.batch_size,
                    epochs=self.epochs,
                    es=self.es
                )
        
        best_hp = tuner.get_best_hyperparameters(1)
        if best_hp == []:
            best_hp = [keras_tuner.HyperParameters()]

        model = self._create_graph_classification_model(best_hp[0])

        history  = self._train_model(model, train_gen, test_gen)
        test_acc = self._test_model(model, test_gen)

        return model, history, test_acc

    # trains the model to predict the label using the graphs
    #
    # returns the training history and the testing accuracy
    def train(self):
        graphs_i = list(range(0, len(self.graphs)))

        train_index, test_index = train_test_split(graphs_i, test_size = self.test_size)
        
        model, history, test_acc = self._trainer(train_index, test_index, True)
        
        self.model = model
        
        self.save_model()

        return history, test_acc

    # generates and evaluates the accuracy of a model at predicting graph labels using the graphs
    #
    # returns the mean accuracy, standered deviation and the list of all accuracies across folds
    def evaluate_model(self):
        test_accs = []

        stratified_folds = model_selection.RepeatedStratifiedKFold(
            n_splits=self.folds, n_repeats=self.n_repeats
        ).split(self.graph_labels, self.graph_labels)

        for i, (train_index, test_index) in enumerate(stratified_folds):
            test_gen = self._get_testing_generator(test_index)

            acc = self._test_model(self.model, test_gen)

            test_accs.append(acc)
        
        return float(np.mean(test_accs)), float(np.std(test_accs)), test_accs
    
    # generates and evaluates the accuracy of a model at predicting graph labels using the graphs
    #
    # returns the mean accuracy, standered deviation, the list of all accuracies across folds and
    # the histories of all training accross all folds
    def evaluate(self):
        test_accs = []
        test_histories = []

        stratified_folds = model_selection.RepeatedStratifiedKFold(
            n_splits=self.folds, n_repeats=self.n_repeats
        ).split(self.graph_labels, self.graph_labels)

        for i, (train_index, test_index) in enumerate(stratified_folds):
            print(f"Training and evaluating on fold {i+1} out of {self.folds * self.n_repeats}...")

            model, history, acc = self._trainer(train_index, test_index, False)

            test_histories.append(history)
            test_accs.append(acc)

        return float(np.mean(test_accs)), float(np.std(test_accs)), test_accs, test_histories

    # makes a prediction for the graphs using the model
    # 
    # returns the predictions for all graphs
    def predict(self):
        gen = self.generator.flow(self.graphs, targets=[0 for graph in self.graphs])
        return self.model.predict(x=gen, verbose=0)

# classifier = GraphClassifier([], pd.DataFrame())
# classifier.load_model("Summer-Research-2022/models/model__1/model_save__1")
# model = classifier.model

# print(model.layers)

# a = visualkeras.graph_view(model, layer_spacing=75, node_spacing=-10)

# print(a.show())


# classifier = GraphClassifier([], pd.DataFrame())

# classifier.read_json_graphs("Summer-Research-2022/Json shapes")
# classifier.read_json_graphs("Summer-Research-2022/negative_shapes")

# print(len(classifier.graphs))
# print(len(classifier.graph_labels))

# train_history = classifier.train()

# m_eval_mean, m_eval_std, m_eval_accs = classifier.evaluate_model()

# eval_mean, eval_std, eval_accs, eval_history = classifier.evaluate()

# print(m_eval_mean, m_eval_std)
# print(eval_mean, eval_std)

# plt.figure(figsize=(8, 6))
# plt.hist(m_eval_accs)
# plt.xlabel("Model Accuracy")
# plt.ylabel("Count")
# plt.show()

# plt.figure(figsize=(8, 6))
# plt.hist(eval_accs)
# plt.xlabel("Evaluation Accuracy")
# plt.ylabel("Count")
# plt.show()