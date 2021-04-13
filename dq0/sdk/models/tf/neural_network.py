# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

This can be used as a base class for UserModel definitions.

Example:
    >>> import dq0.sdk.models.tf.NeuralNetworkClassification # doctest: +SKIP
    >>>
    >>> class MyAwsomeModel(NeuralNetwork): # doctest: +SKIP
    >>>     def __init__(self): # doctest: +SKIP
    >>>         super().__init__() # doctest: +SKIP
    >>>
    >>>     def setup_data(self): # doctest: +SKIP
    >>>         # do something
    >>>         pass # doctest: +SKIP
    >>>
    >>>     def setup_model(self): # doctest: +SKIP
    >>>         # freely deinfe the tf / keras model
    >>>         pass # doctest: +SKIP
    >>>
    >>> if __name__ == "__main__": # doctest: +SKIP
    >>>     myModel = MyAwsomeModel() # doctest: +SKIP
    >>>     myModel.setup_data() # doctest: +SKIP
    >>>     myModel.setup_model() # doctest: +SKIP
    >>>     myModel.fit() # doctest: +SKIP
    >>>     myModel.save() # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import copy
import logging

from dq0.sdk.data.utils import util
from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.model import Model

import numpy as np

import tensorflow.compat.v1 as tf


logger = logging.getLogger()


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Note:
        fit, predict, and evaluate functions will be overriden at runtime
        when executed inside the DQ0 quarantine instance.
    """

    def __init__(self):
        super().__init__()

        # child classes must set following attributes
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.optimizer = None
        self.loss = None
        self.metrics = None
        self.batch_size = None
        self.epochs = None

    def predict(self, x):
        """Model predict function.

        Model scoring.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def save(self, path):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            path (:obj:`str`): The model path
        """
        self.model.save(path)

    def load(self, path):
        """Loads the model.

        Load the model from local storage.

        Args:
            path (:obj:`str`): The model path
        """
        self.model = tf.keras.models.load_model(path)

    def get_clone(self, trained=False):
        """
        Generates a new model with the same parameters, if they are not fit on
        the training data.

        Generates a deep copy of the model without actually
        copying any attached dataset. It yields a new model with the same
        parameters that has not been fit on any data. Parameters fit to
        the training data like, e.g., model weights, are re-initialized in the
        clone.

        Args:
            trained: if `True`, maintains current state including trained model
                weights, etc. Otherwise, returns an unfitted model with the same
                initialization params.

        Returns:
            deep copy of model

        """

        # "clone_model" creates new layers (and thus new weights) for the clone
        new_keras_model = tf.keras.models.clone_model(self.model)
        if trained:
            new_keras_model.set_weights(self.model.get_weights())

        # check
        all_close = all(
            [np.allclose(self.model.get_weights()[lc],
                         new_keras_model.get_weights()[lc]) for lc in range(
                len(self.model.get_weights()))]
        )
        if trained:
            assert all_close
        else:
            assert not all_close

        # performance boosting: do not (deep) copy any data that will be
        # discarded immediately after deep copying
        tmp_storage = {'model': self.model, 'X_train': self.X_train,
                       'y_train': self.y_train, 'X_test': self.X_test,
                       'y_test': self.y_test}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.data_source = None

        # model clone
        # new_model = self.__class__()
        new_model = copy.deepcopy(self)
        new_model.model = new_keras_model

        # recover attributes temporarily removed for efficient deep copying
        for key, value in tmp_storage.items():
            self.__setattr__(key, value)

        return new_model

    def fit(self, verbose=0):
        """
        Model fit function learning a model from training data
        """
        if self.model is None:
            fatal_error('No TensorFlow model provided!', logger=logger)

        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        # work on deep copy of data because
        # "fix_limitation_of_Keras_fit_and_predict_functions" modifies the
        # dataset is gets as input
        tmp_X_train = copy.deepcopy(self.X_train)
        tmp_y_train = copy.deepcopy(self.y_train)
        tmp_X_train, tmp_y_train = \
            fix_limitation_of_Keras_fit_and_predict_functions(
                tmp_X_train, tmp_y_train, self.batch_size
            )
        self.model.fit(tmp_X_train,
                       tmp_y_train,
                       epochs=self.epochs,
                       verbose=verbose,
                       batch_size=self.batch_size)

        if hasattr(self, '_classifier_type'):
            partial_str = ' ' + self._classifier_type
        else:
            partial_str = ''
        print('\nLearned a' + partial_str + ' model from',
              self.X_train.shape[0], 'examples.')

    def evaluate(self, test_data=True, verbose=0):
        """Model evaluate implementation.

        Args:
            test_data (bool): False to use train data instead of test
                Default is True.
            verbose (int): Verbose level, Default is 0
        """

        if self.model is None:
            fatal_error('No  TensorFlow model provided!', logger=logger)

        # Check for valid model setup
        if not test_data and not hasattr(self, 'X_train'):
            fatal_error('Missing argument in model: X_train', logger=logger)
        if not test_data and not hasattr(self, 'y_train'):
            fatal_error('Missing argument in model: y_train', logger=logger)
        if test_data and not hasattr(self, 'X_test'):
            fatal_error('Missing argument in model: X_test', logger=logger)
        if test_data and not hasattr(self, 'y_test'):
            fatal_error('Missing argument in model: y_test', logger=logger)
        if not hasattr(self, 'batch_size'):
            fatal_error('Missing argument in model: batch_size', logger=logger)

        # work on deep copy of data because
        # "fix_limitation_of_Keras_fit_and_predict_functions" modifies the
        # dataset is gets as input
        X = copy.deepcopy(self.X_test) if test_data else copy.deepcopy(
            self.X_train)
        y = copy.deepcopy(self.y_test) if test_data else copy.deepcopy(
            self.y_train)

        # If all the data to be predicted do not fit in the CPU/GPU RAM at
        # the same time, predictions are done in batches.
        X, y = fix_limitation_of_Keras_fit_and_predict_functions(
            X, y, self.batch_size
        )

        result = self.model.evaluate(x=X,
                                     y=y,
                                     batch_size=self.batch_size,
                                     verbose=verbose)

        util.print_evaluation_res(
            dict(zip(self.model.metrics_names, result)),
            'test' if test_data else 'training',
            model_metrics=self.metrics
        )

        return dict(zip(self.model.metrics_names, result))


def fix_limitation_of_Keras_fit_and_predict_functions(X, y, batch_size):
    """
    Fix limitation of Keras "fit", "predict" and "evaluate" functions.

    Limitation of Keras "fit" function: size of training dataset (
    i.e., number of training samples) must be divisible by the minibatch
    size ("batch_size" parameter).

    This function removes above limitation by making training robust for
    any number of minibatches.

    The same limitation holds for Keras "evaluate" and "predict" functions,
    too. In the case of "evaluate" and "predict", if all the data to be
    predicted do not fit in the CPU/GPU RAM at the same time, predictions
    are done in batches.
    Args:
        X: data matrix
        y: learning signal
        batch_size: batch size set in user model

    Returns:
        X, y
    """

    tr_dataset_size = X.shape[0]
    # floor division
    num_minibatches = tr_dataset_size // batch_size
    if num_minibatches <= 0:
        num_minibatches = 1

    X = X[:num_minibatches * batch_size]
    y = y[:num_minibatches * batch_size]

    return X, y
