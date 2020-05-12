# -*- coding: utf-8 -*-
"""Gaussian Naive Bayesian Model example for the adult census data set.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle

from dq0sdk.data.utils import util
from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder


logger = logging.getLogger()


class UserModel(Model):
    """Naive Bayesian classifier for the "Adult Census Income" dataset

    SDK users instantiate this class to create and train the model.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'IBM_Diffpriv'
        self.label_encoder = None

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        self._classifier_type = 'GaussianNB'  # just for better-quality
        # printings

        self.model = GaussianNB()
        print('Setting up a ' + self._classifier_type + ' classifier...')

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        from sklearn.model_selection import train_test_split

        # read and preprocess
        data = self.preprocess()

        # split
        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.20,
                             shuffle=True)
        self.input_dim = X_train_df.shape[1]

        # check data format
        if isinstance(X_train_df, pd.DataFrame):
            X_train_df = X_train_df.values
        if isinstance(X_test_df, pd.DataFrame):
            X_test_df = X_test_df.values
        if isinstance(y_train_ts, pd.DataFrame):
            y_train_ts = y_train_ts.values
        if isinstance(y_test_ts, pd.DataFrame):
            y_test_ts = y_test_ts.values

        # prepare data
        # make non-dimensional array (just to avoid Warnings by Sklearn)
        if y_train_ts.ndim == 2:
            y_train_ts = np.ravel(y_train_ts)
        if y_test_ts.ndim == 2:
            y_test_ts = np.ravel(y_test_ts)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        self.label_encoder = LabelEncoder()
        y_train_ts = self.label_encoder.fit_transform(y_train_ts)
        y_test_ts = self.label_encoder.fit_transform(y_test_ts)

        # back to column vector. Transform one-dimensional array into column
        # vector via newaxis
        y_train_ts = y_train_ts[:, np.newaxis]
        y_test_ts = y_test_ts[:, np.newaxis]

        # set attributes
        self.X_train = X_train_df
        self.y_train = y_train_ts
        self.X_test = X_test_df
        self.y_test = y_test_ts

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        from dq0sdk.data.preprocessing import preprocessing
        import sklearn.preprocessing
        import pandas as pd

        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        # columns
        column_names_list = [
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
            col for col in dataset.columns
            if col != target_feature and dataset[col].dtype == 'object']

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        quantitative_features_list =\
            list(set(column_names_list) - set(categorical_features_list) - {
                target_feature})

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

        # Investigate whether ordinal features are present
        # (Weak) assumption: for each categorical feature, its values in the
        # test set is already present in the training set.
        dataset = pd.get_dummies(dataset, columns=categorical_features_list)
        # dummy_na=True => add a column to indicate NaNs. False => NaNs are
        # ignored.
        # Rather than get_dummies, it would be better as follows ...
        # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # enc.fit(X_df[categorical_features_list])

        # Scale values to the range from 0 to 1 to be precessed by the
        # neural network
        dataset[quantitative_features_list] = sklearn.preprocessing.\
            minmax_scale(dataset[quantitative_features_list])

        # label target
        y_ts = dataset[target_feature]
        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)
        dataset.drop([target_feature], axis=1, inplace=True)
        dataset[target_feature] = y_bin

        return dataset

    def fit(self):
        """Model fit function learning a model from training data
        """
        # Check for valid model setup
        if not hasattr(self, 'X_train'):
            raise ValueError('Missing argument in model: X_train')
        if not hasattr(self, 'y_train'):
            raise ValueError('Missing argument in model: y_train')

        if isinstance(self.y_train, np.ndarray):
            if self.y_train.ndim == 2:
                # make 1-dimensional array
                self.y_train = np.ravel(self.y_train)

        print('\n\n-------------------- ' + self._classifier_type + ' '
              'classifier learning ---------------------')
        print('\nPercentage freq. of target labels in train dataset:')
        util.estimate_freq_of_labels(self.y_train)

        self.model.fit(self.X_train, self.y_train)
        print('\nLearned a ' + self._classifier_type + ' model from',
              self.X_train.shape[0], 'examples')

    def evaluate(self, test_data=True, verbose=0):
        """Model predict and evaluate.

        Test learnt classifier over a test set
        This method is final. Signature will be checked at runtime!

        Args:
            test_data (bool): False to use train data instead of test
                Default is True.
            verbose (int): Verbose level, Default is 0

        Returns:
            accuracy score over test set
        """
        X = self.X_test if test_data else self.X_train
        y = self.y_test if test_data else self.y_train

        data_type = 'test' if test_data else 'train'

        print('\n\n----------------- Testing learnt classifier on ' + data_type
              + ' data -----------------')

        if isinstance(y, np.ndarray):
            if y.ndim == 2:
                # make 1-dimensional arrays
                y = np.ravel(y)

        y_pred_np_a = self.model.predict(X)

        print(
            '\nPercentage freq. of target labels in ' + data_type + ' dataset '
            '(baseline for classification performance):')
        util.estimate_freq_of_labels(y)

        accuracy_score = metrics.accuracy_score(y, y_pred_np_a)
        print('\nModel accuracy on ' + data_type + ' data:', round(
            accuracy_score, 2))
        print('\n', metrics.classification_report(y, y_pred_np_a))

        return accuracy_score

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (str): The name of the model
            version (int): The version of the model
        """

        file_path = '{}/{}/{}.pickle'.format(self.model_path, version, name)
        # create target directory and all intermediate directories if not
        # existing
        file_path_dirs = os.path.dirname(file_path)
        if not os.path.exists(file_path_dirs):
            os.makedirs(file_path_dirs)

        with open(file_path, 'wb') as f:
            pickle.dump(self._classifier, f)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (str): The name of the model
            version (int): The version of the model
        """

        file_path = '{}/{}/{}.pickle'.format(self.model_path, version, name)

        with open(file_path, 'rb') as file:
            self._classifier = pickle.load(file)
