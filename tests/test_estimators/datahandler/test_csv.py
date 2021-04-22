# -*- coding: utf-8 -*-
"""CSV data handler unit tests.

Copyright 2021, Gradient Zero
All rights reserved
"""

import os
import pathlib

from dq0.sdk.data.text.csv import CSV
from dq0.sdk.estimators.data_handler.csv import CSVDataHandler

import logging # noqa

FILEPATH = pathlib.Path(__file__).parent.absolute()
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_CM_CONFIG_CLASSIFICATION = os.path.join(DIR_PATH + '/mc_classification.yaml')


def test_CSVDataHandler_setup_data_001():
    feature_cols = ['a', 'b']
    target_cols = ['c']
    data_source = CSV(path=os.path.join(FILEPATH, 'test.csv'), feature_cols=feature_cols, target_cols=target_cols)
    data_handler = CSVDataHandler()
    X_train, X_test, y_train, y_test = data_handler.setup_data(data_source=data_source)
    print(X_train)
    assert X_train.iloc[0]['a'] == 1


def test_CSVDataHandler_setup_data_002():
    feature_cols = ['a', 'b']
    target_cols = ['c']
    # test with pipeline
    config_path = os.path.join(DIR_PATH, '..', '..', 'test_pipeline', 'pipeline_config.yaml')
    data_source = CSV(path=os.path.join(FILEPATH, 'test.csv'), feature_cols=feature_cols, target_cols=target_cols)
    print(DIR_PATH + '/../dq0/sdk/pipeline/transformer/transformer.py')
    data_handler = CSVDataHandler(pipeline_config_path=config_path, transformers_root_dir=DIR_PATH + '/../../../dq0/sdk/pipeline/transformer/transformer.py')
    X_train, X_test, y_train, y_test = data_handler.setup_data(data_source=data_source)
    print(X_train)
    # assert X_train.loc[0, 'a'] == 1


def test_CSVDataHandler_census():
    feature_cols = ['lastname', 'firstname', 'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship',
                    'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country']
    target_cols = ['income']
    # test with pipeline
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, '..', '..', '..', 'dq0', 'examples', 'census', '_data', 'pipeline_config.yaml')
    data_path = os.path.join(dir_path, '..', '..', '..', 'dq0', 'examples', 'census', '_data', 'adult_with_rand_names_w_header.csv')
    data_source = CSV(path=data_path, feature_cols=feature_cols, target_cols=target_cols)
    data_handler = CSVDataHandler(pipeline_config_path=config_path, transformers_root_dir='./dq0/sdk/pipeline/transformer/transformer.py')
    X_train, X_test, y_train, y_test = data_handler.setup_data(data_source=data_source)
    print(X_train)
    print(y_train)
    print(data_handler.data)
    # assert X_train.loc[0, 'a'] == 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_CSVDataHandler_setup_data_001()
    test_CSVDataHandler_setup_data_002()
    test_CSVDataHandler_census()
