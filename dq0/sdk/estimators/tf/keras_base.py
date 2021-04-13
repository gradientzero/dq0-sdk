# -*- coding: utf-8 -*-
"""Base tensorflow keras classes for all estimator subclasses

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.mod_utils.modules import parse_kwargs, parse_value
from dq0.sdk.estimators.estimator import Estimator

import numpy as np

import tensorflow as tf


logger = logging.getLogger(__name__)


class NeuralNetworkBase(Estimator):
    """Base TF Network mixin."""

    def fit(self, X, y, **kwargs):
        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)
        if 'epochs' in kwargs:
            epochs = kwargs.pop('epochs')
            self.model.fit(X, y, epochs=epochs, **kwargs)
        elif hasattr(self, 'epochs'):
            self.model.fit(X, y, epochs=self.epochs, **kwargs)
        else:
            self.model.fit(X, y, **kwargs)

    def setup_data(self, data_handler_instance='CSV', pipeline_steps=None, pipeline_config_path=None, **kwargs):
        """Keras NN specific setup data. To get the input and output dimensions from the data handler."""
        super().setup_data(data_handler_instance, pipeline_steps=None, pipeline_config_path=None, **kwargs)

        # get the input and output dimensions from the data.
        self.input_dim = self.data_handler.get_input_dim(self.X_train)
        self.out_shape = self.data_handler.get_output_dim(self.y_train)


class NN_Classifier(NeuralNetworkBase):
    """Keras neural network classification models with one hot encoded targets."""

    def predict_proba(self, X):
        """Returns the confidence scores."""
        return self.model.predict(X)

    def predict(self, X):
        """Return the class as index on the one-hot-encoding format."""
        return np.argmax(self.model.predict(X), axis=-1)


class NN_Regressor(NeuralNetworkBase):
    """Keras neural network regression models."""

    def predict_proba(self, X):
        return self.predict(X)

    def predict(self, X):
        return self.model.predict(X).flatten()


def _check_param(param, expected_len):
    if type(param) is list:
        if len(param) == expected_len:
            return param
        else:
            return None
    else:
        return [param] * expected_len


def layer_factory(layers, n_layers, **kwargs):  # noqa
    """Helper function to create the layers given some parameters."""
    # check if the length of the given parameter list is as expected
    # if a global setting is given (no list) it is converted into a list

    # parse n_layer param separately
    n_layers = parse_value(n_layers)
    if not type(n_layers) is list:
        n_layers = [n_layers]
    expected_len = len(n_layers)
    kwargs = parse_kwargs(kwargs)
    # activation
    if 'activation' in kwargs:
        activation = _check_param(kwargs['activation'], expected_len)
    else:
        activation = _check_param('tanh', expected_len)
    # use_bias
    if 'use_bias' in kwargs:
        use_bias = _check_param(kwargs['use_bias'], expected_len)
    else:
        use_bias = _check_param(True, expected_len)
    # kernel_initializer
    if 'kernel_initializer' in kwargs:
        kernel_initializer = _check_param(kwargs['kernel_initializer'], expected_len)
    else:
        kernel_initializer = _check_param('glorot_uniform', expected_len)
    # bias_initializer
    if 'bias_initializer' in kwargs:
        bias_initializer = _check_param(kwargs['bias_initializer'], expected_len)
    else:
        bias_initializer = _check_param('zeros', expected_len)
    # kernel_regularizer
    if 'kernel_regularizer' in kwargs:
        kernel_regularizer = _check_param(kwargs['kernel_regularizer'], expected_len)
    else:
        kernel_regularizer = _check_param(None, expected_len)
    # bias_regularizer
    if 'bias_regularizer' in kwargs:
        bias_regularizer = _check_param(kwargs['bias_regularizer'], expected_len)
    else:
        bias_regularizer = _check_param(None, expected_len)
    # activity_regularizer
    if 'activity_regularizer' in kwargs:
        activity_regularizer = _check_param(kwargs['activity_regularizer'], expected_len)
    else:
        activity_regularizer = _check_param(None, expected_len)
    # kernel_constraint
    if 'kernel_constraint' in kwargs:
        kernel_constraint = _check_param(kwargs['kernel_constraint'], expected_len)
    else:
        kernel_constraint = _check_param(None, expected_len)
    # bias_constraint
    if 'bias_constraint' in kwargs:
        bias_constraint = _check_param(kwargs['bias_constraint'], expected_len)
    else:
        bias_constraint = _check_param(None, expected_len)

    for i, n in enumerate(n_layers):
        layers.append(tf.keras.layers.Dense(units=n, activation=activation[i],
                                            use_bias=use_bias[i], kernel_initializer=kernel_initializer[i],
                                            bias_initializer=bias_initializer[i], kernel_regularizer=kernel_regularizer[i],
                                            bias_regularizer=bias_regularizer[i], activity_regularizer=activity_regularizer[i],
                                            kernel_constraint=kernel_constraint[i], bias_constraint=bias_constraint[i]))
    return layers
