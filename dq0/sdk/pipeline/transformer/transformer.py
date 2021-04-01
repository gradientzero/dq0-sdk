# -*- coding: utf-8 -*-
"""
Pipeline transformers

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from abc import abstractmethod, ABC
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Transformer(ABC):

    def __init__(self, input_col=None, **kwargs):
        self.transformer = None
        self.input_col = input_col

    def fit(self, X, y=None):
        # If input_col is given only those will be processed, by wrapping it into a ColumnTransformer.
        # The remaining columns are passeed through
        if self.input_col is not None:
            self.transformer = ColumnTransformer([('', self.transformer, self.input_col)], remainder='passthrough').fit(X)
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
            X_t = ColumnTransformer([('', self.transformer, self.input_col)], remainder='passthrough').fit_transform(X)
        else:
            X_t = self.transformer.fit_transform(X)

        if self.col_names is not None:
            X_t = pd.DataFrame(X_t, columns=self.col_names)
        return X_t

    def transform(self, X):
        # keep pandas column names after transformation
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None
        X_t = self.transformer.transform(X)
        if self.col_names is not None:
            X_t = pd.DataFrame(X_t, columns=self.col_names)
        return X_t


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
