# -*- coding: utf-8 -*-
"""Example for TUEV.

Neural network model definition for the Census dataset.

"""

import logging

from dq0.sdk.data.utils import util
from dq0.sdk.errors import fatal_error
from dq0.sdk.models.tf import NeuralNetworkClassification

import tensorflow as tf

logger = logging.getLogger('dq0.' + __name__)


class UserModel(NeuralNetworkClassification):
    """Derived from dq0.sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()

        # ensure reproducibility
        # util.initialize_rnd_numbers_generators_state(seed=1)

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected dataset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        from sklearn.model_selection import train_test_split

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

        # TODO complete and uncomment
        # try:
        #     metayaml = kwargs['metayaml']
        # except KeyError:
        #     logger.fatal('path to data YAML file not provided!')
        #     return 1
        # column_names_list, column_info = util.load_dataset_info_from_yaml(metayaml)

        # read and preprocess the data
        dataset_df = self.preprocess()

        # do the train test split
        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(dataset_df.iloc[:, :-1],
                             dataset_df.iloc[:, -1],
                             test_size=0.33
                             )
        self.input_dim = X_train_df.shape[1]

        # set data attributes
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

        logger.debug("X_train.shape: {}".format(self.X_train.shape))
        logger.debug("X_test.shape: {}".format(self.X_test.shape))
        logger.debug("y_train.shape: {}".format(self.y_train.shape))
        logger.debug("y_test.shape: {}".format(self.y_test.shape))

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected dataset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        [TUEV]
            must be reproducible (proof)
            for ordinary scaled features we used integer encoding,
            for nominal scaled data we used one-hot encoding
            a standard scaler to scale the real-valued features between 0
            and 1.

            No leakage was discovered. --> ??

            Data is assumed to be i.i.d. Therefore train/test split
            randomly exclusive. Train/validation split randomly exclusive.

        Returns:
            preprocessed data
        """
        from dq0.sdk.data.preprocessing import preprocessing
        import sklearn.preprocessing
        import pandas as pd

        column_names_list = self.column_names_list
        columns_types_list = self.columns_types_list

        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        # read the data via the attached input data source
        dataset = self.data_source.read(
            names=column_names_list,
            sep=',',
            skiprows=1,
            index_col=None,
            skipinitialspace=True,
            na_values={
                'capital-gain': 99999,
                'capital-loss': 99999,
                'hours-per-week': 99,
                'workclass': '?',
                'native-country': '?',
                'occupation': '?'}
        )

        # drop unused columns
        dataset.drop(['lastname', 'firstname'], axis=1, inplace=True)
        column_names_list.remove('lastname')
        column_names_list.remove('firstname')

        # define target feature
        target_feature = 'income'

        # get categorical features
        categorical_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'string']

        # get quantitative features
        quantitative_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'int' or col['type'] == 'float']

        # get arguments
        approach_for_missing_feature = 'imputation'
        imputation_method_for_cat_feats = 'unknown'
        imputation_method_for_quant_feats = 'median'
        features_to_drop_list = None

        # handle missing data
        dataset = preprocessing.handle_missing_data(
            dataset,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=categorical_features_list,
            quantitative_features_list=quantitative_features_list)

        if features_to_drop_list is not None:
            dataset.drop(features_to_drop_list, axis=1, inplace=True)

        # get dummy columns (one-hot encoding of categorical vars)
        dataset = pd.get_dummies(dataset, columns=categorical_features_list, dummy_na=False)

        # unzip categorical features with dummies
        categorical_features_list_with_dummies = []
        for col in columns_types_list:
            if col['type'] == 'string':
                for value in col['values']:
                    categorical_features_list_with_dummies.append('{}_{}'.format(col['name'], value))

        # add missing columns
        missing_columns = set(categorical_features_list_with_dummies) - set(dataset.columns)
        for col in missing_columns:
            dataset[col] = 0

        # and sort the columns
        dataset = dataset.reindex(sorted(dataset.columns), axis=1)

        # Scale values to the range from 0 to 1 to be precessed by the neural network
        dataset[quantitative_features_list] = sklearn.preprocessing.minmax_scale(dataset[quantitative_features_list])

        # label target
        y_ts = dataset[target_feature]
        self.label_encoder = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = self.label_encoder.fit_transform(y_ts)
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)
        dataset.drop([target_feature], axis=1, inplace=True)
        dataset[target_feature] = y_bin

        return dataset

    def setup_model(self, **kwargs):
        """Setup model function

        Define the model here.
        """

        which_model = 'M4'
        if which_model == 'M1':
            self._model_1()
        elif which_model == 'M2':
            self._model_2()
        elif which_model == 'M3':
            self._model_3()
        elif which_model == 'M4':
            self._model_4()

    def _model_1(self):
        """
        Model in the SDK example
        """

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(5, activation='relu'),
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
        self.metrics = ['accuracy']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        # As an alternative, define the loss function with a string

    def _model_2(self):
        """Setup model function

        Try to overfit by increasing network capacity
        """

        self._model_1()

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(100, activation='relu'),
            tf.keras.layers.Dense(75, activation='relu'),
            tf.keras.layers.Dense(50, activation='relu'),
            tf.keras.layers.Dense(25, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')])

    def _model_3(self):
        """Setup model function

        Sensibly increase learning rate from default value 1e-3 to 1e-1
        """
        self._model_1()

        # To set optimizer params, self.optimizer = optimizer instance
        # rather than string, with params values passed as input to the class
        # constructor. E.g.:
        #

        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)

    def _model_4(self):
        """Setup model function

        Try to overfit by sensibly increasing the number of epochs from 10
        to 100.

        """
        self._model_1()
        self.epochs = 100