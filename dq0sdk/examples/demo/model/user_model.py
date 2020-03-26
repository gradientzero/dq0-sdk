#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult dataset example for cli.
Neural network model definition

Example:
    ./dq0 model create demo
    cd demo
    copy user_source.py to demo/data
    copy user_model.py to demo/model
    ../dq0 data list
    ../dq0 model attach --id <dataset id or uuid>
    ../dq0 model deploy
    ../dq0 model train
    ../dq0 model state
    ../dq0 model predict --input-path </path/to/numpy.npy>
    ../dq0 model state

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Craig Lincoln <cl@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.neural_network import NeuralNetwork

from sklearn.model_selection import train_test_split

from tensorflow import keras

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        data = source.read()

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        self.learning_rate = 0.3
        self.epochs = 5
        self.num_microbatches = 1
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
