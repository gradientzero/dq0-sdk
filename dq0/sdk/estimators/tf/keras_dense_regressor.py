# -*- coding: utf-8 -*-
""" Keras dense neural networks for regression targets.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
import tensorflow as tf
from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import RegressorMixin
from dq0.sdk.estimators.tf.keras_base import NN_Regressor, layer_factory

logger = logging.getLogger(__name__)


class Keras_Dense_Regressor(NN_Regressor, RegressorMixin, Estimator):

    def __init__(self, optimizer='Adam',
                 loss=tf.keras.losses.MeanAbsoluteError(),
                 metrics=['mae'], batch_size=250, epochs=2, n_layers=[10, 10], **kwargs):
        super().__init__(**kwargs)
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_type = 'NeuralNetworkRegression'
        # Auto setup
        if ('input_shape' in kwargs):
            input_shape = kwargs.pop('input_shape')
            self.setup_model(input_shape=input_shape, n_layers=n_layers, optimizer=optimizer,
                             loss=loss, metrics=metrics, batch_siz=batch_size, epochs=epochs,
                             **kwargs)

    def setup_model(self, input_shape=None, n_layers=[10, 10],
                    optimizer='Adam', loss=tf.keras.losses.MeanAbsoluteError(),
                    metrics=['mae'], batch_size=250, epochs=2, **kwargs):
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.batch_size = int(batch_size)
        self.epochs = int(epochs)
        if input_shape is None:
            input_shape = self.input_dim
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = layer_factory(layers, n_layers, **kwargs)
        layers.append(tf.keras.layers.Dense(1, activation='linear'))

        self.model = tf.keras.Sequential(layers)
