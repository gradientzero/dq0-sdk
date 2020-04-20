# -*- coding: utf-8 -*-
"""Multinomial Naive Bayesian Model class

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle

from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder


logger = logging.getLogger()


class UserModel(Model):
    """Multinomial Naive Bayesian classifier for the "20 Newsgroups" dataset

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

        self._classifier_type = 'MultinomialNB'

        if not self.DP_enabled:
            self.model = MultinomialNB()
        else:
            self._classifier_type = 'DP-' + self._classifier_type
            self.DP_epsilon = 0.01
            raise RuntimeError('DP-version of MultinomialNB not yet '
                               'available!')

        # set smoothing prior:
        self.model.set_params(alpha=.01)

        print('Setting up a ' + self._classifier_type + ' classifier...')

    def setup_data(self):

        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        X, y = source.read()

        # check data format
        if isinstance(X, pd.DataFrame):
            X = X.values
        else:
            if not isinstance(X, np.ndarray):
                raise Exception('X is not np.ndarray')

        if isinstance(y, pd.Series):
            y = y.values
        else:
            if not isinstance(y, np.ndarray):
                raise Exception('y is not np.ndarray')

        # prepare data
        if y.ndim == 2:
            # make non-dimensional array (just to avoid Warnings by Sklearn)
            y = np.ravel(y)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        # if self.label_encoder is None:
        #   print('Retraining')
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y)

        # back to column vector. Transform one-dimensional array into column
        # vector via newaxis
        y = y[:, np.newaxis]

        # set attributes
        self.X_train = X
        self.y_train = y
        self.X_test = None
        self.y_test = None

        if self.DP_enabled:
            self._compute_features_bounds()

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            print('\nAttached test dataset to user model. Feature matrix '
                  'shape:', self.X_test.shape)
            print('Class-labels vector shape:', self.y_test.shape)

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
