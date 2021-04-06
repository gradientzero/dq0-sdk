# -*- coding: utf-8 -*-
"""
Pipeline transformers

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from abc import ABC

import numpy as np

import pandas as pd

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer

logger = logging.getLogger(__name__)


class Transformer(ABC):

    def __init__(self, input_col=None, **kwargs):
        self.transformer = None
        self.input_col = input_col

    def fit(self, X, y=None):
        # If input_col is given only those will be processed, by wrapping it into a ColumnTransformer.
        # The remaining columns are passeed through
        if self.input_col is not None:
            self.transformer = ColumnTransformer([('', self.transformer, self.input_col)], remainder='drop').fit(X)
        else:
            self.transformer = self.transformer.fit(X)
        return self

    def fit_transform(self, X, y=None):
        # keep pandas column names after transformation
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None

        # drop columns
        if self.input_col is not None:
            X_t = ColumnTransformer([('', self.transformer, self.input_col)], remainder='drop').fit_transform(X)
            X[self.input_col] = X_t
        else:
            X_t = self.transformer.fit_transform(X)
            if self.col_names is not None:
                X = pd.DataFrame(X_t, columns=self.col_names)
            else:
                X = X_t
        return X

    def transform(self, X):
        # keep pandas column names after transformation
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None
        X_t = self.transformer.transform(X)
        if self.input_col is not None:
            X[self.input_col] = X_t
        elif self.col_names is not None:
            X = pd.DataFrame(X_t, columns=self.col_names)
        else:
            X = X_t
        return X


class StandardScaler(Transformer):

    def __init__(self, *, copy=True, with_mean=True, with_std=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)


class OrdinalEncoder(Transformer):

    def __init__(self, *, categories='auto', dtype=np.float64, handle_unknown='error', unknown_value=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.OrdinalEncoder(categories=categories, dtype=dtype, handle_unknown=handle_unknown,
                                                        unknown_value=unknown_value)


class Binarizer(Transformer):

    def __init__(self, *, threshold=0.0, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.Binarizer(threshold=threshold, copy=copy)


class FunctionTransformer(Transformer):

    def __init__(self, func=None, inverse_func=None, *, validate=False, accept_sparse=False, check_inverse=True, kw_args=None,
                 inv_kw_args=None, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.FunctionTransformer(func=func, inverse_func=inverse_func, validate=validate, accept_sparse=accept_sparse,
                                                             check_inverse=check_inverse, kw_args=kw_args, inv_kw_args=inv_kw_args)


class KBinsDiscretizer(Transformer):

    def __init__(self, n_bins=5, *, encode='onehot', strategy='quantile', dtype=None, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy, dtype=dtype)


class KernelCenterer(Transformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.KernelCenterer()


class LabelBinarizer(Transformer):

    def __init__(self, *, neg_label=0, pos_label=1, sparse_output=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.LabelBinarizer(neg_label=neg_label, pos_label=pos_label, sparse_output=sparse_output)


class LabelEncoder(Transformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.LabelEncoder()


class MultiLabelBinarizer(Transformer):

    def __init__(self, *, classes=None, sparse_output=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MultiLabelBinarizer(classes=classes, sparse_output=sparse_output)


class MaxAbsScaler(Transformer):

    def __init__(self, *, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MaxAbsScaler(copy=copy)


class MinMaxScaler(Transformer):

    def __init__(self, feature_range=(0, 1), *, copy=True, clip=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MinMaxScaler(feature_range=feature_range, copy=copy, clip=clip)


class Normalizer(Transformer):

    def __init__(self, norm='l2', *, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.Normalizer(norm=norm, copy=copy)


class OneHotEncoder(Transformer):

    def __init__(self, *, categories='auto', drop=None, sparse=True, dtype=np.float64, handle_unknown='error', **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.OneHotEncoder(categories=categories, drop=drop, sparse=sparse, dtype=dtype)


class PolynomialFeatures(Transformer):

    def __init__(self, degree=2, *, interaction_only=False, include_bias=True, order='C', **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=include_bias, order=order)


class PowerTransformer(Transformer):

    def __init__(self, method='yeo-johnson', *, standardize=True, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.PowerTransformer(method=method, standardize=standardize, copy=copy)


class QuantileTransformer(Transformer):

    def __init__(self, *, n_quantiles=1000, output_distribution='uniform', ignore_implicit_zeros=False, subsample=100000, random_state=None, copy=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.QuantileTransformer(n_quantiles=n_quantiles, output_distribution=output_distribution,
                                                             ignore_implicit_zeros=ignore_implicit_zeros, subsample=subsample, random_state=random_state,
                                                             copy=copy)


class RobustScaler(Transformer):

    def __init__(self, * , with_centering=True, with_scaling=True, quantile_range=(25.0, 75.0) , copy=True, unit_variance=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.RobustScaler(with_centering=with_centering, with_scaling=with_scaling, quantile_range=quantile_range,
                                                      copy=copy, unit_variance=unit_variance)
