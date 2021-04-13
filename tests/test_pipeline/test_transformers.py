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
    X = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9],
                  [10, 11, 12]])
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def get_data_pandas():
    X, y = get_data_int()
    X = pd.DataFrame(X, columns=['a', 'b', 'c'])
    return X, y


def test_StandardScaler_001():
    print("\ntest_StandardScaler_001")
    X, y = get_data_int()
    trans = transformer.StandardScaler()
    X = trans.fit_transform(X)
    print(X)
    assert np.round(X[0, 0], 5) == -1.34164


def test_StandardScaler_pandas_001():
    print("\ntest_StandardScaler_pandas_001")
    X, y = get_data_pandas()
    trans = transformer.StandardScaler()
    X = trans.fit_transform(X)
    print(X)
    assert np.round(X.iloc[0]['a'], 5) == -1.34164


def test_StandardScaler_pandas_002():
    print("\ntest_StandardScaler_pandas_002")
    X, y = get_data_pandas()
    trans = transformer.StandardScaler(input_col=['a', 'b'])
    print(X)
    assert X.iloc[0]['c'] == 3
    X = trans.fit_transform(X)
    print(X)
    assert np.round(X.iloc[0]['a'], 5) == -1.34164
    assert X.iloc[0]['c'] == 3


def test_StandardScaler_pandas_003():
    print("\ntest_StandardScaler_pandas_003")
    X, y = get_data_pandas()
    trans = transformer.StandardScaler(input_col=['a', 'b'])
    trans.fit(X)
    print(X)
    assert X.iloc[0]['c'] == 3
    X = trans.transform(X)
    print(X)
    assert np.round(X.iloc[0]['a'], 5) == -1.34164
    assert X.iloc[0]['c'] == 3


def test_OrdinalEncoder():
    print("\ntest_OrdinalEncoder")
    X, y = get_data_int()
    trans = transformer.OrdinalEncoder()
    X = trans.fit_transform(X)
    print(X)
    assert X[0, 0] == 0


def test_Binarizer():
    print("\ntest_Binarizer")
    X, y = get_data_int()
    trans = transformer.Binarizer()
    X = trans.fit_transform(X)
    print(X)
    assert X[0, 0] == 1


# TODO: use a function
def test_FunctionTransformer():
    print("\ntest_FunctionTransformer")
    X, y = get_data_int()
    trans = transformer.FunctionTransformer()
    X = trans.fit_transform(X)
    print(X)
    assert X[0, 0] == 1


def test_KBinsDiscretizer_001():
    print("\ntest_KBinsDiscretizer_001")
    X, y = get_data_pandas()
    trans = transformer.KBinsDiscretizer(n_bins=5)
    X = trans.fit_transform(X)
    print(X)

    assert X.iloc[0]['a_bin_0'] == 1.0


def test_KBinsDiscretizer_002():
    print("\ntest_KBinsDiscretizer_002")
    X, y = get_data_int()
    trans = transformer.KBinsDiscretizer(n_bins=5)
    X = trans.fit_transform(X)
    print(X)

    assert X[0, 0] == 1


def test_KernelCenterer():
    print("\ntest_KernelCenterer")
    X, y = get_data_pandas()
    X = X[:3]
    trans = transformer.KernelCenterer()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['c'] == 0.0


def test_LabelBinarizer():
    print("\ntest_LabelBinarizer")
    X, y = get_data_pandas()
    trans = transformer.LabelBinarizer(input_col=['a'])
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a_label_1'] == 1


def test_LabelEncoder():
    print("\ntest_LabelEncoder")
    X, y = get_data_pandas()
    trans = transformer.LabelEncoder(input_col=['a'])
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a'] == 0


def test_MultiLabelBinarizer():
    print("\ntest_MultiLabelBinarizer")
    X, y = get_data_pandas()
    trans = transformer.MultiLabelBinarizer(input_col=['a', 'b'])
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a_label_a'] == 1


def test_MaxAbsScaler():
    print("\ntest_MaxAbsScaler")
    X, y = get_data_pandas()
    trans = transformer.MaxAbsScaler()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[3]['a'] == 1


def test_MinMaxScaler():
    print("\ntest_MinMaxScaler")
    X, y = get_data_pandas()
    trans = transformer.MinMaxScaler()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[3]['a'] == 1


def test_Normalizer():
    print("\ntest_Normalizer")
    X, y = get_data_pandas()
    trans = transformer.Normalizer()
    X = trans.fit_transform(X)
    print(X)
    assert np.round(X.iloc[0]['a'], 5) == 0.26726


def test_OneHotEncoder_001():
    print("\ntest_OneHotEncoder")
    X, y = get_data_pandas()
    trans = transformer.OneHotEncoder()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a_1'] == 1


def test_OneHotEncoder_002():
    print("\ntest_OneHotEncoder")
    X, y = get_data_pandas()
    trans = transformer.OneHotEncoder(input_col=['a', 'b'])
    X = trans.fit_transform(X)
    print(X)
    # column c should not be transformed
    assert X.iloc[0]['c'] == 3


def test_PolynomialFeatures():
    print("\ntest_PolynomialFeatures")
    X, y = get_data_pandas()
    trans = transformer.PolynomialFeatures()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[3]['a_poly_2'] == 100


def test_PowerTransformer():
    print("\ntest_PowerTransformer")
    X, y = get_data_pandas()
    trans = transformer.PowerTransformer()
    X = trans.fit_transform(X)
    print(X)
    assert np.round(X.iloc[0]['a'], 5) == -1.42438


def test_QuantileTransformer():
    print("\ntest_QuantileTransformer")
    X, y = get_data_pandas()
    trans = transformer.QuantileTransformer()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a'] == 0


def test_RobustScaler():
    print("\ntest_RobustScaler")
    X, y = get_data_pandas()
    trans = transformer.RobustScaler()
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a'] == -1


def test_ColumnSelector_001():
    print("\ntest_ColumnSelector_001")
    X, y = get_data_pandas()  # test with pd.DataFrame
    trans = transformer.ColumnSelector(selected_columns=['a'])
    X = trans.fit_transform(X)
    print(X)
    assert X.iloc[0]['a'] == 1.


def test_ColumnSelector_002():
    print("\ntest_ColumnSelector_002")
    X, y = get_data_int()  # test with numpy.array
    trans = transformer.ColumnSelector(selected_columns=[0])
    X = trans.fit_transform(X)
    print(X)
    assert X[0, 0] == 1.


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_StandardScaler_001()
    test_StandardScaler_pandas_001()
    test_StandardScaler_pandas_002()
    test_StandardScaler_pandas_003()
    test_OrdinalEncoder()
    test_Binarizer()
    test_FunctionTransformer()
    test_KBinsDiscretizer_001()
    test_KBinsDiscretizer_002()
    test_KernelCenterer()
    test_LabelBinarizer()
    test_LabelEncoder()
    test_MultiLabelBinarizer()
    test_MaxAbsScaler()
    test_MinMaxScaler()
    test_Normalizer()
    test_OneHotEncoder_001()
    test_OneHotEncoder_002()
    test_PolynomialFeatures()
    test_PowerTransformer()
    test_QuantileTransformer()
    test_RobustScaler()
    test_ColumnSelector_001()
    test_ColumnSelector_002()
