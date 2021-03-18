# -*- coding: utf-8 -*-
"""
Convolutional Neural Network model implementation for "20 Newsgroups"

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.mod_utils.error import fatal_error
from dq0.sdk.data.preprocessing import preprocessing
from dq0.sdk.data.utils import util
from dq0.sdk.models.tf import NeuralNetworkClassification

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import tensorflow.compat.v1 as tf

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """
    Neural Network model implementation for "20 Newsgroups"

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """

    def __init__(self):
        super().__init__()
        self._classifier_type = 'mlnn'
        self.label_encoder = None

    def setup_model(self, **kwargs):

        self.optimizer = 'Adam'
        # As an alternative:
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #   learning_rate=0.015)

        self.epochs = 50
        self.batch_size = 250
        self.metrics = ['accuracy']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        # As an alternative, define the loss function with a string

        # TODO: kernel_regularizer breaks DP training in TF2.40 priv0.5.1
        self.regularization_param = 1e-3
        self.regularizer_dict = {
            # 'kernel_regularizer': tf.keras.regularizers.l2(
            #     self.regularization_param)  # ,
            # # 'activity_regularizer': tf.keras.regularizers.l2(
            # #    self.regularization_param),
            # # 'bias_regularizer': tf.keras.regularizers.l2(
            # #    self.regularization_param)
        }
        print('Setting up a multilayer neural network...')
        self.model = self._get_mlnn_model()

    def _get_mlnn_model(self, which_model='ml-leaks_paper'):

        n_in = self._num_features
        n_out = self._num_classes

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):
            # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py
            num_units_hidden_layer = 128
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(num_units_hidden_layer,
                                      activation='tanh',
                                      **self.regularizer_dict
                                      ),
                tf.keras.layers.Dense(n_out, activation='softmax')
            ]
            )
        else:
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(n_out, activation='softmax')]
            )

        model.summary()
        return model

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
        #
        # WARNING!!! when setting num_top_ranked_feats_to_keep to 20k,
        # DP fitting takes more than an hour
        #
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
            train_test_split(X, y,
                             test_size=0.33
                             )

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

        # set attributes
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
