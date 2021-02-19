"""Auto populate dq0 metadata from CSV"""
import os

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

name = 'Adult Census Income'
description = 'This data was extracted from the 1994 Census bureau ' \
              'database by Ronny Kohavi and Barry Becker (Data Mining and ' \
              'Visualization, Silicon Graphics). A set of reasonably clean ' \
              'records was extracted using the following conditions: ' \
              '((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The ' \
              'prediction task is to determine whether a person makes over ' \
              '$50K a year.'
type_ = 'CSV'
connection = '../dq0-sdk/dq0/sdk/examples/census/_data/adult_with_rand_names' \
             '.csv'

df = pd.read_csv(
    connection,
    names=column_names_list
    )
n_rows = df.shape[0]
n_rows = int(n_rows + np.random.randint(-int(0.1*n_rows),int(0.1*n_rows),1)[0])
# print(type(n_rows))

# create yaml
meta_d = {}
meta_d['name'] = name
meta_d['description'] = description
meta_d['type'] = type_
meta_d['privacy_column'] = 'fnlwgt'

schema = meta_d['schema'] = {}
schema['connection'] = connection

table = schema['table'] = {}
table['rows'] = n_rows
# add columns
for c in df.columns:
    column = table[c] = {}
    dtype_ = df[c].dtype
    card = None
    lower = None
    upper = None
    if dtype_=='object':
        dtype_ = 'string'
        card = df[c].nunique()
    if dtype_=='int64':
        dtype_ = 'int'
        lower = int(df[c].quantile(np.random.uniform(0.05, 0.10, 1)))
        upper = int(df[c].quantile(np.random.uniform(0.9, 0.95, 1)))
    if dtype_=='float':
        dtype_ = 'float'
        lower = float(df[c].quantile(np.random.uniform(0.05, 0.10, 1)))
        upper = float(df[c].quantile(np.random.uniform(0.9, 0.95, 1)))

    column['type'] = dtype_
    column['synthesizable'] = True
    if card is not None:
        column['cardinality'] = card
    if lower is not None:
        column['lower'] = lower
    if upper is not None:
        column['upper'] = upper

meta_yaml = yaml.dump(meta_d)
print(meta_yaml)

from dq0.sdk.data.metadata.metadata import Metadata

meta_dq0 = Metadata(yaml=meta_yaml)

with open(os.path.join(os.path.split(connection)[0],'metadata.yaml'), 'w') as f:
    yaml.dump(meta_d, f)
meta_dq0.to_yaml_file(os.path.join(os.path.split(connection)[0],'metadata_parsed.yaml'))
