#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult dataset example.
Neural network model definition

@author: Wolfgang Gross <wg@gradient0.com>
"""

import logging

import dq0sdk
from dq0sdk.data.preprocessing import preprocessing

import pandas as pd

import sklearn
import sklearn.preprocessing

from tensorflow import keras

logger = logging.getLogger()


class NeuralNetwork_adult(dq0sdk.models.tf.neural_network.NeuralNetwork):
    def __init__(self, model_path):
        super().__init__(model_path)
        self.learning_rate = 0.3
        self.input_dim = None

    def setup_data(self):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        train_data, data = source.read()

        # preprocess data
        X_df, y_ts, num_tr_instances = source.preprocess(
            approach_for_missing_feature='imputation',
            # 'imputation', 'dropping',
            imputation_method_for_cat_feats='unknown',
            # 'unknown', 'most_common_cat'
            imputation_method_for_quant_feats='median',  # 'median', 'mean'
            features_to_drop_list=None
        )
        # Scale values to the range from 0 to 1
        # to be precessed by the neural network
        X_df[source.quantitative_features_list] =\
            sklearn.preprocessing.minmax_scale(
                X_df[source.quantitative_features_list])

        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)  # test to label
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            preprocessing.train_test_split(X_df, y_bin, num_tr_instances)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
