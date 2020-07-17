# -*- coding: utf-8 -*-
"""Neural network Model for the medical insurance dataset

https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/insurance.csv

1338 examples of beneficiaries in the insurance plan.
Task: predict total medical expenses charged to the plan based on six
attributes of the beneficiary:
    age
    sex: gender, female / male
    bmi: body mass index (kg / m ^ 2), ratio of person’s weight in kilograms
         and height in meters squared. Ideally from 18.5 to 24.9
    children: number of children covered by health insurance
    smoker: yes / no
    region: beneficiary's residential area in the US: northeast, southeast,
    southwest, northwest.

Copyright 2020, Gradient Zero
"""

import logging

from dq0.sdk.models.tf import NeuralNetworkRegression

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import minmax_scale

logger = logging.getLogger()


class UserModel(NeuralNetworkRegression):
    """Derived from dq0.sdk.models.tf.NeuralNetworkRegression class

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

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def _prepare_data(self, data_df):
        """Helper function to prepare the input data."""

        y = data_df['charges'].values
        X_df = data_df.drop(labels=['charges'], axis=1)

        # apply different transformations to subsets of the columns
        columnTransformer = ColumnTransformer(
            transformers=[
                ('one_hot_encoder', OneHotEncoder(), ['region']),
                ('binary_encoder', OrdinalEncoder(), ['sex', 'smoker'])
            ],
            remainder='passthrough'
        )
        X = columnTransformer.fit_transform(X_df)

        X_scale = minmax_scale(X)
        y_scale = minmax_scale(y)

        return X_scale, y_scale

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        input_dim = self.X_train.shape[1]
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(input_dim),
            tf.keras.layers.Dense(3, activation='sigmoid'),
            tf.keras.layers.Dense(1, activation='linear')]
        )
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
        # To set optimizer params, self.optimizer = optimizer instance
        # rather than string, with params values passed as input to the class
        # constructor. E.g.:
        #
        #   import tensorflow
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #       learning_rate=0.015)
        #
        self.epochs = 20
        self.batch_size = 250
        self.metrics = ['mean_absolute_error']
        self.loss = tf.keras.losses.MeanAbsoluteError()
        # As an alternative, define the loss function with a string
