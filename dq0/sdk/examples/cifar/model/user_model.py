# -*- coding: utf-8 -*-
"""Neural Network model for CIFAR-10 image dataset.

Use this class to train a classifier on CIFAR-10 image data.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.data.utils import util
from dq0.sdk.models.tf import NeuralNetworkClassification

import numpy as np

import pandas as pd

from sklearn.preprocessing import LabelEncoder

import tensorflow.compat.v1 as tf

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """
    Convolutional Neural Network model implementation for Cifar-10 image data.

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Args:
        model_path (str): Path to the model save destination.

    Attributes:
        model_type (:obj:`str`): type of this model instance. Options: 'keras'.
        label_encoder (:obj:`sklearn.preprocessing.LabelEncoder`): sklearn
        class label encoder.
    """

    def __init__(self, model_path):
        super().__init__(model_path)
        self._classifier_type = 'cnn'
        self.label_encoder = None

    def _get_cnn_model(self, which_model='ml-leaks_paper'):

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):

            model = tf.keras.Sequential()
            # create the convolutional base
            model.add(tf.keras.layers.Conv2D(32, (5, 5), activation='relu',
                                             input_shape=(32, 32, 3), **self.regularizer_dict))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(32, (5, 5), activation='relu',
                                             **self.regularizer_dict))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))

            # add dense layers on top
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(128, activation='tanh',
                                            **self.regularizer_dict))
            model.add(tf.keras.layers.Dense(self._num_classes, activation='softmax'))

        elif util.case_insensitive_str_comparison(which_model, 'tf_tutorial'):

            model = tf.keras.Sequential()
            # create the convolutional base
            model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                                             input_shape=(32, 32, 3)))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

            # add dense layers on top
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            model.add(tf.keras.layers.Dense(self._num_classes, activation='softmax'))

        model.summary()
        return model

    def setup_model(self):
        """Setup model function

        Define the CNN model.
        """

        self.optimizer = 'Adam'
        # As an alternative:
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #   learning_rate=0.001)
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
        print('Setting up a convolution neural network...')
        self.model = self._get_cnn_model()

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
            logger.error('No data source found')
            return

        X, y = self.data_source.read()  # num_instances_to_load=10000

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

        # np.nan, np.Inf in y are counted as classes by np.unique
        self._num_classes = len(np.unique(y))  # np.ravel(y)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
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
