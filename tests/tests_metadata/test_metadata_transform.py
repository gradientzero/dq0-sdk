# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

# the unused imports are necessary for the repr evaluation
from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.verifier import Verifier


def test_metadata_print():
    # prepare yaml file
    content = '''type_name: 'dataset'
attributes:
    -
        type_name: 'string'
        key: 'name'
        value: 'test_ds'
    -
        type_name: 'string'
        key: 'description'
        value: "some description"
    -
        type_name: 'list'
        key: 'dataset_tags'
        value:
            -
                type_name: 'string'
                value: 'tag1'
            -
                type_name: 'string'
                value: 'tag2'
    -
        type_name: 'boolean'
        key: 'metadata_is_public'
        value: true
child_nodes:
    -
        type_name: 'database'
        child_nodes:
            -
                type_name: 'schema'
                child_nodes:
                    -
                        type_name: 'table'
                        attributes:
                            -
                                type_name: 'list'
                                key: 'connector'
                                value:
                                    -
                                        type_name: 'string'
                                        key: 'type_name'
                                        value: 'csv'
                                    -
                                        type_name: 'string'
                                        key: 'uri'
                                        value: 'user@db'
                                    -
                                        type_name: 'boolean'
                                        key: 'use_original_header'
                                        value: true
                                    -
                                        type_name: 'list'
                                        key: 'header_row'
                                        value:
                                            -
                                                type_name: 'int'
                                                value: 1
                                            -
                                                type_name: 'int'
                                                value: 2
                                    -
                                        type_name: 'list'
                                        key: 'na_values'
                                        value:
                                            -
                                                type_name: 'string'
                                                key: 'weight'
                                                value: '?'
                                            -
                                                type_name: 'string'
                                                key: 'height'
                                                value: '??'
                            -
                                type_name: 'int'
                                key: 'privacy_level'
                                value: 1
                            -
                                type_name: 'string'
                                key: 'privacy_column'
                                value: 'user_id'
                            -
                                type_name: 'float'
                                key: 'budget_epsilon'
                                value: 1000.0
                            -
                                type_name: 'float'
                                key: 'budget_delta'
                                value: 500.0
                            -
                                type_name: 'boolean'
                                key: 'synth_allowed'
                                value: true
                            -
                                type_name: 'float'
                                key: 'tau'
                                value: 99.0
                            -
                                type_name: 'boolean'
                                key: 'row_privacy'
                                value: true
                            -
                                type_name: 'int'
                                key: 'rows'
                                value: 2000
                            -
                                type_name: 'int'
                                key: 'max_ids'
                                value: 1
                            -
                                type_name: 'boolean'
                                key: 'sample_max_ids'
                                value: true
                            -
                                type_name: 'boolean'
                                key: 'use_dpsu'
                                value: true
                            -
                                type_name: 'boolean'
                                key: 'clamp_counts'
                                value: true
                            -
                                type_name: 'boolean'
                                key: 'clamp_columns'
                                value: true
                            -
                                type_name: 'boolean'
                                key: 'censor_dims'
                                value: true
                        child_nodes:
                            -
                                type_name: 'column'
                                attributes:
                                    -
                                        type_name: 'string'
                                        key: 'name'
                                        value: 'user_id'
                                    -
                                        type_name: 'list'
                                        key: 'data'
                                        value:
                                            -
                                                type_name: 'string'
                                                key: 'data_type_name'
                                                value: 'int'
                                    -
                                        type_name: 'boolean'
                                        key: 'private_id'
                                        value: true
                            -
                                type_name: 'column'
                                attributes:
                                    -
                                        type_name: 'string'
                                        key: 'name'
                                        value: 'weight'
                                    -
                                        type_name: 'string'
                                        key: 'data_type_name'
                                        value: 'float'
                                    -
                                        type_name: 'boolean'
                                        key: 'selectable'
                                        value: true
                                    -
                                        type_name: 'boolean'
                                        key: 'bounded'
                                        value: true
                                    -
                                        type_name: 'float'
                                        key: 'lower'
                                        value: 0.0
                                    -
                                        type_name: 'float'
                                        key: 'upper'
                                        value: 100.5
                            -
                                type_name: 'column'
                                attributes:
                                    -
                                        type_name: 'string'
                                        key: 'name'
                                        value: 'height'
                                    -
                                        type_name: 'string'
                                        key: 'data_type_name'
                                        value: 'float'
                                    -
                                        type_name: 'boolean'
                                        key: 'bounded'
                                        value: true
                                    -
                                        type_name: 'boolean'
                                        key: 'use_auto_bounds'
                                        value: true
                                    -
                                        type_name: 'float'
                                        key: 'auto_bounds_prob'
                                        value: 0.8
                                    -
                                        type_name: 'boolean'
                                        key: 'discrete'
                                        value: true
                                    -
                                        type_name: 'float'
                                        key: 'min_step'
                                        value: 0.5
                                    -
                                        type_name: 'boolean'
                                        key: 'synthesizable'
                                        value: false
                            -
                                type_name: 'column'
                                attributes:
                                    -
                                        type_name: 'string'
                                        key: 'name'
                                        value: 'name'
                                    -
                                        type_name: 'string'
                                        key: 'data_type_name'
                                        value: 'string'
                                    -
                                        type_name: 'boolean'
                                        key: 'synthesizable'
                                        value: true
                            -
                                type_name: 'column'
                                attributes:
                                    -
                                        type_name: 'string'
                                        key: 'name'
                                        value: 'email'
                                    -
                                        type_name: 'string'
                                        key: 'data_type_name'
                                        value: 'string'
                                    -
                                        type_name: 'string'
                                        key: 'mask'
                                        value: '(.*)@(.*).{3}$'
                                    -
                                        type_name: 'int'
                                        key: 'cardinality'
                                        value: 123
'''

    # load metadata
    metadata = Metadata.from_yaml(yaml_content=content, apply_default_attributes=None, verify_func=Verifier.verifyAllSingleWithSchema)

    # test to_yaml
    metadata2 = Metadata.from_yaml(yaml_content=metadata.to_yaml(), apply_default_attributes=None, verify_func=Verifier.verifyAllSingleWithSchema)
    assert repr(metadata) == repr(metadata2)

    # test str
    metadata3 = Metadata.from_yaml(yaml_content=str(metadata), apply_default_attributes=None, verify_func=Verifier.verifyAllSingleWithSchema)
    assert repr(metadata) == repr(metadata3)

    # test repr
    assert repr(metadata) == repr(eval(repr(metadata)))
