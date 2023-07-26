import sys
import os
import numpy as np

import pandas as pd
import unittest

sys.path.insert(0, './Summer-Research-2022/')

from gcn_graph_classification import GraphClassifier

from to_stellar_graph import ToStellarGraph

class TestToStellarGraph(unittest.TestCase):

    '''
    
    Helper Methods
    
    '''

    #
    # creates a classifier containing a graph without a label
    #
    def create_unknown_classifier(self):
        graph, label = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/TestShape.json')
        graphs = [graph]
        classifier = GraphClassifier(graphs)
        return classifier

    #
    # creates a classifier containing a graph and its associated label
    #
    def create_simple_classifier(self):
        graph, label = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/TestShape.json')
        graphs = [graph]
        labels = label
        classifier = GraphClassifier(graphs, labels)
        return classifier
    
    #
    # creates a classifier containing 5 graphs and their associated labels
    #
    def create_small_classifier(self):
        graph1, label1 = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/TestShape.json')
        graph2, label2 = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Triangles/ConcaveTringlesWithRight.json')
        graph3, label3 = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Polygons/Pentagram 150.json')
        graph4, label4 = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Triangles/KiteOfTriangles.json')
        graph5, label5 = ToStellarGraph.from_json('Summer-Research-2022/Json shapes/Quadrilaterals/KiteAndDart.json')
        graphs = [graph1, graph2, graph3, graph4, graph5]
        labels = pd.concat([label1, label2, label3, label4, label5])
        classifier = GraphClassifier(graphs, labels)
        return classifier
    
    #
    # creates a classifier containing many graphs and their associated labels
    #
    def create_large_classifier(self):
        graphs = []
        labels = pd.DataFrame()

        directory = 'Summer-Research-2022/Json shapes'
        if os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith('.json'):
                        with open(os.path.join(dirpath, filename)) as f:
                            graph, label = ToStellarGraph.from_json(f.name)
                            graphs.append(graph)
                            labels = pd.concat([labels, label])
        else:
            print("File does not exist.")
        
        classifier = GraphClassifier(graphs[0:20], labels.head(20))
        return classifier

    """

    Unknown Tests
    
    """
    
    #
    # checks that a model is made without a label
    #
    def test_create_graph_classification_model_unknown(self):
        classifier = self.create_unknown_classifier()

        model = classifier._create_graph_classification_model()
        self.assertIsNotNone(model)

     #
    # tests that a prediction is made without a label
    #
    def test_predict_unknown(self):
        classifier = self.create_unknown_classifier()

        classifier.model = classifier._create_graph_classification_model()
        predictions = classifier.predict()

        self.assertEqual(type(predictions), np.ndarray)
        self.assertEqual(type(predictions[0][0]), np.float32)
        self.assertTrue(predictions[0][0] >= 0 and predictions[0][0] <= 1)

    
    """

    Simple Tests
    
    """

    #
    # checks that all of the parameters are set to their initial defaults
    #
    def test_set_parameters_defaults(self):
        classifier = self.create_simple_classifier()
        
        self.assertEqual(classifier.epochs, 200)
        self.assertEqual(classifier.folds, 10)
        self.assertEqual(classifier.n_repeats, 5)
        self.assertEqual(classifier.es.monitor, "val_loss")
        self.assertEqual(classifier.es.min_delta, 0)
        self.assertEqual(classifier.es.patience, 25)
        self.assertEqual(classifier.es.restore_best_weights, True)
        self.assertEqual(classifier.test_size, 0.2)
        self.assertEqual(classifier.batch_size, 30)

    #
    # checks that modifying one parameter only affects that one
    #
    def test_set_parameters_one(self):
        classifier = self.create_simple_classifier()

        classifier.set_parameters(epochs=10)
        
        self.assertEqual(classifier.epochs, 10)
        self.assertEqual(classifier.folds, 10)
        self.assertEqual(classifier.n_repeats, 5)
        self.assertEqual(classifier.es.monitor, "val_loss")
        self.assertEqual(classifier.es.min_delta, 0)
        self.assertEqual(classifier.es.patience, 25)
        self.assertEqual(classifier.es.restore_best_weights, True)
        self.assertEqual(classifier.test_size, 0.2)
        self.assertEqual(classifier.batch_size, 30)

    #
    # checks that modifying multiple parameters only affects the ones that were modified
    #
    def test_set_parameters_two(self):
        classifier = self.create_simple_classifier()

        classifier.set_parameters(restore_best_weights=False, monitor="loss")

        self.assertEqual(classifier.epochs, 200)
        self.assertEqual(classifier.folds, 10)
        self.assertEqual(classifier.n_repeats, 5)
        self.assertEqual(classifier.es.monitor, "loss")
        self.assertEqual(classifier.es.min_delta, 0)
        self.assertEqual(classifier.es.patience, 25)
        self.assertEqual(classifier.es.restore_best_weights, False)
        self.assertEqual(classifier.test_size, 0.2)
        self.assertEqual(classifier.batch_size, 30)

    #
    # check that all modifiers can be successfully modified
    #
    def test_set_parameters_all(self):
        classifier = self.create_simple_classifier()

        classifier.set_parameters(min_delta=100, test_size=1, epochs=1, patience=-1, n_repeats=0,
                                  batch_size=1000, monitor="acc", restore_best_weights=False, folds=7)

        self.assertEqual(classifier.epochs, 1)
        self.assertEqual(classifier.folds, 7)
        self.assertEqual(classifier.n_repeats, 0)
        self.assertEqual(classifier.es.monitor, "acc")
        self.assertEqual(classifier.es.min_delta, 100)
        self.assertEqual(classifier.es.patience, -1)
        self.assertEqual(classifier.es.restore_best_weights, False)
        self.assertEqual(classifier.test_size, 1)
        self.assertEqual(classifier.batch_size, 1000)

    #
    # checks that a model is made with one graph
    #
    def test_create_graph_classification_model_simple(self):
        classifier = self.create_simple_classifier()

        model = classifier._create_graph_classification_model()
        self.assertIsNotNone(model)

    #
    # checks that a generator is made with one graph
    #
    def test_get_training_generator_simple(self):
        classifier = self.create_simple_classifier()

        train_gen = classifier._get_training_generator([0])
        self.assertIsNotNone(train_gen)

    #
    # checks that a generator is made with one graph
    #
    def test_get_testing_generator_simple(self):
        classifier = self.create_simple_classifier()

        test_gen = classifier._get_testing_generator([0])
        self.assertIsNotNone(test_gen)

    #
    # checks that a model is made with one graph
    #
    def test_train_model_simple(self):
        classifier = self.create_simple_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator([0])
        test_gen = classifier._get_testing_generator([0])
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that the test returns an accuracy score with one graph
    #
    def test_test_model_simple(self):
        classifier = self.create_simple_classifier()

        classifier.model = classifier._create_graph_classification_model()
        test_gen = classifier._get_testing_generator([0])
        acc = classifier._test_model(test_gen)

        self.assertEqual(type(acc), float)
        self.assertTrue(acc >= 0 and acc <= 1)

    #
    # tests that a prediction is made with one graph
    #
    def test_predict_simple(self):
        classifier = self.create_simple_classifier()

        classifier.model = classifier._create_graph_classification_model()
        predictions = classifier.predict()

        self.assertEqual(type(predictions), np.ndarray)
        self.assertEqual(type(predictions[0][0]), np.float32)
        self.assertTrue(predictions[0][0] >= 0 and predictions[0][0] <= 1)

    """

    Small Tests
    
    """

    #
    # checks that a model is made with five graphs
    #
    def test_create_graph_classification_model_small(self):
        classifier = self.create_small_classifier()

        model = classifier._create_graph_classification_model()
        self.assertIsNotNone(model)

    #
    # checks that a generator is made with five graphs using only some of them
    #
    def test_get_training_generator_partial_small(self):
        classifier = self.create_small_classifier()

        train_gen = classifier._get_training_generator([0, 1])
        self.assertIsNotNone(train_gen)

    #
    # checks that a generator is made with five graphs using all of them
    #
    def test_get_training_generator_whole_small(self):
        classifier = self.create_small_classifier()

        train_gen = classifier._get_training_generator([0, 1, 2, 3, 4])
        self.assertIsNotNone(train_gen)

    #
    # checks that a generator is made with five graphs using only some of them
    #
    def test_get_testing_generator_partial_small(self):
        classifier = self.create_small_classifier()

        test_gen = classifier._get_testing_generator([1, 2])
        self.assertIsNotNone(test_gen)

    #
    # checks that a generator is made with five graphs using all of them
    #
    def test_get_testing_generator_whole_small(self):
        classifier = self.create_small_classifier()

        test_gen = classifier._get_testing_generator([0, 1, 2, 3, 4])
        self.assertIsNotNone(test_gen)

    #
    # checks that a model is made with five graphs using only some of them without repetition
    #
    def test_train_model_partial_unique_small(self):
        classifier = self.create_small_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator([0, 1])
        test_gen = classifier._get_testing_generator([2, 3])
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with five graphs using only some of them with repetition
    #
    def test_train_model_partial_repeating_small(self):
        classifier = self.create_small_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator([0, 1])
        test_gen = classifier._get_testing_generator([1, 2, 3])
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with five graphs using all of them without repetition
    #
    def test_train_model_whole_unique_small(self):
        classifier = self.create_small_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator([0, 1, 2])
        test_gen = classifier._get_testing_generator([3, 4])
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with five graphs using all of them with repetition
    #
    def test_train_model_whole_repeating_small(self):
        classifier = self.create_small_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator([0, 1, 2, 3, 4])
        test_gen = classifier._get_testing_generator([0, 1, 2, 3, 4])
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that the test returns an accuracy score with five graphs using only some of them
    #
    def test_test_model_partial_small(self):
        classifier = self.create_small_classifier()

        classifier.model = classifier._create_graph_classification_model()
        test_gen = classifier._get_testing_generator([1, 2, 3])
        acc = classifier._test_model(test_gen)

        self.assertEqual(type(acc), float)
        self.assertTrue(acc >= 0 and acc <= 1)

    #
    # checks that the test returns an accuracy score with five graphs using all of them
    #
    def test_test_model_whole_small(self):
        classifier = self.create_small_classifier()

        classifier.model = classifier._create_graph_classification_model()
        test_gen = classifier._get_testing_generator([0, 1, 2, 3, 4])
        acc = classifier._test_model(test_gen)

        self.assertEqual(type(acc), float)
        self.assertTrue(acc >= 0 and acc <= 1)

    # 
    # checks that a model is producted by training with five graphs
    # 1 testing graph and 4 training graphs
    #
    def test_train_small(self):
        classifier = self.create_small_classifier()

        classifier.model = classifier._create_graph_classification_model()
        classifier.train()

        self.assertIsNotNone(classifier.model)

    #
    # checks that the mean and sd are returned by evaluating the model with five graphs
    # 2 folds with 1 repetition
    #
    def test_evaluate_small(self):
        classifier = self.create_small_classifier()
        classifier.folds = 2
        classifier.n_repeats = 1

        classifier.model = classifier._create_graph_classification_model()
        mean, sd = classifier.evaluate()

        self.assertEqual(type(mean), float)
        self.assertEqual(type(sd), float)

    #
    # tests that a prediction is made with five graphs
    #
    def test_predict_small(self):
        classifier = self.create_small_classifier()

        classifier.model = classifier._create_graph_classification_model()
        predictions = classifier.predict()

        self.assertEqual(type(predictions), np.ndarray)
        for prediction in predictions:
            self.assertEqual(type(prediction[0]), np.float32)
            self.assertTrue(prediction[0] >= 0 and prediction[0] <= 1)

    """

    Large Tests
    
    """

    #
    # checks that a model is made with many graphs
    #
    def test_create_graph_classification_model_large(self):
        classifier = self.create_large_classifier()

        model = classifier._create_graph_classification_model()
        self.assertIsNotNone(model)

    #
    # checks that a generator is made with many graphs using only some of them
    #
    def test_get_training_generator_partial_large(self):
        classifier = self.create_large_classifier()

        train_gen = classifier._get_training_generator(range(0, int(len(classifier.graphs)/2)))
        self.assertIsNotNone(train_gen)

    #
    # checks that a generator is made with many graphs using all of them
    #
    def test_get_training_generator_whole_large(self):
        classifier = self.create_large_classifier()

        train_gen = classifier._get_training_generator(range(0, len(classifier.graphs)))
        self.assertIsNotNone(train_gen)

    #
    # checks that a generator is made with many graphs using only some of them
    #
    def test_get_testing_generator_partial_large(self):
        classifier = self.create_large_classifier()

        test_gen = classifier._get_testing_generator(range(0, int(len(classifier.graphs)/2)))
        self.assertIsNotNone(test_gen)

    #
    # checks that a generator is made with many graphs using all of them
    #
    def test_get_testing_generator_whole_large(self):
        classifier = self.create_large_classifier()

        test_gen = classifier._get_testing_generator(range(0, len(classifier.graphs)))
        self.assertIsNotNone(test_gen)

    #
    # checks that a model is made with many graphs using only some of them without repetition
    #
    def test_train_model_partial_unique_large(self):
        classifier = self.create_large_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator(range(0, int(len(classifier.graphs)/4)))
        test_gen = classifier._get_testing_generator(range(int(len(classifier.graphs)/4), int(len(classifier.graphs)/2)))
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with many graphs using only some of them with repetition
    #
    def test_train_model_partial_repeating_large(self):
        classifier = self.create_large_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator(range(0, int(len(classifier.graphs)/3)))
        test_gen = classifier._get_testing_generator(range(int(len(classifier.graphs)/4), int(len(classifier.graphs)/2)))
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with many graphs using all of them without repetition
    #
    def test_train_model_whole_unique_large(self):
        classifier = self.create_large_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator(range(0, int(len(classifier.graphs)/2)))
        test_gen = classifier._get_testing_generator(range(int(len(classifier.graphs)/2), len(classifier.graphs)))
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that a model is made with many graphs using all of them with repetition
    #
    def test_train_model_whole_repeating_large(self):
        classifier = self.create_large_classifier()
        
        classifier.model = classifier._create_graph_classification_model()
        train_gen = classifier._get_training_generator(range(0, len(classifier.graphs)))
        test_gen = classifier._get_testing_generator(range(0, len(classifier.graphs)))
        classifier._train_model(train_gen, test_gen)

        self.assertIsNotNone(classifier.model)

    #
    # checks that the test returns an accuracy score with many graphs using only some of them
    #
    def test_test_model_partial_large(self):
        classifier = self.create_large_classifier()

        classifier.model = classifier._create_graph_classification_model()
        test_gen = classifier._get_testing_generator(range(0, int(len(classifier.graphs)/2)))
        acc = classifier._test_model(test_gen)

        self.assertEqual(type(acc), float)
        self.assertTrue(acc >= 0 and acc <= 1)

    #
    # checks that the test returns an accuracy score with many graphs using all of them
    #
    def test_test_model_whole_large(self):
        classifier = self.create_large_classifier()

        classifier.model = classifier._create_graph_classification_model()
        test_gen = classifier._get_testing_generator(range(0, len(classifier.graphs)))
        acc = classifier._test_model(test_gen)

        self.assertEqual(type(acc), float)
        self.assertTrue(acc >= 0 and acc <= 1)

    # 
    # checks that a model is producted by training with many graphs
    # 20% testing graphs and 80% training graphs
    # 
    def test_train_large(self):
        classifier = self.create_large_classifier()

        classifier.model = classifier._create_graph_classification_model()
        classifier.train()

        self.assertIsNotNone(classifier.model)

    #
    # checks that the mean and sd are returned by evaluating the model with many graphs
    # 10 folds with 5 repetition
    #
    def test_evaluate_large(self):
        classifier = self.create_large_classifier()

        classifier.model = classifier._create_graph_classification_model()
        mean, sd = classifier.evaluate()

        self.assertEqual(type(mean), float)
        self.assertEqual(type(sd), float)

    #
    # tests that a prediction is made with many graphs
    #
    def test_predict_large(self):
        classifier = self.create_large_classifier()

        classifier.model = classifier._create_graph_classification_model()
        predictions = classifier.predict()

        self.assertEqual(type(predictions), np.ndarray)
        for prediction in predictions:
            self.assertEqual(type(prediction[0]), np.float32)
            self.assertTrue(prediction[0] >= 0 and prediction[0] <= 1)

if __name__ == '__main__':
    unittest.main()