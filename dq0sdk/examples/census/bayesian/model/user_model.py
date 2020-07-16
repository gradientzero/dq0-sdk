# -*- coding: utf-8 -*-
"""Gaussian Naive Bayesian Model example for the adult census data set.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.bayes.naive_bayesian_model import NaiveBayesianModel

import numpy as np

import pandas as pd

from sklearn.naive_bayes import GaussianNB

from tensorflow.keras import metrics

logger = logging.getLogger()


class UserModel(NaiveBayesianModel):
    """Naive Bayesian classifier for the "Adult Census Income" dataset

    SDK users instantiate this class to create and train the model.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.label_encoder = None

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        self._classifier_type = 'GaussianNB'  # just for better-quality
        # printings

        self.model = GaussianNB()

        self.metrics = ['accuracy', metrics.Precision()]

        print('Set up a ' + self._classifier_type + ' classifier.')

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
        # self.label_encoder = LabelEncoder()
        # y_train_ts = self.label_encoder.fit_transform(y_train_ts)
        # y_test_ts = self.label_encoder.transform(y_test_ts)

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
        self.label_encoder = sklearn.preprocessing.LabelEncoder()
        y_enc = self.label_encoder.fit_transform(y_ts)
        y_enc = pd.Series(index=y_ts.index, data=y_enc)
        dataset.drop([target_feature], axis=1, inplace=True)
        dataset[target_feature] = y_enc

        return dataset
