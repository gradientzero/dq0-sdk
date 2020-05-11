# -*- coding: utf-8 -*-
"""Neural network Model class for patient dataset:

https://synthea.mitre.org/downloads

Copyright 2020, Gradient Zero
"""

import logging

from dq0sdk.models.tf.neural_network_regression import NeuralNetworkRegression

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import minmax_scale


logger = logging.getLogger()


class UserModel(NeuralNetworkRegression):
    """Derived from dq0sdk.models.tf.NeuralNetworkRegression class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path, **kwargs):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        from sklearn.model_selection import train_test_split

        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        data = self.data_source.read()
        X, y = self._prepare_data(data)

        self.input_dim = X.shape[1]
        self.batch_size = X.shape[0]
        self.num_microbatches = self.batch_size

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def _prepare_data(self, data):
        """Helper function to prepare the input data."""
        le = LabelEncoder()
        data['GENDER_NUM'] = le.fit_transform(data['GENDER'])
        data['BIRTHPLACE_NUM'] = le.fit_transform(data['BIRTHPLACE'])
        data['CITY_NUM'] = le.fit_transform(data['CITY'])
        data['STATE_NUM'] = le.fit_transform(data['STATE'])
        data['COUNTY_NUM'] = le.fit_transform(data['COUNTY'])

        data['BIRTHDATE'] = [pd.Timestamp(ts) for ts in data['BIRTHDATE']]
        data['BIRTHDATE_UNIX'] = data['BIRTHDATE'].astype(int) / 10**9

        target_col = 'BIRTHDATE_UNIX'
        col_selecion = ['GENDER_NUM', 'BIRTHPLACE_NUM', 'CITY_NUM', 'STATE_NUM', 'COUNTY_NUM',
                        'ZIP', 'LAT', 'LON', 'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE']

        X_df = data[col_selecion].fillna(0.)
        y_df = data[target_col]

        X = X_df.values
        y = y_df.values

        X_scale = minmax_scale(X)
        y_scale = minmax_scale(y)

        return X_scale, y_scale

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        self.optimizer = 'Adam'
        self.learning_rate = 0.001

        self.epochs = 10
        self.loss = tf.keras.losses.MeanSquaredError()

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(1000, activation='tanh'),
            tf.keras.layers.Dense(1000, activation='tanh'),
            tf.keras.layers.Dense(1, activation='linear')]
        )
