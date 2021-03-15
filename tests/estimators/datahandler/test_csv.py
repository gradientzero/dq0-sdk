# -*- coding: utf-8 -*-
"""CSV data handler unit tests.

Copyright 2021, Gradient Zero
All rights reserved
"""

from dq0.sdk.estimators.data_handler.csv import CSVDataHandler
from dq0.sdk.data.text.csv import CSV

import pathlib, os

FILEPATH = pathlib.Path(__file__).parent.absolute()


def test_CSVDataHandler_setup_data_001():
    feature_cols = ['a', 'b']
    target_cols = ['c']
    data_source = CSV(path=os.path.join(FILEPATH, 'test.csv'), feature_cols=feature_cols, target_cols=target_cols)
    data_handler = CSVDataHandler()
    X_train, X_test, y_train, y_test = data_handler.setup_data(data_source=data_source)
    assert X_train.loc[0, 'a'] == 1


if __name__ == "__main__":
    test_CSVDataHandler_setup_data_001()
