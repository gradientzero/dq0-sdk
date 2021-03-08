# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
import tensorflow as tf

from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import ClassifierMixin
from dq0.sdk.estimators.tf.keras_base import NN_Classifier

logger = logging.getLogger(__name__)


class Keras_Dense_Classifier_OHE(NN_Classifier, ClassifierMixin, Estimator):
    """Keras sequential dense estimator for classification with OHE targets."""

    def __init__(self, input_shape, n_classes, n_layers=[10, 10], optimizer='Adam',
                 loss=tf.keras.losses.CategoricalCrossentropy(),
                 metrics=['accuracy', 'mae']):
        # TODO: finish the comments
        """
        Args:
            n_layers: list of int, for every element a layer with the number of units given in the list

        """
        super().__init__()
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        # Create Network architecture
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = _layer_factory(layers, n_layers)
        layers.append(tf.keras.layers.Dense(n_classes, activation='softmax'))

        self.model = tf.keras.Sequential(layers)


class Keras_Dense_Classifier_Integer(NN_Classifier, ClassifierMixin, Estimator):

    def __init__(self, input_shape, n_classes, n_layers=[10, 10], optimizer='Adam',
                 loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                 metrics=['accuracy', 'mae']):
        # TODO: finish the comments
        """
        Args:
            n_layers: list of int, for every element a layer with the number of units given in the list

        """
        super().__init__()
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        # Create Network architecture
        layers = [tf.keras.layers.Input(shape=input_shape)]
        layers = _layer_factory(layers, n_layers)
        layers.append(tf.keras.layers.Dense(n_classes, activation='softmax'))

        self.model = tf.keras.Sequential(layers)


class Keras_Dense_Classifier_Binary(NN_Classifier, ClassifierMixin, Estimator):

    def __init__(self, input_shape, n_layers=[10, 10], optimizer='Adam',
                 loss=tf.keras.losses.BinaryCrossentropy(),
                 metrics=['accuracy', 'mae']):
        # TODO: finish the comments
        """
        Args:
            n_layers: list of int, for every element a layer with the number of units given in the list

        """
        super().__init__()
        # define for fit, compile is excecuted just before fit is called
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        # Create Network architecture
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
