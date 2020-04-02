
"""
Neural network Model class

Basic Tensorflow neural-network implementation using Keras.

Todo:
    * Protect Keras compile and fit functions

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>

Copyright 2019, Gradient Zero
"""

import logging

from dq0sdk.data.utils import util
from dq0sdk.models.tf.neural_network import NeuralNetwork

import numpy as np

import pandas as pd

from sklearn.preprocessing import LabelEncoder

import tensorflow as tf

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    """
    Convolutional Neural Network model implementation for "20 Newsgroups"

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'keras'
        self._classifier_type = 'mlnn'
        self.label_encoder = None

        self.DP_enabled = False
        self.DP_epsilon = None

    def _get_cnn_model(self, n_out, which_model='ml-leaks_paper'):

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):

            # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py

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
            model.add(tf.keras.layers.Dense(n_out, activation='softmax'))

        elif util.case_insensitive_str_comparison(which_model, 'tf_tutorial'):

            # https://www.tensorflow.org/tutorials/images/cnn

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
            model.add(tf.keras.layers.Dense(n_out, activation='softmax'))

        model.summary()
        return model

    def setup_model(self):

        self.learning_rate = 0.001  # 0.15
        self.epochs = 50  # 50 in ML-leaks paper
        self.verbose = 2
        self.metrics = ['accuracy']
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
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        X, y = source.read()

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
