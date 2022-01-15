"""Auto populate dq0 metadata from CSV"""
import os

from dq0.sdk.data.metadata.metadata import Metadata

import numpy as np

import pandas as pd

import yaml


feature_cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
label_cols = ['charges']

name = 'medical_insurance'
short_name = 'm_i'
description = 'description'
connection = '../dq0-sdk/dq0/examples/medical_insurance/_data/datasets_13720_18513_insurance.csv'

df = pd.read_csv(
    connection)
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
            }
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
                                'type_name': 'int',
                                'key': 'header_row',
                                'value': 0
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
                                'type_name': 'string',
                                'key': 'name',
                                'value': short_name + " database",
                            },
                        ],
                    }
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
                            }
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
                                                'type_name': 'string',
                                                'key': 'name',
                                                'value': short_name + " table",
                                            },
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
                        'key': 'is_target',
                        'value': True,
                    },
                ],
            } if c in label_cols else {
                'type_name': 'list',
                'key': 'machine_learning',
                'value': [
                    {
                        'type_name': 'boolean',
                        'key': 'is_feature',
                        'value': c in feature_cols,
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

with open(os.path.join(os.path.split(connection)[0], 'datasets_13720_18513_insurance_generated_full.yaml'), 'w') as f:
    yaml.dump(meta_d, f)
