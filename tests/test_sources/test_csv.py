# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata import Metadata
from dq0.sdk.data.text.csv import CSV

import numpy as np


def test_csv():
    # prepare yaml file
    content = '''description: 'This data was extracted from the 1994 Census bureau database by Ronny
  Kohavi and Barry Becker (Data Mining and Visualization, Silicon Graphics). A set
  of reasonably clean records was extracted using the following conditions: ((AAGE>16)
  && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The prediction task is to determine whether
  a person makes over $50K a year.'
name: Adult Census Income
privacy_column: fnlwgt
schema:
  connection: ../dq0-sdk/tests/test_sources/adult_with_rand_names.csv
  table:
    age:
      is_feature: true
      lower: 20
      synthesizable: true
      type: int
      upper: 60
    capital-gain:
      is_feature: true
      lower: 0
      synthesizable: true
      type: int
      upper: 2463
    capital-loss:
      is_feature: true
      lower: 0
      synthesizable: true
      type: int
      upper: 0
    education:
      cardinality: 16
      is_feature: true
      synthesizable: true
      type: string
    education-num:
      is_feature: true
      lower: 5
      synthesizable: true
      type: int
      upper: 14
    firstname:
      cardinality: 3298
      is_feature: true
      synthesizable: true
      type: string
    fnlwgt:
      is_feature: true
      lower: 57233
      synthesizable: true
      type: int
      upper: 354632
    header_columns:
    - lastname
    - firstname
    - age
    - workclass
    - fnlwgt
    - education
    - education-num
    - marital-status
    - occupation
    - relationship
    - race
    - sex
    - capital-gain
    - capital-loss
    - hours-per-week
    - native-country
    - income
    hours-per-week:
      is_feature: true
      lower: 20
      synthesizable: true
      type: int
      upper: 55
    income:
      cardinality: 2
      is_target: true
      synthesizable: true
      type: string
    lastname:
      cardinality: 18144
      is_feature: true
      synthesizable: true
      type: string
    marital-status:
      cardinality: 7
      is_feature: true
      synthesizable: true
      type: string
    native-country:
      cardinality: 42
      is_feature: true
      synthesizable: true
      type: string
    occupation:
      cardinality: 15
      is_feature: true
      synthesizable: true
      type: string
    race:
      cardinality: 5
      is_feature: true
      synthesizable: true
      type: string
    relationship:
      cardinality: 6
      is_feature: true
      synthesizable: true
      type: string
    rows: 51607
    sex:
      cardinality: 2
      is_feature: true
      synthesizable: true
      type: string
    use_original_header: false
    workclass:
      cardinality: 9
      is_feature: true
      synthesizable: true
      type: string
    skipinitialspace: true
type: CSV
    '''

    na_values = {
        'capital-gain': 99999,
        'capital-loss': 99999,
        'hours-per-week': 99,
        'workclass': '?',
        'native-country': '?',
        'occupation': '?'}

    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata
    metadata = Metadata(filename='test.yaml')

    # get ml_dict
    meta_ml = metadata.to_metadata_ml()

    # get data_source instance and load data
    data_source = CSV(path=metadata.schemas['schema'].connection, meta_ml=meta_ml)
    df = data_source.read()

    # test dataframe has correct header
    header_columns = metadata.schemas['schema'].tables['table'].header_columns
    header_columns_df = list(df.columns.values)
    header_columns_diff = [i for i in header_columns + header_columns_df if i not in header_columns or i not in header_columns_df]
    assert len(header_columns_diff) == 0

    # test na_values are present
    assert df.iloc[0, 8] == '?'
    assert df.iloc[0, -3] == 99
    
    # add na_values to data_source
    data_source.na_values = na_values

    # read data again
    df = data_source.read()

    # test na_values are nan
    na_bool = df.iloc[[0],:].isna()
    assert na_bool.iloc[0, 8]
    assert na_bool.iloc[0, -3]

    # change separator
    df.to_csv('test.csv', index=False, sep=';')

    # test reads with different separator
    data_source.path = 'test.csv'
    data_source.use_original_header = True
    df = data_source.read()
    assert df.shape == (10, 1)
    
    data_source.sep = ';'
    df = data_source.read()
    assert df.shape == (10, 17)

    # TODO: add decimal test, ...

    # clean up
    os.remove('test.yaml')
    os.remove('test.csv')


