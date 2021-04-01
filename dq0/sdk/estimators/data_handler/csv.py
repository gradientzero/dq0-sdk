# -*- coding: utf-8 -*-
"""Base data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split

from dq0.sdk.estimators.data_handler.base import BasicDataHandler
import dq0.sdk
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class CSVDataHandler(BasicDataHandler):
    """Basic CSV Data Handler for all estimators"""

    def __init__(self, pipeline_steps=None, pipeline_config_path=None):
        super().__init__(pipeline_steps=pipeline_steps, pipeline_config_path=pipeline_config_path)

    def setup_data(self, data_source, train_size=0.66, **kwargs):
        """ Setup data from CSV file. Using the CSV data source.
        """

        # Check if the data source is of expected type
        if not isinstance(data_source, dq0.sdk.data.text.csv.CSV):
            raise ValueError("data_source attached to estimator and handled by the CSV data handler is not of Type: dq0.sdk.data.text.csv.CSV but: {}".format(type(data_source)))
        if not hasattr(data_source, 'feature_cols') and not hasattr(data_source, 'target_cols'):
            raise ValueError("CSV data source has not attribute feature_cols or target_cols. Please set this values on init or in the metadata")

        data = super().setup_data(data_source=data_source, **kwargs)
        # Check type of data, must be pandas.DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data loaded is not of type pandas.DataFrame, but: {}".format(type(data)))

        # TODO: Remode
        # Convert all non-numerical columns to numerical ones
        # data = self._df_to_numerical(data)
        if self.pipeline is not None:
            data = self.pipeline.fit_transform(data)

        X = self._get_X(data, data_source.feature_cols)
        y = self._get_y(data, data_source.target_cols)
        X_train, X_test, y_train, y_test = self._train_test_split(X, y, train_size=train_size)
        return X_train, X_test, y_train, y_test

    def get_input_dim(self, X):
        if not len(X.shape) == 2:
            raise ValueError("Feature Vector X is not 2-dim. The CSVDataHandler can only handle 2-dim DFs")
        return X.shape[-1]

    def get_output_dim(self, y):
        return len(y.unique())

    def _get_X(self, data, feature_cols):
        """Get X features vectors assuming data is a Pandas DataFrame"""
        return data[feature_cols]

    def _get_y(self, data, target_cols):
        """Get y target vector assuming data is a Pandas DataFrame"""
        if len(target_cols) == 1:
            return data[target_cols[-1]]
        else:
            raise ValueError("CSVDataHandler currently only supports one target_col (Check Metadata!); len(target_cols): {}".format(len(target_cols)))

    def _df_to_numerical(self, data):
        logger.info("Converting all non-numerical columns to numerical (Integer-Encoding)")
        data_num = pd.DataFrame()
        for col_name, col_type in zip(data.columns, data.dtypes):
            if (col_type is not np.dtype(np.int)) and (col_type is not np.dtype(np.float)):
                enc = OrdinalEncoder()
                data_num[col_name] = enc.fit_transform(data[col_name].values.reshape(-1, 1)).flatten()

            else:
                data_num[col_name] = data[col_name]
        return data_num

    def _train_test_split(self, X, y, train_size=0.66):
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size)
        return X_train, X_test, y_train, y_test
