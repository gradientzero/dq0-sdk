# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork

import tensorflow.compat.v1 as tf


class NeuralNetworkRegression(NeuralNetwork):
    """Neural Network model implementation.

    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'NeuralNetworkRegression'
        self.metrics = ['mean_squared_error']

    def to_string(self):
        print('\nModel type is: ', self.model_type)

    def fit(self):
        """Model fit function.
        """

        x = self.X_train
        y = self.y_train
        steps_per_epoch = self.X_train.shape[0] // self.num_microbatches
        x = x[:steps_per_epoch * self.num_microbatches]
        y = y[:steps_per_epoch * self.num_microbatches]

        loss = tf.keras.losses.MeanSquaredError()
        self.model.compile(optimizer=self.optimizer,
                           loss=loss,
                           metrics=self.metrics)
        self.model.fit(x,
                       y,
                       batch_size=self.num_microbatches,
                       epochs=self.epochs,
                       verbose=self.verbose)
