# -*- coding: utf-8 -*-
"""Data Source for adult test dataset.

https://archive.ics.uci.edu/ml/datasets/adult

Predict whether income exceeds $50K/yr based on census data.

The test set is contained in the subfolder "data"

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.data.csv import CSVSource
from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.utils import util

import pandas as pd


class CensusSource(CSVSource):
    """Data Source for the Adult dataset.

    Provides function to read and preprocess the adult dataset.

    Attributes:
        categorical_features_list (list): List of category features
        quantitative_features_list (list): List of quantitative features
        target_feature (:obj:`str`): The target feature (column name)
        filepath_train (:obj:`str`): Absolute path to the adult train dataset file.
        filepath_test (:obj:`str`): Absolute path to the adult test dataset file.
        skiprows (int, optional): Number of rows to skip.

    Args:
        paths (:obj:`str`): One or more paths (';' separated) for train and test
    """
    def __init__(self, paths):
        super().__init__(paths)
        self.train_data = None  # test data in self.data
        path_parts = paths.split(';')
        self.filepath_train = path_parts[0] if len(path_parts) > 0 else ''
        self.filepath_test = path_parts[1] if len(path_parts) > 1 else ''
        self.skiprows = 1
        self.categorical_features_list = None
        self.quantitative_features_list = None
        self.target_feature = None

    def read(self, force=False):
        """Read Adult dataset.

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            train and test data as pandas dataframe.

        Raises:
            IOError: if directory was not found
        """
        if not force and self.data is not None:
            return self.train_data, self.data

        path = self.filepath_train
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not find the adult train data.'
                          'File not found {}'.format(path))
        path = self.filepath_test
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not find the adult test data.'
                          'File not found {}'.format(path))

        column_names_list = [
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

        target_feature = 'income'

        dataset_df = pd.read_csv(self.filepath_train,
                                 names=column_names_list,
                                 sep=',',
                                 skiprows=self.skiprows,
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

        dataset_df_test = pd.read_csv(self.filepath_test,
                                      names=column_names_list,
                                      sep=',',
                                      skiprows=self.skiprows,
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

        categorical_features_list = [
            col for col in dataset_df.columns
            if col != target_feature and dataset_df[col].dtype == 'object']

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        quantitative_features_list =\
            list(set(column_names_list) - set(categorical_features_list) - set(
                [target_feature]))

        self.data = dataset_df_test
        self.train_data = dataset_df
        self.categorical_features_list = categorical_features_list
        self.quantitative_features_list = quantitative_features_list
        self.target_feature = target_feature

        return self.train_data, self.data

    def preprocess(self,
                   force=False,
                   approach_for_missing_feature='imputation',
                   imputation_method_for_cat_feats='unknown',
                   imputation_method_for_quant_feats='median',
                   features_to_drop_list=None):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            force (bool): True to force re-read of the data.
            approach_for_missing_feature (:obj:`str`): imputation or dropping
            imputation_method_for_cat_feats (:obj:`str`): unknown or most_common_cat
            imputation_method_for_quant_feats (:obj:`str`): median or mean
            features_to_drop_list (list): list of features (columns) to drop

        Returns:
            preprocessed data
        """
        if not force and self.preprocessed_data is not None:
            return self.preprocessed_data

        tr_dataset_df = preprocessing.handle_missing_data(
            self.train_data,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=self.categorical_features_list,
            quantitative_features_list=self.quantitative_features_list)

        test_dataset_df = preprocessing.handle_missing_data(
            self.data,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=self.categorical_features_list,
            quantitative_features_list=self.quantitative_features_list)

        num_tr_instances, _ = self.train_data.shape
        num_test_instances, _ = self.data.shape

        X_train_df = tr_dataset_df.drop(self.target_feature, axis=1)
        X_test_df = test_dataset_df.drop(self.target_feature, axis=1)

        # full dataset
        X_df = X_train_df.append(X_test_df)
        y_ts = tr_dataset_df[self.target_feature].append(
            test_dataset_df[self.target_feature])

        # cleanup (test) labels: strip trailing '.' (by visual inspection on
        # sampled data, it should appear only in the test labels. For safety,
        # parse training labels, too.)
        y_ts = y_ts.apply(lambda label: label.rstrip("."))

        # util.print_dataset_info(X_df, 'Raw full dataset
        # without target_feature')

        if features_to_drop_list is not None:
            X_df.drop(features_to_drop_list, axis=1, inplace=True)
            util.pretty_print_strings_list(
                features_to_drop_list,
                '\nThe following uninformative features (given the remaining '
                'ones)  have been dropped:')

        print('\nConvert categorical features to numerical representations by '
              'one-hot encoding')
        # TODO: investigate whether ordinal features are present
        #
        # (Weak) assumption: for each categorical feature, its values in the
        # test set is already present in the training set.
        #
        X_df = pd.get_dummies(X_df, columns=self.categorical_features_list,
                              dummy_na=False)  # True => add a column to
        # indicate NaNs. False => NaNs are ignored.
        #
        # Rather than get_dummies, it would be better as follows ...
        # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # enc.fit(X_df[categorical_features_list])

        # print(X_df.head(10))  # debug

        return X_df, y_ts, num_tr_instances
