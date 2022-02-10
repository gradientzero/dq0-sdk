"""Auto populate dq0 metadata from CSV"""
from dq0.sdk.data.metadata.structure.metadata import Metadata

import yaml


name = 'pneumonia'
short_name = 'pneu'
description = "some description"
connection = '../data/X_ray_pneumonia/chest_xray/feat_vec_imgs.csv'

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
                                'value': True,
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
                                        ],
                                    },
                                ],
                                'child_nodes': [
                                    {
                                        'type_name': 'column',
                                        'attributes': [
                                            {
                                                'type_name': 'list',
                                                'key': 'data',
                                                'value': [
                                                    {
                                                        'type_name': 'string',
                                                        'key': 'data_type_name',
                                                        'value': 'int',
                                                    },
                                                    {
                                                        'type_name': 'string',
                                                        'key': 'name',
                                                        'value': 'label',
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
                                            },
                                        ],
                                    },
                                ],
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
for index in range(0, 1280):
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
                        'value': 'int',
                    },
                    {
                        'type_name': 'string',
                        'key': 'name',
                        'value': f"f_{index}",
                    },
                ],
            },
            {
                'type_name': 'list',
                'key': 'machine_learning',
                'value': [
                    {
                        'type_name': 'boolean',
                        'key': 'is_feature',
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

with open('../dq0-sdk/dq0/examples/pneumonia/pneumonia_generated_full.yaml', 'w') as f:
    yaml.dump(meta_d, f)
