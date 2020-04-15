# -*- coding: utf-8 -*-
"""Data Source for census adult data set.

https://archive.ics.uci.edu/ml/datasets/adult

Predict whether income exceeds $50K/yr based on census data.

The census data set was augmented with random first- and lastnames for
the purpose of privacy demonstration.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.data.csv import CSVSource

import pandas as pd


class UserSource(CSVSource):
    """Data Source for the Adult dataset.

    Provides function to read and preprocess the modified adult dataset.

    Attributes:
        categorical_features_list (list): List of category features
        quantitative_features_list (list): List of quantitative features
        target_feature (:obj:`str`): The target feature (column name)
        skiprows (int, optional): Number of rows to skip.

    Args:
        filepath (:obj:`str`): Path to the data set csv
    """
    def __init__(self, filepath):
        super().__init__(filepath)
        self.skiprows = 1
        self.categorical_features_list = None
        self.quantitative_features_list = None
        self.target_feature = None

    def read(self):
        """Read Adult dataset.

        Returns:
            data as pandas dataframe.

        Raises:
            IOError: if filepath was not found
        """
        path = self.filepath
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not find the adult data.'
                          'File not found {}'.format(path))

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

        target_feature = 'income'

        dataset_df = pd.read_csv(path,
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

        dataset_df.drop(['lastname', 'firstname'], axis=1, inplace=True)
        column_names_list.remove('lastname')
        column_names_list.remove('firstname')

        categorical_features_list = [
            col for col in dataset_df.columns
            if col != target_feature and dataset_df[col].dtype == 'object']

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        quantitative_features_list =\
            list(set(column_names_list) - set(categorical_features_list) - set(
                [target_feature]))

        self.data = dataset_df
        self.categorical_features_list = categorical_features_list
        self.quantitative_features_list = quantitative_features_list
        self.target_feature = target_feature

        return dataset_df

    def preprocess(self,
                   approach_for_missing_feature='imputation',
                   imputation_method_for_cat_feats='unknown',
                   imputation_method_for_quant_feats='median',
                   features_to_drop_list=None):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            approach_for_missing_feature (:obj:`str`): imputation or dropping
            imputation_method_for_cat_feats (:obj:`str`): unknown or most_common_cat
            imputation_method_for_quant_feats (:obj:`str`): median or mean
            features_to_drop_list (list): list of features (columns) to drop

        Returns:
            preprocessed data
        """
        from dq0sdk.data.preprocessing import preprocessing
        import sklearn.preprocessing

        # read data first
        dataset_df = self.read()

        # now preprocess
        dataset_df = preprocessing.handle_missing_data(
            dataset_df,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=self.categorical_features_list,
            quantitative_features_list=self.quantitative_features_list)

        if features_to_drop_list is not None:
            dataset_df.drop(features_to_drop_list, axis=1, inplace=True)

        # Investigate whether ordinal features are present
        # (Weak) assumption: for each categorical feature, its values in the
        # test set is already present in the training set.
        dataset_df = pd.get_dummies(dataset_df, columns=self.categorical_features_list,
                                    dummy_na=False)
        # True => add a column to indicate NaNs. False => NaNs are ignored.
        # Rather than get_dummies, it would be better as follows ...
        # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # enc.fit(X_df[categorical_features_list])

        # Scale values to the range from 0 to 1 to be precessed by the neural network
        dataset_df[self.quantitative_features_list] =\
            sklearn.preprocessing.minmax_scale(
                dataset_df[self.quantitative_features_list])

        # label target
        y_ts = dataset_df[self.target_feature]
        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)
        dataset_df.drop([self.target_feature], axis=1, inplace=True)
        dataset_df[self.target_feature] = y_bin

        return dataset_df
