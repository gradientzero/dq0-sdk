# -*- coding: utf-8 -*-
"""Neural network Model class for patient dataset:
https://synthea.mitre.org/downloads



Copyright 2020, Gradient Zero
"""

import logging

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.utils import util
from dq0sdk.models.tf.neural_network_regression import NeuralNetworkRegression

import numpy as np

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection

import tensorflow as tf
from tensorflow import keras

logger = logging.getLogger()


class PatientModel(NeuralNetworkRegression):

    def __init__(self):
        super().__init__()

        self.DP_enabled = False
        self.DP_epsilon = False

        self.learning_rate = 0.001
        self.epochs = 10000
        self.optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.loss = keras.losses.MeanSquaredError()
        


    def setup_data(self):
        
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        data = source.read()
        X, y = source.prepare_data(data)

        self.input_dim  = X.shape[1]
        self.batch_size = X.shape[0]
        self.num_microbatches = self.batch_size

        X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y)
        
        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            print('\nAttached test dataset to user model. Feature matrix '
                  'shape:', self.X_test.shape)
            print('Class-labels vector shape:', self.y_test.shape)
        

    def setup_model(self):
        self.model = keras.Sequential([
                    keras.layers.Input(self.input_dim),
                    keras.layers.Dense(1000, activation='tanh'),
                    keras.layers.Dense(1000, activation='tanh'),
                    keras.layers.Dense(1, activation='linear')]
                )

