# -*- coding: utf-8 -*-
"""
Adult dataset loading

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>

Copyright 2019, Gradient Zero
"""

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.csv.csv_source import CSVSource
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import minmax_scale

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import tensorflow as tf

class PatientSource(CSVSource):

    def __init__(self, file_path, **kwargs):
        super().__init__(file_path,**kwargs)
        
    
    def prepare_data(self, data):

        le = LabelEncoder()
        data['GENDER_NUM'] = le.fit_transform(data['GENDER'])
        data['BIRTHPLACE_NUM'] = le.fit_transform(data['BIRTHPLACE'])
        data['CITY_NUM'] = le.fit_transform(data['CITY'])
        data['STATE_NUM'] = le.fit_transform(data['STATE'])
        data['COUNTY_NUM'] = le.fit_transform(data['COUNTY'])

        data['BIRTHDATE'] = [pd.Timestamp(ts) for ts in df['patients']['BIRTHDATE']]
        data['BIRTHDATE_UNIX'] = data['BIRTHDATE'].astype(int)/ 10**9

        target_col = 'BIRTHDATE_UNIX'
        col_selecion = ['GENDER_NUM','BIRTHPLACE_NUM','CITY_NUM','STATE_NUM','COUNTY_NUM','ZIP','LAT','LON','HEALTHCARE_EXPENSES',
                    'HEALTHCARE_COVERAGE']

        X_df = data[col_selecion].fillna(0.)
        y_df = data[target_col]

        X = X_df.values
        y = y_df.values

        X_scale = minmax_scale(X)
        y_scale = minmax_scale(y)

        return X_scale, y_scale
