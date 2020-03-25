
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

import os
import warnings

from dq0sdk.data.utils import util
from dq0sdk.models.model import Model
from dq0sdk.models.tf.neural_network import NeuralNetwork

import numpy as np

import pandas as pd

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

import tensorflow as tf  # no GPU support for Mac. In any case,
# NVIDIA GPU card with CUDA is required.
# from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


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

        # if 'saved_model_folder' in kwargs:
        #    self._saved_model_folder = kwargs['saved_model_folder']
        # else:
        #    self._saved_model_folder = './data/output'
        self._classifier_type = 'cnn'  # kwargs['classifier_type']
        self._num_classes = 10

        self._label_encoder = None

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
        # to inherit from abstract base class
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
        # TODO: grid search over parameters space

        # network topology. TODO: make it parametric!
        if self._classifier_type.startswith('DP-'):
            network_type = self._classifier_type[3:]
        else:
            network_type = self._classifier_type
        if util.case_insensitive_str_comparison(network_type, 'cnn'):
            print('Setting up a multilayer convolution neural network...')
            self._model = self._get_cnn_model(self._num_classes)

    def setup_data(self):
        if y_np_a.ndim == 2:
            # make non-dimensional array (just to avoid Warnings by Sklearn)
            y_np_a = np.ravel(y_np_a)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        if self._label_encoder is None:
            # self._label_encoder is None => y contains train labels
            self._label_encoder = LabelEncoder()
            y_encoded_np_a = self._label_encoder.fit_transform(y_np_a)
        else:
            y_encoded_np_a = self._label_encoder.transform(y_np_a)

        return y_encoded_np_a
