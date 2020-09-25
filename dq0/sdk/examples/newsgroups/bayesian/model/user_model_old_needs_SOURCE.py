# -*- coding: utf-8 -*-
"""Multinomial Naive Bayesian Model example for the 20Newsgroups dataset.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.models.bayes.naive_bayesian_model import NaiveBayesianModel

import numpy as np

import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder


logger = logging.getLogger()


class UserModel(NaiveBayesianModel):
    """Multinomial Naive Bayesian classifier for the "20 Newsgroups" dataset

    SDK users instantiate this class to create and train the model.
    """

    def __init__(self):
        super().__init__()
        self.label_encoder = None

    def setup_model(self):
        """Setup model.

        Define the model here.
        """
        self._classifier_type = 'MultinomialNB'  # just for better-quality
        # printings

        self.model = MultinomialNB()
        # set smoothing prior
        self.model.set_params(alpha=.01)

        self.metrics = ['accuracy']

        print('Set up a ' + self._classifier_type + ' classifier.')

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        X, y = self.data_source.read()

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

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            print('\nAttached test dataset to user model. Feature matrix '
                  'shape:', self.X_test.shape)
            print('Class-labels vector shape:', self.y_test.shape)
