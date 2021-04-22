# -*- coding: utf-8 -*-
"""
Convolutional Neural Network model implementation for "20 Newsgroups"

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.data.utils import util
from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.tf import NeuralNetworkClassification

import numpy as np

import pandas as pd

from sklearn.preprocessing import LabelEncoder

import tensorflow.compat.v1 as tf

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """
    Neural Network model implementation for "20 Newsgroups"

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """

    def __init__(self):
        super().__init__()
        self._classifier_type = 'mlnn'
        self.label_encoder = None

    def setup_model(self):

        self.optimizer = 'Adam'
        # As an alternative:
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #   learning_rate=0.015)

        self.epochs = 50
        self.batch_size = 250
        self.metrics = ['accuracy']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        # As an alternative, define the loss function with a string

        self.regularization_param = 1e-3
        self.regularizer_dict = {
            'kernel_regularizer': tf.keras.regularizers.l2(
                self.regularization_param)  # ,
            # 'activity_regularizer': tf.keras.regularizers.l2(
            #    self.regularization_param),
            # 'bias_regularizer': tf.keras.regularizers.l2(
            #    self.regularization_param)
        }
        print('Setting up a multilayer neural network...')
        self.model = self._get_mlnn_model()

    def _get_mlnn_model(self, which_model='ml-leaks_paper'):

        n_in = self._num_features
        n_out = self._num_classes

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):
            # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py
            num_units_hidden_layer = 128
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(num_units_hidden_layer,
                                      activation='tanh',
                                      **self.regularizer_dict
                                      ),
                tf.keras.layers.Dense(n_out, activation='softmax')
            ]
            )
        else:
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(n_out, activation='softmax')]
            )

        model.summary()
        return model

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        X, y = self.data_source.read()

        # check data format
        if isinstance(X, pd.DataFrame):
            X = X.values
        else:
            if not isinstance(X, np.ndarray):
                raise Exception('X is not np.ndarray')

        if isinstance(y, pd.Series):
            y = y.values
        else:
            if not isinstance(y, np.ndarray):
                raise Exception('y is not np.ndarray')

        # prepare data
        if y.ndim == 2:
            # make non-dimensional array (just to avoid Warnings by Sklearn)
            y = np.ravel(y)

        self._num_features = X.shape[1]

        # WARNING: np.nan, np.Inf in y are counted as classes by np.unique
        self._num_classes = len(np.unique(y))  # np.ravel(y)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        # if self.label_encoder is None:
        #   print('Retraining')
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y)

        # back to column vector. Transform one-dimensional array into column
        # vector via newaxis
        y = y[:, np.newaxis]

        # set attributes
        self.X_train = X
        self.y_train = y
        self.X_test = None
        self.y_test = None

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            print('\nAttached test dataset to user model. Feature matrix '
                  'shape:', self.X_test.shape)
            print('Class-labels vector shape:', self.y_test.shape)
