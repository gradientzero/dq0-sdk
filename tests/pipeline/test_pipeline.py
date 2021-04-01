# -*- coding: utf-8 -*-
""" 
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.pipeline import pipeline
from dq0.sdk.pipeline.transformer import transformer
import numpy as np
import pandas as pd
import os

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.array([[1, 2, 3], [4, 5, 6, ], [7, 8, 9], [10, 11, 12]])
    y_int = np.array([1, 2, 3, 4])

    return X, y_int

def get_data_pandas():
    X, y = get_data_int()
    X = pd.DataFrame(X, columns=['a', 'b', 'c'])
    return X, y

def test_pipeline_001():
    X, y = get_data_int()
    trans = transformer.StandardScaler()
    steps = [('StandardScaler', trans)]
    pipe = pipeline.Pipeline(steps=steps)

    X_t = pipe.fit_transform(X)
    print(X_t)


def test_pipeline_002():
    # with numpy
    X, y = get_data_int()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config.yaml'))

    X_t = pipe.fit_transform(X)
    print(X_t)


def test_pipeline_003():
    # with pandas
    X, y = get_data_pandas()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config.yaml'))

    X_t = pipe.fit_transform(X)
    print(X_t)


def test_pipeline_004():
    # with pandas
    X, y = get_data_pandas()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pipe = pipeline.Pipeline(config_path=os.path.join(dir_path, 'pipeline_config_2.yaml'))

    X_t = pipe.fit_transform(X)
    print(X_t)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_pipeline_001()
    test_pipeline_002()
    test_pipeline_003()
    test_pipeline_004()
