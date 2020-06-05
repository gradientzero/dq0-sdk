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

from dq0sdk.models.model import Model

import tensorflow.compat.v1 as tf


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
