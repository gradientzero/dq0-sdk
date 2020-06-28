# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

This can be used as a base class for UserModel definitions.

Example:
    >>> import dq0sdk.models.tf.NeuralNetworkClassification # doctest: +SKIP
    >>>
    >>> class MyAwsomeModel(NeuralNetwork): # doctest: +SKIP
    >>>     def __init__(self, model_path): # doctest: +SKIP
    >>>         super().__init__(model_path) # doctest: +SKIP
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

from dq0sdk.models.model import Model

import tensorflow.compat.v1 as tf
import numpy as np


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Note:
        fit, predict, and evaluate functions will be overriden at runtime
        when executed inside the DQ0 quarantine instance.

    Attributes:
        model_path (:obj:`str`): path of model (save / load)
    """
    def __init__(self, model_path):
        super().__init__(model_path)

        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def predict(self, x):
        """Model predict function.

        Model scoring.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model.save('{}/{}/{}.h5'.format(self.model_path, version, name),
                        include_optimizer=False)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model = tf.keras.models.load_model(
            '{}/{}/{}.h5'.format(
                self.model_path, version, name),
            compile=False)

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
                       'y_test': self.y_test, 'model_path': self.model_path}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.model_path = None
        self.data_source = None

        # model clone
        # new_model = self.__class__(model_path=None)
        new_model = copy.deepcopy(self)
        new_model.model = new_keras_model

        # recover attributes temporarily removed for efficient deep copying
        for key, value in tmp_storage.items():
            self.__setattr__(key, value)

        return new_model
