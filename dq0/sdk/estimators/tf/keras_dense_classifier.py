# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
import tensorflow as tf

from dq0.sdk.estimators.data_handler.base import BasicDataHandler
from dq0.sdk.estimators.base_mixin import ClassifierMixin
from dq0.sdk.estimators.tf.keras_base import NN_Classifier

logger = logging.getLogger(__name__)


class Keras_Dense_Classifier_OHE(NN_Classifier, ClassifierMixin, BasicDataHandler):
    """Keras sequential dense estimator for classification with OHE targets."""

    def __init__(self, optimizer='Adam',
                 loss=tf.keras.losses.CategoricalCrossentropy(),
                 metrics=['accuracy', 'mae'], batch_size=250, epochs=2, **kwargs):
        # TODO: finish the comments
        """
        Args:

        """
        super().__init__(**kwargs)
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_type = 'NeuralNetworkClassification'

    def setup_model(self, input_shape=None, n_classes=None, n_layers=[10, 10], **kwargs):
        """Args:
            n_layers: list of int, for every element a layer with the number of units given in the list
        """
        # TODO: move the setup model back to the init, so that we can set all parameters when we init the models
        # Create Network architecture
        if input_shape is None:
            input_shape = self.input_dim
        if n_classes is None:
            n_classes = self.out_shape
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = _layer_factory(layers, n_layers)
        layers.append(tf.keras.layers.Dense(n_classes, activation='softmax'))

        self.model = tf.keras.Sequential(layers)


class Keras_Dense_Classifier_Integer(NN_Classifier, ClassifierMixin, BasicDataHandler):

    def __init__(self, optimizer='Adam',
                 loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                 metrics=['accuracy', 'mae'], batch_size=250, epochs=2, **kwargs):
        # TODO: finish the comments
        """
        Args:
            n_layers: list of int, for every element a layer with the number of units given in the list

        """
        super().__init__(**kwargs)
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_type = 'NeuralNetworkClassification'

    def setup_model(self, input_shape=None, n_classes=None, n_layers=[10, 10], **kwargs):
        """Args:
            n_layers: list of int, for every element a layer with the number of units given in the list
        """
        if input_shape is None:
            input_shape = self.input_dim
        if n_classes is None:
            n_classes = self.out_shape
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = _layer_factory(layers, n_layers)
        layers.append(tf.keras.layers.Dense(n_classes, activation='softmax'))

        self.model = tf.keras.Sequential(layers)


class Keras_Dense_Classifier_Binary(NN_Classifier, ClassifierMixin, BasicDataHandler):

    def __init__(self, optimizer='Adam',
                 loss=tf.keras.losses.BinaryCrossentropy(),
                 metrics=['accuracy', 'mae'], batch_size=250, epochs=2, **kwargs):
        # TODO: finish the comments
        """
        Args:
            n_layers: list of int, for every element a layer with the number of units given in the list

        """
        super().__init__(**kwargs)
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_type = 'NeuralNetworkClassification'
    
    def setup_model(self, input_shape=None, n_classes=None, n_layers=[10, 10], **kwargs):
        """Args:
            n_layers: list of int, for every element a layer with the number of units given in the list
        """
        if input_shape is None:
            input_shape = self.input_dim
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = _layer_factory(layers, n_layers)
        layers.append(tf.keras.layers.Dense(1, activation='sigmoid'))

        self.model = tf.keras.Sequential(layers)


def _layer_factory(layers, n_layers):
    """Helper function to create the layers given some parameters."""
    # TODO: increase the functionality
    for n in n_layers:
        layers.append(tf.keras.layers.Dense(units=n, activation='tanh'))
    return layers
