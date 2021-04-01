# -*- coding: utf-8 -*-
""" 
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.pipeline.transformer import transformer
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.array([[1, 2, 3], [4, 5, 6, ], [7, 8, 9], [10, 11, 12]])
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def get_data_pandas():
    X, y = get_data_int()
    X = pd.DataFrame(X, columns=['a', 'b', 'c'])
    return X, y


def test_StandardScaler():
    X, y = get_data_int()
    trans = transformer.StandardScaler()
    X = trans.fit_transform(X)


def test_StandardScaler_pandas_001():
    X, y = get_data_pandas()
    trans = transformer.StandardScaler()
    X = trans.fit_transform(X)


def test_StandardScaler_pandas_002():
    X, y = get_data_pandas()
    trans = transformer.StandardScaler(input_col=['a', 'b'])
    print(X)
    X = trans.fit_transform(X)
    print(X)


def test_StandardScaler_pandas_003():
    X, y = get_data_pandas()
    trans = transformer.StandardScaler(input_col=['a', 'b'])
    trans.fit(X)
    print(X)
    X = trans.transform(X)
    print(X)


def test_OrdinalEncoder():
    X, y = get_data_int()
    trans = transformer.OrdinalEncoder()
    X = trans.fit_transform(X)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_StandardScaler()
    test_StandardScaler_pandas_001()
    test_StandardScaler_pandas_002()
    test_StandardScaler_pandas_003()
    test_OrdinalEncoder()
