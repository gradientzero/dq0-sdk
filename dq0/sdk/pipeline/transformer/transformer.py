# -*- coding: utf-8 -*-
"""
Pipeline transformers

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from abc import ABC, abstractmethod

import numpy as np

import pandas as pd

import scipy

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer

logger = logging.getLogger(__name__)


class Transformer(ABC):

    def __init__(self, input_col=None, **kwargs):
        self.transformer = None
        self.col_names = None
        self.input_col = input_col

    @abstractmethod
    def fit(self, X, y=None):
        pass

    @abstractmethod
    def transform(self, X):
        pass

    def fit_transform(self, X, y=None):
        """Call fit and then transform"""
        self.fit(X, y)
        return self.transform(X)


class Transformer_1_to_1(ABC):
    """Standart transformer with 1 to 1 column mappings"""

    def __init__(self, input_col=None, **kwargs):
        self.transformer = None
        self.col_names = None
        self.input_col = input_col

    def fit(self, X, y=None):
        # If input_col is given only those will be processed, by wrapping it into a ColumnTransformer.
        # The remaining columns are passeed through
        # keep pandas column names after transformation
        if self.input_col is not None:
            self.transformer = ColumnTransformer([('', self.transformer, self.input_col)], remainder='drop').fit(X)
        else:
            self.transformer = self.transformer.fit(X)
        return self

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def transform(self, X):
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None
        X_t = self.transformer.transform(X)
        # check and convert sparse encoding arrays
        if isinstance(X_t, scipy.sparse.csr.csr_matrix):
            X_t = X_t.toarray()
        # case ColumnTransformer
        if self.input_col is not None:
            X[self.input_col] = X_t
        elif self.col_names is not None:
            X = pd.DataFrame(X_t, columns=self.col_names)
        else:  # numpy array
            X = X_t
        return X

    def _update_X_pandas(X, X_t, input_col):
        """Takes the input pd.DataFrame and updates the input columns of the DataFrame with the
        new values after the transformation. If the mapping of the columns (X_t) are not 1:1 the
        original columns are dropped and new columns added with names generated.
        """
        pass


class Transformer_1_to_N(Transformer):
    """Transformer with 1 to N column mappings (e.g. One-Hot-Encoding).
    The mapping if performed column wise so the N new columns can be named an track accordingly.
    A many to many mapping is not possible with this type of transformer
    """

    @abstractmethod
    def _get_column_names(self, transformer, c_name):
        """Specific to each transformer mapping. Gets names of the resulting Xt columns."""
        pass

    @abstractmethod
    def _setup_transformer(self):
        """"Sets up transformers with the given params for columnwise transformation if the given data"""
        pass

    def fit_transform(self, X, y=None):
        """Call fit and then transform"""
        self.fit(X, y)
        X_t = self.transform(X)
        if self.input_col is not None:
            X = X.drop(self.input_col, axis=1)
            X = pd.concat([X, X_t], axis=1)  # append X_t
        else:
            X = X_t
        return X

    def fit(self, X, y=None):
        """ Sets up a separate transformer for every column in the DataFrame.
        Args:
            X: pandas DataFrame
            y: None, ignored here. Only for compatability with pipeline
        Retruns:
            self
        """
        # TODO add functionality for numpy array
        if type(X) != pd.DataFrame:
            raise TypeError(f"X should be of type dataframe, not {type(X)}")

        self.transformers_c = []
        self.column_names_ = []

        if self.input_col is not None:
            col_process = self.input_col
        else:
            col_process = X.columns

        for c in col_process:
            transformer = self._setup_transformer()
            self.transformers_c.append(transformer.fit(X.loc[:, [c]]))
            self.column_names_.append(self._get_column_names(transformer, c))

        return self

    def transform(self, X):
        """Transform X using the transformers per column

        Args:
            X: Dataframe that is to be one hot encoded

        Returns:
            Dataframe Xt

        """
        # TODO add functionality for numpy array
        if type(X) != pd.DataFrame:
            raise TypeError(f"X should be of type dataframe, not {type(X)}")

        all_df = []

        if self.input_col is not None:
            col_process = self.input_col
        else:
            col_process = X.columns

        for i, c in enumerate(col_process):
            transformer = self.transformers_c[i]

            transformed_col = transformer.transform(X.loc[:, [c]])
            if isinstance(transformed_col, scipy.sparse.csr.csr_matrix):
                transformed_col = transformed_col.toarray()
            df_col = pd.DataFrame(transformed_col, columns=self.column_names_[i])
            all_df.append(df_col)

        return pd.concat(all_df, axis=1)


class StandardScaler(Transformer_1_to_1):

    def __init__(self, *, copy=True, with_mean=True, with_std=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)


class OrdinalEncoder(Transformer_1_to_1):

    def __init__(self, *, categories='auto', dtype=np.float64, handle_unknown='error', unknown_value=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.OrdinalEncoder(categories=categories, dtype=dtype, handle_unknown=handle_unknown,
                                                        unknown_value=unknown_value)


class Binarizer(Transformer_1_to_1):

    def __init__(self, *, threshold=0.0, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.Binarizer(threshold=threshold, copy=copy)


class FunctionTransformer(Transformer_1_to_1):

    def __init__(self, func=None, inverse_func=None, *, validate=False, accept_sparse=False, check_inverse=True, kw_args=None,
                 inv_kw_args=None, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.FunctionTransformer(func=func, inverse_func=inverse_func, validate=validate, accept_sparse=accept_sparse,
                                                             check_inverse=check_inverse, kw_args=kw_args, inv_kw_args=inv_kw_args)


class KBinsDiscretizer(Transformer_1_to_N):

    def __init__(self, n_bins=5, *, encode='onehot', strategy='quantile', dtype=None, **kwargs):
        super().__init__(**kwargs)
        self.n_bins = n_bins
        self.encode = encode
        self.strategy = strategy
        self.dtype = dtype
        self.transformer = self._setup_transformer()

    def _setup_transformer(self):
        return preprocessing.KBinsDiscretizer(n_bins=self.n_bins, encode=self.encode, strategy=self.strategy, dtype=self.dtype)

    def _get_column_names(self, transformer, c_name):
        """Specific to this transformer mapping. Gets names of the resulting Xt columns."""
        col_names = []
        for i in range(transformer.n_bins_[0]):
            col_names.append(f"{c_name}_bin_{i}")

        return col_names


class KernelCenterer(Transformer_1_to_1):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.KernelCenterer()


class LabelBinarizer(Transformer_1_to_1):

    def __init__(self, *, neg_label=0, pos_label=1, sparse_output=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.LabelBinarizer(neg_label=neg_label, pos_label=pos_label, sparse_output=sparse_output)


class LabelEncoder(Transformer_1_to_1):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.LabelEncoder()


class MultiLabelBinarizer(Transformer_1_to_1):

    def __init__(self, *, classes=None, sparse_output=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MultiLabelBinarizer(classes=classes, sparse_output=sparse_output)


class MaxAbsScaler(Transformer_1_to_1):

    def __init__(self, *, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MaxAbsScaler(copy=copy)


class MinMaxScaler(Transformer_1_to_1):

    def __init__(self, feature_range=(0, 1), *, copy=True, clip=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.MinMaxScaler(feature_range=feature_range, copy=copy, clip=clip)


class Normalizer(Transformer_1_to_1):

    def __init__(self, norm='l2', *, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.Normalizer(norm=norm, copy=copy)


class OneHotEncoder(Transformer_1_to_N):

    def __init__(self, *, categories='auto', drop=None, sparse=True, dtype=np.float64, handle_unknown='error', **kwargs):
        super().__init__(**kwargs)
        self.categories = categories
        self.drop = drop
        self.sparse = sparse
        self.dtype = dtype
        self.handle_unknown = handle_unknown
        self.transformer = self._setup_transformer()

    def _setup_transformer(self):
        return preprocessing.OneHotEncoder(categories=self.categories, drop=self.drop, sparse=self.sparse, dtype=self.dtype)

    def _get_column_names(self, transformer, c_name):
        """Specific to this transformer mapping. Gets names of the resulting Xt columns."""
        col_names = []
        for i in transformer.get_feature_names():
            col_names.append(f"{c_name}_{i.replace('x0_', '')}")

        return col_names


class PolynomialFeatures(Transformer_1_to_N):
    """Take note is 1 to N mapping does not allows for interaction of the features."""
    # TODO: add k to N transformer and change here
    def __init__(self, degree=2, *, interaction_only=False, include_bias=True, order='C', **kwargs):
        super().__init__(**kwargs)
        self.degree = degree
        self.interaction_only = interaction_only
        self.include_bias = include_bias
        self.order = order
        self.transformer = self._setup_transformer()

    def _setup_transformer(self):
        return preprocessing.PolynomialFeatures(degree=self.degree, interaction_only=self.interaction_only, include_bias=self.include_bias, order=self.order)

    def _get_column_names(self, transformer, c_name):
        """Specific to this transformer mapping. Gets names of the resulting Xt columns."""
        col_names = []
        for i in range(transformer.n_output_features_):
            col_names.append(f"{c_name}_poly_{i}")

        return col_names


class PowerTransformer(Transformer_1_to_1):

    def __init__(self, method='yeo-johnson', *, standardize=True, copy=True, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.PowerTransformer(method=method, standardize=standardize, copy=copy)


class QuantileTransformer(Transformer_1_to_1):

    def __init__(self, *, n_quantiles=1000, output_distribution='uniform', ignore_implicit_zeros=False, subsample=100000, random_state=None, copy=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.QuantileTransformer(n_quantiles=n_quantiles, output_distribution=output_distribution,
                                                             ignore_implicit_zeros=ignore_implicit_zeros, subsample=subsample, random_state=random_state,
                                                             copy=copy)


class RobustScaler(Transformer_1_to_1):

    def __init__(self, * , with_centering=True, with_scaling=True, quantile_range=(25.0, 75.0) , copy=True, unit_variance=False, **kwargs):
        super().__init__(**kwargs)
        self.transformer = preprocessing.RobustScaler(with_centering=with_centering, with_scaling=with_scaling, quantile_range=quantile_range,
                                                      copy=copy, unit_variance=unit_variance)
