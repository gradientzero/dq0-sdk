#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult dataset example.
Neural network model definition

@author: Wolfgang Gross <wg@gradient0.com>
"""

import sklearn
import sklearn.preprocessing
import pandas as pd
from tensorflow import keras

from dq0.data_connector import preprocessing
import dq0


class NeuralNetwork_adult(dq0.models.tf.neural_network.NeuralNetwork):
    def __init__(self, model_path='.'):
        super().__init__()
        self.learning_rate = 0.3
        self.input_dim = None
        self.model_path = model_path

    def setup_data(self, X_df, y_ts, quantitative_features_list, num_tr_instances):
        # Scale values to the range from 0 to 1; to be precessed by the neural network
        X_df[quantitative_features_list] = sklearn.preprocessing.minmax_scale(X_df[quantitative_features_list])

        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)  # test to label
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)

        X_train_df, X_test_df, y_train_ts, y_test_ts = preprocessing.train_test_split(X_df, y_bin, num_tr_instances)
        self.input_dim = X_train_df.shape[1]

        return X_train_df, X_test_df, y_train_ts, y_test_ts

    def setup_model(self):
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])

