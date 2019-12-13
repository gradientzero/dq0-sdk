# -*- coding: utf-8 -*-
"""
Adult dataset example.

Neural network model definition

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.models.tf import NeuralNetwork

import pandas as pd

import sklearn
import sklearn.preprocessing

from tensorflow import keras


class NeuralNetwork_adult(NeuralNetwork):
    """Neural Network model implementation.

    This is an example of how to subclass the dq0sdk Neural Network model.
    """
    def __init__(self, model_path='.'):
        super().__init__()
        self.learning_rate = 0.3
        self.input_dim = None
        self.model_path = model_path

    def setup_data(self,
                   X_df,
                   y_ts,
                   quantitative_features_list,
                   num_tr_instances):
        """Setup data function

        This implementation overrides the parent's setup_data function to
        prepare the data for this specific model.

        Args:
            X_df (df): loaded dataset to preprocess.
            y_ts (df): loaded testset to preprocess.
            quantitative_features_list (list): list of quantitative feature
                columns.
            num_tr_instances (int): number of training samples.
        """
        # Scale values to the range from 0 to 1
        X_df[quantitative_features_list] =\
            sklearn.preprocessing.minmax_scale(X_df[
                quantitative_features_list])

        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)  # test to label
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            preprocessing.train_test_split(X_df, y_bin, num_tr_instances)
        self.input_dim = X_train_df.shape[1]

        return X_train_df, X_test_df, y_train_ts, y_test_ts

    def setup_model(self):
        """Setup model function

        Custom Keras model definition.
        """
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
