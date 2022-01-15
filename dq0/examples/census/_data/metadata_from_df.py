"""Auto populate dq0 metadata from CSV"""
import os

from dq0.sdk.data.metadata.metadata import Metadata

import numpy as np

import pandas as pd

import yaml

column_names_list = [
    'lastname',
    'firstname',
    'age',
    'workclass',
    'fnlwgt',
    'education',
    'education-num',
    'marital-status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'capital-gain',
    'capital-loss',
    'hours-per-week',
    'native-country',
    'income'
]

na_values_d = {
    'capital-gain': 99999,
    'capital-loss': 99999,
    'hours-per-week': 99,
    'workclass': '?',
    'native-country': '?',
    'occupation': '?'}

target_col = 'income'

name = "Adult Census Income"
short_name = 'ACI'
description = 'This data was extracted from the 1994 Census bureau ' \
              'database by Ronny Kohavi and Barry Becker (Data Mining and ' \
              'Visualization, Silicon Graphics). A set of reasonably clean ' \
              'records was extracted using the following conditions: ' \
              '((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The ' \
              'prediction task is to determine whether a person makes over ' \
              '$50K a year.'
connection = '../dq0-sdk/dq0/examples/census/_data/adult_with_rand_names' \
             '.csv'

df = pd.read_csv(
    connection,
    names=column_names_list,
    na_values=na_values_d)
n_rows = df.shape[0]
n_rows = int(n_rows + np.random.randint(-int(0.1 * n_rows), int(0.1 * n_rows), 1)[0])
# print(type(n_rows))

# create yaml
meta_d = {'meta_dataset': {
    'format': 'full',
    'node': {
        'type_name': 'dataset',
        'attributes': [
            {
                'type_name': 'list',
                'key': 'data',
                'value': [
                    {
                        'type_name': 'string',
                        'key': 'description',
                        'value': description,
                    },
                    {
                        'type_name': 'string',
                        'key': 'name',
                        'value': name,
                    },
                ],
            },
        ],
        'child_nodes': [
            {
                'type_name': 'database',
                'attributes': [
                    {
                        'type_name': 'list',
                        'key': 'connector',
                        'value': [
                            {
                                'type_name': 'list',
                                'key': 'header_columns',
                                'value': [
                                    {
                                        'type_name': 'string',
                                        'value': value,
                                    } for value in column_names_list
                                ],
                            },
                            {
                                'type_name': 'list',
                                'key': 'na_values',
                                'value': [
                                    {
                                        'type_name': 'int' if isinstance(value, int) else 'string',
                                        'key': key,
                                        'value': value,
                                    } for key, value in na_values_d.items()
                                ],
                            },
                            {
                                'type_name': 'boolean',
                                'key': 'skipinitialspace',
                                'value': True,
                            },
                            {
                                'type_name': 'string',
                                'key': 'type_name',
                                'value': 'csv',
                            },
                            {
                                'type_name': 'string',
                                'key': 'uri',
                                'value': connection,
                            },
                            {
                                'type_name': 'boolean',
                                'key': 'use_original_header',
                                'value': False,
                            },
                        ],
                    },
                    {
                        'type_name': 'list',
                        'key': 'data',
                        'value': [
                            {
                                'type_name': 'string',
                                'key': 'name',
                                'value': short_name + " database",
                            },
                        ],
                    },
                ],
                'child_nodes': [
                    {
                        'type_name': 'schema',
                        'attributes': [
                            {
                                'type_name': 'list',
                                'key': 'data',
                                'value': [
                                    {
                                        'type_name': 'string',
                                        'key': 'name',
                                        'value': short_name + " schema",
                                    },
                                ],
                            },
                        ],
                        'child_nodes': [
                            {
                                'type_name': 'table',
                                'attributes': [
                                    {
                                        'type_name': 'list',
                                        'key': 'data',
                                        'value': [
                                            {
                                                'type_name': 'int',
                                                'key': 'rows',
                                                'value': n_rows,
                                            },
                                            {
                                                'type_name': 'string',
                                                'key': 'name',
                                                'value': short_name + " table",
                                            },
                                        ],
                                    },
                                    {
                                        'type_name': 'list',
                                        'key': 'differential_privacy',
                                        'value': [
                                            {
                                                'type_name': 'string',
                                                'key': 'privacy_column',
                                                'value': 'fnlwgt',
                                            },
                                        ],
                                    },
                                ],
                                'child_nodes': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    'specification': 'dataset_v1',
}}

# add columns
for c in df.columns:
    dtype_ = df[c].dtype
    card = None
    lower = None
    upper = None
    if dtype_ == 'object':
        dtype_ = 'string'
        card = df[c].nunique()
    if dtype_ == 'int64':
        dtype_ = 'int'
        lower = int(df[c].quantile(np.random.uniform(0.05, 0.10, 1)))
        upper = int(df[c].quantile(np.random.uniform(0.9, 0.95, 1)))
    if dtype_ == 'float':
        dtype_ = 'float'
        lower = float(df[c].quantile(np.random.uniform(0.05, 0.10, 1)))
        upper = float(df[c].quantile(np.random.uniform(0.9, 0.95, 1)))

    meta_d['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes'].append({
        'type_name': 'column',
        'attributes': [
            {
                'type_name': 'list',
                'key': 'data',
                'value': [
                    {
                        'type_name': 'string',
                        'key': 'data_type_name',
                        'value': dtype_,
                    },
                    {
                        'type_name': 'string',
                        'key': 'name',
                        'value': c,
                    },
                ],
            },
            {
                'type_name': 'list',
                'key': 'machine_learning',
                'value': [
                    {
                        'type_name': 'boolean',
                        'key': 'is_target' if c == target_col else 'is_feature',
                        'value': True,
                    },
                ],
            },
            {
                'type_name': 'list',
                'key': 'private_sql_and_synthesis',
                'value': [
                    {
                        'type_name': 'int',
                        'key': 'cardinality',
                        'value': card,
                    },
                ] if card is not None else [
                    {
                        'type_name': dtype_,
                        'key': 'lower',
                        'value': lower,
                    },
                    {
                        'type_name': dtype_,
                        'key': 'upper',
                        'value': upper,
                    },
                ],
            },
            {
                'type_name': 'list',
                'key': 'private_synthesis',
                'value': [
                    {
                        'type_name': 'boolean',
                        'key': 'synthesizable',
                        'value': True,
                    },
                ],
            },
        ],
    })

meta_yaml = yaml.dump(meta_d)
meta_dq0 = Metadata.from_yaml(yaml_content=meta_yaml)
print(f"Internal full: {meta_dq0.to_yaml(request_uuids=None)}")
print(f"Outputted yaml file content: {meta_yaml}")

with open(os.path.join(os.path.split(connection)[0], 'adult_with_rand_names_generated_full.yaml'), 'w') as f:
    yaml.dump(meta_d, f)
