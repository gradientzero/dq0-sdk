# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork

import tensorflow as tf


class NeuralNetworkRegression(NeuralNetwork):
    """Neural Network model implementation.

    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'NeuralNetworkRegression'
        self.metrics = ['mean_squared_error']

    def fit(self):
        """Model fit function.
        """
        # optimizer = tf.keras.optimizers.SGD(learning_rate=self.learning_rate)
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        loss = tf.keras.losses.MeanSquaredError()
        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=self.metrics)
        self.model.fit(self.X_train,
                       self.y_train,
                       batch_size=self.num_microbatches,
                       epochs=self.epochs,
                       verbose=self.verbose)
