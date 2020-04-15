# -*- coding: utf-8 -*-
"""Neural network Model class for patient dataset:

https://synthea.mitre.org/downloads

Copyright 2020, Gradient Zero
"""

import logging

from dq0sdk.models.tf.neural_network_regression import NeuralNetworkRegression


logger = logging.getLogger()


class UserModel(NeuralNetworkRegression):
    """Derived from dq0sdk.models.tf.NeuralNetworkRegression class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path, **kwargs):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        from sklearn.model_selection import train_test_split

        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        data = source.read()
        X, y = source.prepare_data(data)

        self.input_dim = X.shape[1]
        self.batch_size = X.shape[0]
        self.num_microbatches = self.batch_size

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        from tensorflow import keras

        self.learning_rate = 0.001
        self.epochs = 10  # 10000
        self.optimizer = 'Adam'
        self.loss = keras.losses.MeanSquaredError()

        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(1000, activation='tanh'),
            keras.layers.Dense(1000, activation='tanh'),
            keras.layers.Dense(1, activation='linear')]
        )
