# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.structure.metadata import Metadata
from dq0.sdk.data.text.csv import CSV

import numpy as np

import pandas as pd


def test_csv_001():
    # prepare yaml file
    content = '''meta_dataset:
  format: simple
  node:
    dataset:
      attributes:
        'data':
          'description': "This data was extracted from the 1994 Census bureau database by Ronny Kohavi and Barry Becker (Data Mining and Visualization, Silicon Graphics). A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The prediction task is to determine whether a person makes over $50K a year."
          'metadata_is_public': true
          'name': 'Adult Census Income'
      child_nodes:
        database:
          attributes:
            'connector':
              'header_columns':
              - 'lastname'
              - 'firstname'
              - 'age'
              - 'workclass'
              - 'fnlwgt'
              - 'education'
              - 'education-num'
              - 'marital-status'
              - 'occupation'
              - 'relationship'
              - 'race'
              - 'sex'
              - 'capital-gain'
              - 'capital-loss'
              - 'hours-per-week'
              - 'native-country'
              - 'income'
              'skipinitialspace': true
              'type_name': 'csv'
              'uri': '../dq0-sdk/tests/test_sources/adult_with_rand_names.csv'
              'use_original_header': false
            'data':
              'name': 'Adult Census Income DB'
          child_nodes:
            schema:
              attributes:
                'data':
                  'name': 'Adult Census Income DB Schema'
              child_nodes:
                table:
                  attributes:
                    'data':
                      'name': 'Adult Census Income DB Table'
                      'rows': 51607
                    'differential_privacy':
                      'privacy_column': 'fnlwgt'
                  child_nodes:
                    column_0:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'age'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 20
                          'upper': 60
                        'private_synthesis':
                          'synthesizable': true
                    column_1:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'capital-gain'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 0
                          'upper': 2463
                        'private_synthesis':
                          'synthesizable': true
                    column_2:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'capital-loss'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 0
                          'upper': 0
                        'private_synthesis':
                          'synthesizable': true
                    column_3:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'education'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 123
                        'private_synthesis':
                          'synthesizable': true
                    column_4:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'education-num'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 5
                          'upper': 14
                        'private_synthesis':
                          'synthesizable': true
                    column_5:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'firstname'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 3298
                        'private_synthesis':
                          'synthesizable': true
                    column_6:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'fnlwgt'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 57233
                          'upper': 354632
                        'private_synthesis':
                          'synthesizable': true
                    column_7:
                      attributes:
                        'data':
                          'data_type_name': 'int'
                          'name': 'hours-per-week'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'lower': 20
                          'upper': 55
                        'private_synthesis':
                          'synthesizable': true
                    column_8:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'income'
                        'machine_learning':
                          'is_target': true
                        'private_sql_and_synthesis':
                          'cardinality': 2
                        'private_synthesis':
                          'synthesizable': true
                    column_9:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'lastname'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 18144
                        'private_synthesis':
                          'synthesizable': true
                    column_10:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'marital-status'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 7
                        'private_synthesis':
                          'synthesizable': true
                    column_11:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'native-country'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 42
                        'private_synthesis':
                          'synthesizable': true
                    column_12:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'occupation'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 15
                        'private_synthesis':
                          'synthesizable': true
                    column_13:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'race'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 5
                        'private_synthesis':
                          'synthesizable': true
                    column_14:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'relationship'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 6
                        'private_synthesis':
                          'synthesizable': true
                    column_15:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'sex'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 2
                        'private_synthesis':
                          'synthesizable': true
                    column_16:
                      attributes:
                        'data':
                          'data_type_name': 'string'
                          'name': 'workclass'
                        'machine_learning':
                          'is_feature': true
                        'private_sql_and_synthesis':
                          'cardinality': 9
                        'private_synthesis':
                          'synthesizable': true
  specification: 'dataset_v1'
'''  # noqa: E501

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
    metadata = Metadata.from_yaml_file(filename='test.yaml')
    m_interface = Interface(metadata=metadata)

    # get data_source instance and load data
    data_source = CSV(meta_database=m_interface.dataset().database())
    df = data_source.read()

    # test dataframe has correct header
    header_columns = m_interface.dataset().database().connector.header_columns
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
    na_bool = df.iloc[[0], :].isna()
    assert na_bool.iloc[0, 8]
    assert na_bool.iloc[0, -3]

    # change separator
    df.to_csv('test.csv', index=False, sep=';')
    data_source.use_original_header = True

    # test reads with different separator
    data_source.path = 'test.csv'
    df = data_source.read(names=None)
    assert df.shape == (10, 1)

    data_source.sep = ';'
    df = data_source.read(names=None)
    assert df.shape == (10, 17)

    # add float column with comma for deicmal
    df['float'] = '1,0'
    df.to_csv('test.csv', index=False, sep=';')

    # test decimal
    df = data_source.read()
    assert df.dtypes[-1] == 'object'
    data_source.decimal = ','
    df = data_source.read()
    assert df.dtypes[-1] == 'float64'

    # test skiprows as kwargs
    df = data_source.read(names=None, skiprows=np.arange(1, 6))
    assert df.shape == (5, 18)

    # test multicolumn index
    columns = pd.MultiIndex.from_product([df.columns, ['test']])
    df.columns = columns
    df.to_csv('test.csv', index=False, sep=';')
    data_source.header_row = [0, 1]
    df = data_source.read(names=None)
    assert df.columns.__class__.__name__ == 'MultiIndex'

    # test mutliindex with skiprows
    df = data_source.read(names=None, skiprows=[2])
    assert df.columns.__class__.__name__ == 'MultiIndex'
    assert df.shape[0] == 4

    # clean up
    os.remove('test.yaml')
    os.remove('test.csv')


if __name__ == "__main__":
  test_csv_001()
