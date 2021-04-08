# -*- coding: utf-8 -*-
"""Multinomial Naive Bayesian Model example for the 20Newsgroups dataset.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.mod_utils.error import fatal_error
from dq0.sdk.data.preprocessing import preprocessing
from dq0.sdk.data.utils import util
from dq0.sdk.models.bayes.naive_bayesian_model import NaiveBayesianModel

import numpy as np

from sklearn.model_selection import train_test_split
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

    def setup_model(self, **kwargs):
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
        # Set the number of features for feature extraction
        num_top_ranked_feats_to_keep = int(
            5e3)  # set to 'all' to skip feat sel.
        if str(num_top_ranked_feats_to_keep).lower() != 'all':
            technique_for_feat_sel = 'chi-squared test'  # 'mutual information'

        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        dataset_df = self.data_source.read()

        X = dataset_df.iloc[:, 0]
        y = dataset_df.iloc[:, 1]

        # fillna with empty strings (exist in original)
        X.fillna("", inplace=True)

        # Split for preprocessing
        # If the input is sparse, the output will be a scipy.sparse.csr_matrix.
        # Otherwise, output type is the same as the input type.
        X_train_df, X_test_df, y_train_se, y_test_se =\
            train_test_split(X, y, test_size=0.33)

        X_train_sp_matr, X_test_sp_matr, feature_names_list = \
            preprocessing.extract_count_features_from_text_corpus(
                X_train_df.values.tolist(),
                X_test_df.values.tolist()
            )

        if str(num_top_ranked_feats_to_keep).lower() != 'all':
            X_train_sp_matr, X_test_sp_matr, feature_names_list = \
                preprocessing.univariate_feature_selection(
                    num_top_ranked_feats_to_keep,
                    X_train_sp_matr,
                    y_train_se,
                    X_test_sp_matr,
                    technique=technique_for_feat_sel,
                    feature_names_list=feature_names_list
                )

        """Data structure helper function."""
        sparse_representation = False
        X_train_df = util.sparse_scipy_matrix_to_Pandas_df(
            X_train_sp_matr,
            sparse_representation,
            columns_names_list=feature_names_list)

        X_test_df = util.sparse_scipy_matrix_to_Pandas_df(
            X_test_sp_matr,
            sparse_representation,
            columns_names_list=feature_names_list)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        # if self.label_encoder is None:
        #   print('Retraining')
        label_encoder = LabelEncoder()
        le_model = label_encoder.fit(y_train_se)
        # transform() returns one-dimensional numpy.ndarray even if input type
        # is Pandas.Series
        y_train_np_a = le_model.transform(y_train_se)
        y_test_np_a = le_model.transform(y_test_se)

        # back to column vector. Transform one-dimensional array into column
        # vector via newaxis
        y_train_np_a = y_train_np_a[:, np.newaxis]
        y_test_np_a = y_test_np_a[:, np.newaxis]

        # set attributes: get numpy.ndarray objects if not yet
        self.X_train = X_train_df.values
        self.y_train = y_train_np_a
        self.X_test = X_test_df.values
        self.y_test = y_test_np_a
        self._num_features = self.X_train.shape[1]
        # WARNING: np.nan, np.Inf in y are counted as classes by np.unique
        self._num_classes = len(np.unique(self.y_train))

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            print('\nAttached test dataset to user model. Feature matrix '
                  'shape:', self.X_test.shape)
            print('Class-labels vector shape:', self.y_test.shape)
