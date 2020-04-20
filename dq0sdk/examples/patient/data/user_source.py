# -*- coding: utf-8 -*-
"""Patient Data Source Example

https://synthea.mitre.org/downloads

Copyright 2020, Gradient Zero
"""

from dq0sdk.data.csv.csv_source import CSVSource

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import minmax_scale


class UserSource(CSVSource):
    """Patient Data Source class.

    Example data source for regression model.
    """
    def __init__(self, file_path):
        super().__init__(file_path)

    def prepare_data(self, data):

        le = LabelEncoder()
        data['GENDER_NUM'] = le.fit_transform(data['GENDER'])
        data['BIRTHPLACE_NUM'] = le.fit_transform(data['BIRTHPLACE'])
        data['CITY_NUM'] = le.fit_transform(data['CITY'])
        data['STATE_NUM'] = le.fit_transform(data['STATE'])
        data['COUNTY_NUM'] = le.fit_transform(data['COUNTY'])

        data['BIRTHDATE'] = [pd.Timestamp(ts) for ts in data['BIRTHDATE']]
        data['BIRTHDATE_UNIX'] = data['BIRTHDATE'].astype(int) / 10**9

        target_col = 'BIRTHDATE_UNIX'
        col_selecion = ['GENDER_NUM', 'BIRTHPLACE_NUM', 'CITY_NUM', 'STATE_NUM', 'COUNTY_NUM',
                        'ZIP', 'LAT', 'LON', 'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE']

        X_df = data[col_selecion].fillna(0.)
        y_df = data[target_col]

        X = X_df.values
        y = y_df.values

        X_scale = minmax_scale(X)
        y_scale = minmax_scale(y)

        return X_scale, y_scale
