
# -*- coding: utf-8 -*-
"""Gaussian Naive Bayesian Model example for the adult census data set.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle

import diffprivlib.models as dp

from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

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

        self.DP_enabled = False
        self.DP_epsilon = None

    def setup_model(self):

        self._classifier_type = 'GaussianNB'

        if not self.DP_enabled:
            self.model = GaussianNB()
        else:
            self._classifier_type = 'DP-' + self._classifier_type
            self.DP_epsilon = 0.01

            self.model = dp.GaussianNB(
                epsilon=self.DP_epsilon,
                bounds=self.features_bounds
            )
        print('Setting up a ' + self._classifier_type + ' classifier...')

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        from sklearn.model_selection import train_test_split

        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        # read and preprocess
        data = source.preprocess()

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
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

        # LabelEncoder() encodes target labels with value between 0 and n_classes - 1
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

        if self.DP_enabled:
            self._compute_features_bounds()

    def _compute_features_bounds(self):

        if isinstance(self.X_train, pd.DataFrame):
            min_values = self.X_train.min(axis=0).values
            max_values = self.X_train.max(axis=0).values
        elif isinstance(self.X_train, np.ndarray):
            min_values = self.X_train.min(axis=0)
            max_values = self.X_train.max(axis=0)

        self.features_bounds = list(zip(min_values, max_values))

    def fit(self, **kwargs):
        """

        Train model on a dataset passed as input.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

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
