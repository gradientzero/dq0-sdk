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

import tensorflow as tf
from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer

from dq0sdk.data.preprocessing import preprocessing
import dq0sdk


class NeuralNetwork_adult_yaml(dq0sdk.models.tf.neural_network.NeuralNetwork):
    def __init__(self, yaml_config):
        super().__init__()
        self.yaml_config = yaml_config
        self.yaml_dict = yaml_config.yaml_dict
        self.dp_optimizer_para = yaml_config.optimizer_para_from_yaml()
        self.model_path = self.yaml_dict['MODEL_PATH']
        self.metrics = self.yaml_dict['METRICS']
        self.epochs = self.yaml_dict['FIT']['epochs']

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
        self.model = self.yaml_config.model_from_yaml()

    def fit(self, **kwargs):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        X_train = kwargs['X_train']
        y_train = kwargs['y_train']

        optimizer = dp_optimizer.GradientDescentOptimizer(
            **self.dp_optimizer_para)
        loss = self.yaml_config.loss_from_yaml()
        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=self.metrics)
        self.model.fit(X_train,
                       y_train,
                       epochs=self.epochs,
                       verbose=self.verbose)

