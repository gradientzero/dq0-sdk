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

        X = dataset_df.iloc[:,:-1]
        y = dataset_df.iloc[:,-1]

        # do the train test split
        X_train, X_test, y_train, y_test =\
            train_test_split(X,
                             y,
                             test_size=0.33
                             )

        # preprocess the data
        self.ud_preprocessor_name = CalledWhatever()
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
    def __init__(self):
        super().__init__()
        self.per_feature_imputation_value_ts = None
        self.categories = 'auto'
        self.ohe_params = None
        self.scaler_params = None
        self.le_params = None
        
        # columns
        self.column_names_list = [
            'lastname',
            'firstname',
            'age',
            'workclass',
            'fnlwgt',
            'education',
            'education-num',
            'marital-status',
            'occupation',
            'relationship',
            'race',
            'sex',
            'capital-gain',
            'capital-loss',
            'hours-per-week',
            'native-country',
            'income'
        ]

        self.columns_types_list = [
            {
                'name': 'age',
                'type': 'int'
            },
            {
                'name': 'workclass',
                'type': 'string',
                'values': [
                    'Private',
                    'Self-emp-not-inc',
                    'Self-emp-inc',
                    'Federal-gov',
                    'Local-gov',
                    'State-gov',
                    'Without-pay',
                    'Never-worked',
                    'Unknown'
                ]
            },
            {
                'name': 'fnlwgt',
                'type': 'int'
            },
            {
                'name': 'education',
                'type': 'string',
                'values': [
                    'Bachelors',
                    'Some-college',
                    '11th',
                    'HS-grad',
                    'Prof-school',
                    'Assoc-acdm',
                    'Assoc-voc',
                    '9th',
                    '7th-8th',
                    '12th',
                    'Masters',
                    '1st-4th',
                    '10th',
                    'Doctorate',
                    '5th-6th',
                    'Preschool'
                ]
            },
            {
                'name': 'education-num',
                'type': 'int'
            },
            {
                'name': 'marital-status',
                'type': 'string',
                'values': [
                    'Married-civ-spouse',
                    'Divorced',
                    'Never-married',
                    'Separated',
                    'Widowed',
                    'Married-spouse-absent',
                    'Married-AF-spouse'
                ]
            },
            {
                'name': 'occupation',
                'type': 'string',
                'values': [
                    'Tech-support',
                    'Craft-repair',
                    'Other-service',
                    'Sales',
                    'Exec-managerial',
                    'Prof-specialty',
                    'Handlers-cleaners',
                    'Machine-op-inspct',
                    'Adm-clerical',
                    'Farming-fishing',
                    'Transport-moving',
                    'Priv-house-serv',
                    'Protective-serv',
                    'Armed-Forces',
                    'Unknown'
                ]
            },
            {
                'name': 'relationship',
                'type': 'string',
                'values': [
                    'Wife',
                    'Own-child',
                    'Husband',
                    'Not-in-family',
                    'Other-relative',
                    'Unmarried'
                ]
            },
            {
                'name': 'race',
                'type': 'string',
                'values': [
                    'White',
                    'Asian-Pac-Islander',
                    'Amer-Indian-Eskimo',
                    'Other',
                    'Black'
                ]
            },
            {
                'name': 'sex',
                'type': 'string',
                'values': [
                    'Female',
                    'Male'
                ]
            },
            {
                'name': 'capital-gain',
                'type': 'int'
            },
            {
                'name': 'capital-loss',
                'type': 'int'
            },
            {
                'name': 'hours-per-week',
                'type': 'int'
            },
            {
                'name': 'native-country',
                'type': 'string',
                'values': [
                    'United-States',
                    'Cambodia',
                    'England',
                    'Puerto-Rico',
                    'Canada',
                    'Germany',
                    'Outlying-US(Guam-USVI-etc)',
                    'India',
                    'Japan',
                    'Greece',
                    'South',
                    'China',
                    'Cuba',
                    'Iran',
                    'Honduras',
                    'Philippines',
                    'Italy',
                    'Poland',
                    'Jamaica',
                    'Vietnam',
                    'Mexico',
                    'Portugal',
                    'Ireland',
                    'France',
                    'Dominican-Republic',
                    'Laos',
                    'Ecuador',
                    'Taiwan',
                    'Haiti',
                    'Columbia',
                    'Hungary',
                    'Guatemala',
                    'Nicaragua',
                    'Scotland',
                    'Thailand',
                    'Yugoslavia',
                    'El-Salvador',
                    'Trinadad&Tobago',
                    'Peru',
                    'Hong',
                    'Holand-Netherlands',
                    'Unknown'
                ]
            }
        ]

        self.na_values_d = {
            'capital-gain': 99999,
            'capital-loss': 99999,
            'hours-per-week': 99,
            'workclass': '?',
            'native-country': '?',
            'occupation': '?'}
        
        # define target feature
        self.target_feature = 'income'

    def run(self, x, y=None, train=False):
        """Preprocess the data

        Preprocess the data set and store transformer parameters.

        Returns:
            preprocessed data
        """
        import sklearn.preprocessing
        import pandas as pd
        import numpy as np

        column_names_list = self.column_names_list
        columns_types_list = self.columns_types_list

        x.columns = column_names_list[:-1]

        # Do the same NaN value substitution as in read_csv
        x.replace(to_replace=self.na_values_d, value=np.nan, inplace=True)

        # drop unused columns
        x.drop(['lastname', 'firstname'], axis=1, inplace=True)
        # column_names_list.remove('lastname')
        # column_names_list.remove('firstname')

        # get categorical features
        categorical_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'string']

        # get quantitative features
        quantitative_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'int' or col['type'] == 'float']

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
            le = sklearn.preprocessing.LabelEncoder()
            le.fit(y)
            if train:
                self.le_params = le.get_params()
                print(le.classes_)
                print(self.le_params)
            if self.le_params is not None:
                le.set_params(**self.le_params)
            else:
                raise ValueError('self.le_params cannot be None')
        
            y = le.transform(y)

        return x, y
