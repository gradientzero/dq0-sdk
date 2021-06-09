# -*- coding: utf-8 -*-
"""Adult dataset example.

Neural network model definition

Example:
    >>> ./dq0 project create --name demo # doctest: +SKIP
    >>> cd demo # doctest: +SKIP
    >>> copy user_model.py to demo/model/ # doctest: +SKIP
    >>> ../dq0 data list # doctest: +SKIP
    >>> ../dq0 model attach --id <dataset id> # doctest: +SKIP
    >>> ../dq0 project deploy # doctest: +SKIP
    >>> ../dq0 model train # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP
    >>> ../dq0 model predict --input-path </path/to/numpy.npy> # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

# from dq0.examples.census.raw.model.preprocess import CalledWhatever
from dq0.sdk.data.base_preprocess import BasePreprocess
from dq0.sdk.errors import fatal_error
from dq0.sdk.models.tf import NeuralNetworkClassification

logger = logging.getLogger('dq0.' + __name__)


class UserModel(NeuralNetworkClassification):
    """Derived from dq0.sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()
        self.calibrate_posterior_probabilities = False

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        from sklearn.model_selection import train_test_split

        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)
        
        # read the data via the attached input data source
        dataset_df = self.data_source.read(
            # sep=',',
            # header=None,
            # index_col=None,
            # skipinitialspace=True,
            # na_values=self.na_values_d,
        )
        
        X = dataset_df.loc[:,self.data_source.feature_cols]  # results in alphabetically ordered columns
        y = dataset_df.loc[:,self.data_source.target_cols].values
        
        # do the train test split
        X_train, X_test, y_train, y_test =\
            train_test_split(X,
                             y,
                             test_size=0.33
                             )

        # preprocess the data
        self.ud_preprocessor_name = CalledWhatever(data_source=self.data_source)
        X_train, y_train = self.ud_preprocessor_name.run(X_train.copy(), y_train, train=True)
        X_test, y_test = self.ud_preprocessor_name.run(X_test.copy(), y_test)

        # set data attributes
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        self.input_dim = self.X_train.shape[1]

        logger.debug("X_train.shape: {}".format(self.X_train.shape))
        logger.debug("X_test.shape: {}".format(self.X_test.shape))
        logger.debug("y_train.shape: {}".format(self.y_train.shape))
        logger.debug("y_test.shape: {}".format(self.y_test.shape))

    def setup_model(self, **kwargs):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(10, activation='tanh'),
            tf.keras.layers.Dense(10, activation='tanh'),
            tf.keras.layers.Dense(2, activation='softmax')])
        self.optimizer = 'Adam'
        # To set optimizer params, self.optimizer = optimizer instance
        # rather than string, with params values passed as input to the class
        # constructor. E.g.:
        #
        #   import tensorflow
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #       learning_rate=0.015)
        #
        self.epochs = 10
        self.batch_size = 250
        self.metrics = ['accuracy', 'mae']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        # As an alternative, define the loss function with a string


class CalledWhatever(BasePreprocess):
    """ Derived from dq0.sdk.data.base_preprocess.BasePreprocess class
    
    User defined preprocessing class used
    to preprocess data in setup_data() during training run
    and later for predict.

    Note: all preprocessing required at predict must be included

    """
    def __init__(self, data_source=None):
        super().__init__()
        self.data_source = data_source
        self.per_feature_imputation_value_ts = None
        self.categories = 'auto'
        self.ohe_params = None
        self.scaler_params = None
        self.le_params = None

        self.na_values_d = {
            'capital-gain': 99999,
            'capital-loss': 99999,
            'hours-per-week': 99,
            'workclass': '?',
            'native-country': '?',
            'occupation': '?'}

    def run(self, x, y=None, train=False):
        """Preprocess the data

        Preprocess the data set and store transformer parameters.

        Returns:
            preprocessed data
        """
        import sklearn.preprocessing
        import pandas as pd
        import numpy as np

        # Do the same NaN value substitution as in read_csv
        x.replace(to_replace=self.na_values_d, value=np.nan, inplace=True)

        # drop unused columns
        x.drop(['lastname', 'firstname'], axis=1, inplace=True)

        # get cat and numeric columns
        if self.data_source.col_types is not None:
            categorical_features_list = [
                k for k, v in self.data_source.col_types.items() 
                if (v in ['string', '']) and (k in x.columns)]
            quantitative_features_list = [
                k for k, v in self.data_source.col_types.items() 
                if (v in ['int', 'float']) and (k in x.columns)]

        # Impute cat nan values
        x[categorical_features_list] = x[
            categorical_features_list].fillna('Unknown')

        # impute numeric nan values
        if train:
            self.per_feature_imputation_value_ts = \
                x[quantitative_features_list].median(axis=0)

        x[quantitative_features_list] = x[
                quantitative_features_list].fillna(
                self.per_feature_imputation_value_ts, axis=0)

        # get dummy columns
        enc = sklearn.preprocessing.OneHotEncoder(categories=self.categories, sparse=False, handle_unknown='ignore')
        enc.fit(x[categorical_features_list])
        if train:
            self.categories = enc.categories_
            self.ohe_params = enc.get_params()
        enc.set_params(**self.ohe_params)
        x_dummies = enc.transform(x[categorical_features_list])
        col_names = enc.get_feature_names(categorical_features_list)
        x_dummies = pd.DataFrame(x_dummies, columns=col_names)
        x = pd.concat([x.reset_index(drop=True), x_dummies], axis=1)
        x.drop(categorical_features_list, axis=1, inplace=True)

        # Scale values to the range from 0 to 1 to be precessed by the neural network
        scaler = sklearn.preprocessing.MinMaxScaler()
        scaler.fit(x[quantitative_features_list])
        if train:
            self.scaler_params = scaler.get_params()
        if self.scaler_params is not None:
            scaler.set_params(**self.scaler_params)
        else:
            raise ValueError('self.scaler_params cannot be None')
        x[quantitative_features_list] = scaler.transform(x[quantitative_features_list])

        # label target
        if y is not None:
            if y.ndim > 1:
                _y = y.ravel()
            le = sklearn.preprocessing.LabelEncoder()
            le.fit(_y)
            if train:
                self.le_params = le.get_params()
            if self.le_params is not None:
                le.set_params(**self.le_params)
            else:
                raise ValueError('self.le_params cannot be None')

            y = le.transform(_y)

        return x, y
