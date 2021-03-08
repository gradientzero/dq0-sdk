# -*- coding: utf-8 -*-
"""Base data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split

from dq0.sdk.estimators.estimator import Estimator
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class BasicDataHandler(Estimator):
    """Basic Data Handler for all estimators"""

    def setup_data(self, train_size=0.66, **kwargs):

        data = super().setup_data(**kwargs)

        # TODO: make type safe, for now I assume data is of type pandas.DataFrame
        data = self._df_to_numerical(data)
        X = self._get_X(data, self.feature_cols)
        y = self._get_y(data, self.target_cols)

        self.X_train, self.X_test, self.y_train, self.y_test = self._train_test_split(X, y, train_size=train_size)
    
    def _get_X(self, data, feature_cols):
        """Get X features vectors assuming data is a Pandas DataFrame"""
        # TODO: make this type safe
        return data[feature_cols]

    def _get_y(self, data, target_cols):
        """Get X features vectors assuming data is a Pandas DataFrame"""
        # TODO: make this type safe
        return data[target_cols]

    def _df_to_numerical(self, data):
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
