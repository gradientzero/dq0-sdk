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

from dq0.sdk.data.base_preprocess import BasePreprocess
from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.tf import NeuralNetworkRegression

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import minmax_scale

logger = logging.getLogger(__name__)


class UserModel(NeuralNetworkRegression):
    """Derived from dq0.sdk.models.tf.NeuralNetworkRegression class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        from sklearn.model_selection import train_test_split

        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        data = self.data_source.read()
        y = data['charges'].values
        X = data.drop(labels=['charges'], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # preprocess the data
        self.instance_preproc = Preprocessor(data_source=self.data_source)
        X_train, _ = self.instance_preproc.run(X_train.copy(), train=True)
        X_test, _ = self.instance_preproc.run(X_test.copy())

        # set attributes
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def setup_model(self, **kwargs):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        input_dim = self.X_train.shape[1]
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(input_dim),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
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
        self.epochs = 40
        self.batch_size = 50
        self.metrics = ['mean_absolute_error', 'mean_absolute_percentage_error']
        self.loss = tf.keras.losses.MeanAbsoluteError()
        # As an alternative, define the loss function with a string


class Preprocessor(BasePreprocess):
    """ Derived from dq0.sdk.data.base_preprocess.BasePreprocess class

    User defined preprocessing class used
    to preprocess data in setup_data() during training run
    and later for predict.

    Note: all preprocessing required at predict must be included

    """
    def __init__(self, data_source=None):
        super().__init__()
        self.ct_params = None
        self.x_minmax_scaler_params = None
        self.y_minmax_scaler_params = None

    def run(self, x, y=None, train=False):
        """Preprocess the data

        Preprocess the data set and store transformer parameters.

        Returns:
            preprocessed data
        """

        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.preprocessing import OrdinalEncoder
        from sklearn.preprocessing import MinMaxScaler

        # apply different transformations to subsets of the columns
        columnTransformer = ColumnTransformer(
            transformers=[
                ('one_hot_encoder', OneHotEncoder(), ['region']),
                ('binary_encoder', OrdinalEncoder(), ['sex', 'smoker'])
            ],
            remainder='passthrough'
        )

        columnTransformer.fit(x)
        if train:
            self.ct_params = columnTransformer.get_params()
        columnTransformer.set_params(**self.ct_params)
        x = columnTransformer.transform(x)

        x_minmax_scaler = MinMaxScaler()
        x_minmax_scaler.fit(x)
        if train:
            self.x_minmax_scaler_params = x_minmax_scaler.get_params()
        x_minmax_scaler.set_params(**self.x_minmax_scaler_params)
        X_scale = x_minmax_scaler.transform(x)
        
        return X_scale, None
