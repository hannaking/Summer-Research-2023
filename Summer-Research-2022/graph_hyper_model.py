import keras_tuner
import numpy as np
from sklearn import model_selection
from keras.callbacks import EarlyStopping

class CVTuner(keras_tuner.RandomSearch):

    def run_trial(self, trial, generator, graphs, labels, k, folds, batch_size=32, epochs=1, es=EarlyStopping()):
        cv = model_selection.RepeatedStratifiedKFold(n_splits=folds, n_repeats=k)

        eval = []
        for train_indices, test_indices in cv.split(labels, labels):
            train_y = labels.iloc[train_indices].values
            test_y = labels.iloc[test_indices].values
            
            train_gen = generator.flow(train_indices, targets=train_y, batch_size=batch_size)
            test_gen  = generator.flow(test_indices,  targets=test_y,  batch_size=batch_size)
            
            model = self.hypermodel.build(trial.hyperparameters)
            
            model.fit(train_gen, epochs=epochs, validation_data=test_gen, verbose=0, callbacks=[es])
            
            eval.append(model.evaluate(test_gen, verbose=1)[1])
        print(eval)
        self.oracle.update_trial(trial.trial_id, {'eval': np.mean(eval)})
