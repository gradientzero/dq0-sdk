# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata import Metadata


def test_metadata():
    # prepare yaml file
    content = '''name: 'sample data 1'
description: 'some description'
type: 'CSV'
privacy_column: 'user_id'
Database:
    connection: 'user@db'
    size: 1001
    privacy_budget: 1000
    privacy_budget_interval_days: 30
    synth_allowed: true
    privacy_level: 1
    Table1:
        row_privacy: true
        rows: 2000
        max_ids: 1
        sample_max_ids: true
        censor_dims: true
        use_dpsu: true
        clamp_counts: true
        clamp_columns: true
        tau: 99
        user_id:
            private_id: true
            type: int
        weight:
            type: float
            bounded: true
            lower: 0.0
            upper: 100.5
            selectable: true
        height:
            type: float
            bounded: true
            use_auto_bounds: true
            auto_bounds_prob: 0.8
            synthesizable: false
        name:
            type: string
            synthesizable: true
        email:
            type: string
            mask: '(.*)@(.*).{3}$'
            cardinality: 123
    '''
    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata
    metadata = Metadata(filename='test.yaml')

    # test
    assert metadata.name == "sample data 1"
    assert metadata.description == "some description"
    assert metadata.type == "CSV"
    assert metadata.privacy_column == 'user_id'
    assert metadata.schemas['Database'].connection == "user@db"
    assert metadata.schemas['Database'].size == 1001
    assert metadata.schemas['Database'].privacy_budget == 1000
    assert metadata.schemas['Database'].privacy_budget_interval_days == 30
    assert metadata.schemas['Database'].privacy_level == 1
    assert metadata.schemas['Database'].synth_allowed is True
    assert metadata.schemas['Database'].tables['Table1'].row_privacy is True
    assert metadata.schemas['Database'].tables['Table1'].rows == 2000
    assert metadata.schemas['Database'].tables['Table1'].max_ids == 1
    assert metadata.schemas['Database'].tables['Table1'].sample_max_ids is True
    assert metadata.schemas['Database'].tables['Table1'].censor_dims is True
    assert metadata.schemas['Database'].tables['Table1'].use_dpsu is True
    assert metadata.schemas['Database'].tables['Table1'].clamp_counts is True
    assert metadata.schemas['Database'].tables['Table1'].clamp_columns is True
    assert metadata.schemas['Database'].tables['Table1'].tau == 99
    assert len(metadata.schemas['Database'].tables['Table1'].columns.keys()) == 5
    assert metadata.schemas['Database'].tables['Table1'].columns['user_id'].name == "user_id"
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].name == "weight"
    assert metadata.schemas['Database'].tables['Table1'].columns['height'].name == "height"
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].synthesizable is True
    assert metadata.schemas['Database'].tables['Table1'].columns['height'].synthesizable is False
    assert metadata.schemas['Database'].tables['Table1'].columns['name'].synthesizable is True
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].cardinality == 123
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].synthesizable is True
    assert metadata.schemas['Database'].tables['Table1'].columns['name'].name == "name"
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].name == "email"
    assert metadata.schemas['Database'].tables['Table1'].columns['user_id'].private_id is True
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].private_id is False
    assert metadata.schemas['Database'].tables['Table1'].columns['user_id'].type == "int"
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].bounded is True
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].use_auto_bounds is False
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].lower == 0.0
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].upper == 100.5
    assert metadata.schemas['Database'].tables['Table1'].columns['weight'].selectable is True
    assert metadata.schemas['Database'].tables['Table1'].columns['height'].bounded is True
    assert metadata.schemas['Database'].tables['Table1'].columns['height'].use_auto_bounds is True
    assert metadata.schemas['Database'].tables['Table1'].columns['height'].auto_bounds_prob == 0.8
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].selectable is False
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].type == "string"
    assert metadata.schemas['Database'].tables['Table1'].columns['email'].mask == "(.*)@(.*).{3}$"

    # change metadata
    metadata.schemas['Database'].privacy_budget = 1234
    metadata.description = 'new description'

    # save metadata
    yaml_string = metadata.to_yaml()

    # reload metadata
    metadata = Metadata(yaml=yaml_string)

    # test again
    assert metadata.schemas['Database'].privacy_budget == 1234
    assert metadata.description == "new description"

    # change metadata
    metadata.schemas['Database'].privacy_budget = 5678
    metadata.description = 'new description 2'

    # dump metadata
    meta_string = metadata.to_yaml()

    # reload metadata
    metadata = Metadata(yaml=meta_string)

    # test again
    assert metadata.schemas['Database'].privacy_budget == 5678
    assert metadata.description == "new description 2"

    # test drop columns
    metadata.drop_columns_with_key_value('synthesizable', False)
    assert len(metadata.schemas['Database'].tables['Table1'].columns) == 4

    # test to_dict
    m_dict = metadata.to_dict()
    assert m_dict['name'] == "sample data 1"
    assert m_dict['Database']['Table1']['row_privacy'] is True
    assert m_dict['Database']['Table1']['weight']['selectable'] is True

    # tets to_dict sm
    sm_dict = metadata.to_dict_sm()
    assert 'name' not in sm_dict
    assert sm_dict['Collection']['Database']['Table1']['row_privacy'] is True
    assert 'selectable' not in sm_dict['Collection']['Database']['Table1']['weight']
    assert sm_dict['Collection']['Database']['Table1']['weight']['upper'] == 100.5
    assert sm_dict['Collection']['Database']['Table1']['email']['cardinality'] == 123

    # clean up
    os.remove('test.yaml')


def test_combine_metadata():
    # prepare yaml file
    content1 = '''name: 'sample data 1'
description: 'some description'
type: 'CSV'
Database1:
    connection: 'user1@db'
    privacy_budget: 1000
    privacy_budget_interval_days: 30
    synth_allowed: true
    privacy_level: 1
    Table1:
        row_privacy: true
        rows: 1000
        user_id:
            private_id: true
            type: int
    '''

    content2 = '''name: 'sample data 2'
description: 'some description'
type: 'CSV'
Database2:
    connection: 'user@db'
    privacy_budget: 1001
    privacy_budget_interval_days: 30
    synth_allowed: true
    privacy_level: 1
    Table2:
        row_privacy: false
        rows: 2000
        email:
            private_id: true
            type: string
    '''

    content3 = '''name: 'sample data 3'
description: 'some description'
type: 'CSV'
Database1:
    connection: 'user3@db'
    privacy_budget: 1000
    privacy_budget_interval_days: 30
    synth_allowed: true
    privacy_level: 1
    Table3:
        row_privacy: false
        rows: 3000
        weight:
            type: int
    '''
    # load metadata
    metadata1 = Metadata(yaml=content1)
    metadata2 = Metadata(yaml=content2)
    metadata3 = Metadata(yaml=content3)

    metadata1.combine_with(metadata2)
    metadata1.combine_with(metadata3)

    assert metadata1.schemas['Database1'].connection == 'user1@db'
    assert metadata1.schemas['Database2'].privacy_budget == 1001
    assert metadata1.schemas['Database1'].tables['Table1'].row_privacy is True
    assert metadata1.schemas['Database1'].tables['Table3'].row_privacy is False
    assert metadata1.schemas['Database2'].tables['Table2'].rows == 2000
    assert metadata1.schemas['Database2'].tables['Table2'].columns['email'].type == 'string'
