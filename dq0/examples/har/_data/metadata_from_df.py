"""Auto populate dq0 metadata from CSV"""
import os

from dq0.sdk.data.metadata.metadata import Metadata

import numpy as np

import pandas as pd

import yaml


name = 'Human Activity Recognition'
description = 'https://github.com/fbarth/humanActivityRecognition'
type_ = 'CSV'
connection = '../dq0-sdk/dq0/examples/har/_data/dataset-har-PUC-Rio-ugulino.csv'

df = pd.read_csv(
    connection,
    sep=';',
    decimal=',')
n_rows = df.shape[0]
n_rows = int(n_rows + np.random.randint(-int(0.1 * n_rows), int(0.1 * n_rows), 1)[0])
# print(type(n_rows))

# create yaml
meta_d = {'meta_dataset': {
    'format': 'full',
    'node': {
        'type_name': 'dataset',
        'attributes': [{
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
        }],
        'child_nodes': [
            {
                'type_name': 'database',
                'child_nodes': [
                    {
                        'type_name': 'schema',
                        'child_nodes': [
                            {
                                'type_name': 'table',
                                'attributes': [
                                    {
                                        'type_name': 'list',
                                        'key': 'connector',
                                        'value': [
                                            {
                                                'type_name': 'int',
                                                'key': 'header_row',
                                                'value': 0,
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
                                        ],
                                    },
                                    {
                                        'type_name': 'list',
                                        'key': 'data',
                                        'value': [
                                            {
                                                'type_name': 'int',
                                                'key': 'rows',
                                                'value': n_rows,
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
                                                'value': '',
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
    'specification': 'dataset_standard_2021120201',
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
print(meta_yaml)

meta_dq0, _, _ = Metadata.from_yaml(yaml_content=meta_yaml)

with open(os.path.join(os.path.split(connection)[0], 'dataset-har-PUC-Rio-ugulino.yaml'), 'w') as f:
    yaml.dump(meta_d, f)
