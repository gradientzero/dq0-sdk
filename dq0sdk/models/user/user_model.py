
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

from sklearn.preprocessing import LabelEncoder

import tensorflow as tf

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    """
    Convolutional Neural Network model implementation for Cifar10

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path, **kwargs):
        super().__init__(model_path)
        self.model_type = 'keras'
        self._classifier_type = 'cnn'  # kwargs['classifier_type']
        self.label_encoder = None

        # @Jona
        self.DP_enabled = False
        self.DP_epsilon = False

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

        # network topology.
        # if self._classifier_type.startswith('DP-'):
        #    network_type = self._classifier_type[3:]
        # else:
        #    network_type = self._classifier_type
        # if util.case_insensitive_str_comparison(network_type, 'cnn'):
        print('Setting up a multilayer convolution neural network...')
        self.model = self._get_cnn_model(self._num_classes)

    def setup_data(self):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        # @Jona
        X_train, y_train, X_test, y_test = source.read(num_instances_to_load=10000)

        assert isinstance(X_train, np.ndarray)
        assert isinstance(y_train, np.ndarray)

        # @Jona
        # X_train = source.preprocess(X=X_train)
        # X_test = source.preprocess(X=X_test)

        # np.nan, np.Inf in y_train are counted as classes in the following
        # line
        self._num_classes = len(np.unique(np.ravel(y_train)))

        # make non-dimensional array (just to avoid Warnings by Sklearn)
        if y_train.ndim == 2:
            y_train = np.ravel(y_train)
        if y_test.ndim == 2:
            y_test = np.ravel(y_test)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        # if self.label_encoder is None:
        #   print('Retraining')
        self.label_encoder = LabelEncoder()
        y_train = self.label_encoder.fit_transform(y_train)
        y_test = self.label_encoder.transform(y_test)

        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        print('\n\nDEBUG: in user_model.setup_data: self.X_train.shape ',
              self.X_train.shape)
        print('DEBUG: in user_model.setup_data: self.y_train.shape ',
              self.y_train.shape, '\n\n')

        print('\n\nDEBUG: in user_model.setup_data: self.X_TEST.shape ',
              self.X_test.shape)
        print('DEBUG: in user_model.setup_data: self.y_TEST.shape ',
              self.y_test.shape, '\n\n')