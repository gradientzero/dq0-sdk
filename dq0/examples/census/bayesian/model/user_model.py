# -*- coding: utf-8 -*-
"""Gaussian Naive Bayesian Model example for the adult census data set.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import sys

from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.bayes.naive_bayesian_model import NaiveBayesianModel

import numpy as np

import pandas as pd

from sklearn.naive_bayes import GaussianNB

from tensorflow.keras import metrics

logger = logging.getLogger()


class UserModel(NaiveBayesianModel):
    """Naive Bayesian classifier for the "Adult Census Income" dataset

    SDK users instantiate this class to create and train the model.
    """

    def __init__(self):
        super().__init__()
        self.label_encoder = None

    def setup_model(self, **kwargs):
        """Setup model function

        Define the model here.
        """
        self._classifier_type = 'GaussianNB'  # just for better-quality
        # printings

        self.model = GaussianNB()

        self.metrics = ['accuracy', metrics.Precision()]

        print('Set up a ' + self._classifier_type + ' classifier.')

    def setup_data(self, **kwargs):
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
            # TODO discuss how we save the features list is user model. We
            #  cannot use the list of columns in the data yaml file, 'cause
            #  the user can remove columns during the preprocessing step.
            #  More in general, we should not allow the user to create new
            #  features (e.g., by multiply columns)!
            self.features_list = X_train_df.columns.to_list()

            X_train_df = X_train_df.values
        if isinstance(X_test_df, pd.DataFrame):
            X_test_df = X_test_df.values
        if isinstance(y_train_ts, pd.Series):
            y_train_ts = y_train_ts.values
        if isinstance(y_test_ts, pd.Series):
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
        y_train_ts = y_train_ts.reshape(-1, 1)  # y_train_ts[:, np.newaxis]
        y_test_ts = y_test_ts.reshape(-1, 1)  # y_test_ts[:, np.newaxis]

        # set attributes
        self.X_train = X_train_df
        self.y_train = y_train_ts
        self.X_test = X_test_df
        self.y_test = y_test_ts

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached
        source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        from dq0.sdk.data.preprocessing import preprocessing
        from dq0.sdk.data.utils import util
        import sklearn.preprocessing
        import pandas as pd

        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

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

        # define target feature
        target_feature = 'income'

        categorical_features_list, quantitative_features_list = \
            util.get_categorical_and_quantitative_features_list(
                dataset, target_feature)

        # Continuous variable "fnlwgt" is the "final weight",
        # the number of units in the target population that the responding unit
        # represents.
        #
        # Variable "education_num" contains the total number of years of
        # education. It is basically a continuous representation of the
        # categorical variable "education".
        #
        # The variable "relationship" represents the person role in his own
        # family.
        #
        # "capital_gain" and "capital_loss" are incomes from investment
        # sources other than wage/salary.
        features_to_drop_list = ['lastname', 'firstname', 'fnlwgt']

        # Gaussian Naive Bayes is designed for continuous data.
        # In detail, it assumes IID features, with each feature following a
        # Gaussian Distribution (although it can perform decently
        # even if this assumption is violated).
        #
        # We ignore the assumption of Gaussian distribution here (just
        # verify it with the Shapiro-Wilkes test) and drop categorical
        # variables.

        features_to_drop_list.extend(
            x for x in categorical_features_list if x not in features_to_drop_list)

        if features_to_drop_list is not None:
            dataset.drop(features_to_drop_list, axis=1, inplace=True)

        # update lists
        categorical_features_list, quantitative_features_list = \
            util.get_categorical_and_quantitative_features_list(
                dataset, target_feature
            )

        # handle missing data
        approach_for_missing_feature = 'imputation'
        imputation_method_for_cat_feats = 'unknown'
        imputation_method_for_quant_feats = 'median'
        dataset = preprocessing.handle_missing_data(
            dataset,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=categorical_features_list,
            quantitative_features_list=quantitative_features_list
        )

        # label target
        y_ts = dataset[target_feature]
        self.label_encoder = sklearn.preprocessing.LabelEncoder()
        y_enc = self.label_encoder.fit_transform(y_ts)
        y_enc = pd.Series(index=y_ts.index, data=y_enc)
        dataset.drop([target_feature], axis=1, inplace=True)
        dataset[target_feature] = y_enc

        util.print_dataset_info(dataset, 'Census dataset')

        return dataset
