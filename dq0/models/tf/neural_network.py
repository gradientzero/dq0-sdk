# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow_privacy.privacy.optimizers import dp_optimizer

from dq0.models import Model


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self):
        super().__init__()

    def setup(self, **kwargs):
        """Setup function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        model = keras.Sequential([
            keras.layers.Input(len(kwargs['feature_columns'])),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')]
        )
        return model

    def fit(self, **kwargs):
        """Model fit function.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns

        Returns:
            model: fitted model.
        """
        preprocessed_data = kwargs['preprocessed_data']
        feature_columns = kwargs['feature_columns']
        target_column = kwargs['target_column']

        nn = self.setup(**kwargs)

        optimizer = dp_optimizer.GradientDescentOptimizer(learning_rate=0.15)
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        nn.compile(optimizer=optimizer, loss=loss, metrics=['accuracy', 'mse'])
        nn.fit(
            preprocessed_data[feature_columns],
            preprocessed_data[target_column],
            epochs=10,
            verbose=0)

        return nn

    def fit_dp(self, **kwargs):
        """Model fit with differential privacy.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns

        Returns:
            model: fitted model.
        """
        preprocessed_data = kwargs['preprocessed_data']
        feature_columns = kwargs['feature_columns']
        target_column = kwargs['target_column']

        nn = self.setup(**kwargs)

        # DPSGD Training
        optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
            l2_norm_clip=1.0,
            noise_multiplier=1.1,
            num_microbatches=250,
            learning_rate=0.15)
        # Compute vector of per-example loss rather than
        # its mean over a minibatch.
        loss = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True,
            reduction=tf.compat.v1.losses.Reduction.NONE)

        nn.compile(optimizer=optimizer, loss=loss, metrics=['accuracy', 'mse'])

        nn.fit(
            preprocessed_data[feature_columns],
            preprocessed_data[target_column],
            epochs=10,
            verbose=0,
            batch_size=250)

        return nn

    def predict(self, **kwargs):
        """Model predict function.

        Implementing child classes will perform model scoring here.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        pass
