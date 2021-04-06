# -*- coding: utf-8 -*-
"""
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.pipeline import pipeline # noqa
from dq0.sdk.pipeline.transformer import transformer # noqa
import numpy as np # noqa
import pandas as pd # noqa
import os # noqa

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.array([[2, 20, 3], [4, 50, 6, ], [7, 80, 9], [10, 110, 12]])
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def get_data_pandas():
    X, y = get_data_int()
    X = pd.DataFrame(X, columns=['a', 'b', 'c'])
    return X, y


def test_pipeline_001():
    print("\ntest_pipeline_001")
    X, y = get_data_int()
    trans = transformer.StandardScaler()
    steps = [('StandardScaler', trans)]
    pipe = pipeline.Pipeline(steps=steps)

    X_t = pipe.fit_transform(X)
    print(X_t)
    assert np.round(X_t[0, 0], 5) == -1.23718
    assert np.round(X_t[0, 1], 5) == -1.34164
    assert np.round(X_t[0, 2], 5) == -1.34164


def test_pipeline_002():
    print("\ntest_pipeline_002")
    # with numpy
    X, y = get_data_int()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config.yaml'),
                             transformers_root_dir='./dq0/sdk/pipeline/transformer/transformer.py')

    X_t = pipe.fit_transform(X)
    print(X_t)
    assert np.round(X_t[0, 0], 5) == 0.65983
    assert np.round(X_t[0, 1], 5) == 0.59628
    assert np.round(X_t[0, 2], 5) == 0.89443


def test_pipeline_003():
    print("\ntest_pipeline_003")
    # with pandas
    X, y = get_data_pandas()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config.yaml'),
                             transformers_root_dir='./dq0/sdk/pipeline/transformer/transformer.py')

    X_t = pipe.fit_transform(X)
    print(X_t)
    assert np.round(X_t.iloc[0]['a'], 5) == 0.65983
    assert np.round(X_t.iloc[0]['b'], 5) == 0.59628
    assert np.round(X_t.iloc[0]['c'], 5) == 0.89443


def test_pipeline_004():
    print("\ntest_pipeline_004")
    # with pandas
    X, y = get_data_pandas()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config_2.yaml'),
                             transformers_root_dir='./dq0/sdk/pipeline/transformer/transformer.py')

    X_t = pipe.fit_transform(X)
    print(X_t)
    assert np.round(X_t.iloc[0]['a'], 5) == -1.23718
    assert np.round(X_t.iloc[0]['b'], 5) == 0.59628
    assert np.round(X_t.iloc[0]['c'], 5) == 0.89443


def test_pipeline_005():
    print("\ntest_pipeline_005")
    # with pandas
    X, y = get_data_pandas()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config_3.yaml'),
                             transformers_root_dir='./dq0/sdk/pipeline/transformer/transformer.py')

    X_t = pipe.fit_transform(X)
    print(X_t)
    assert X_t.iloc[0]['a'] == 2.0
    assert X_t.iloc[0]['b'] == 20.0
    assert np.round(X_t.iloc[0]['c'], 5) == -1.34164


# use only during development
# def test_pipeline_provoke_error():
#     # provoke error
#     pipeline.Pipeline(config_path='', steps=[])
#     print("This should not be printed")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_pipeline_001()
    test_pipeline_002()
    test_pipeline_003()
    test_pipeline_004()
    test_pipeline_005()
    # test_pipeline_provoke_error()
