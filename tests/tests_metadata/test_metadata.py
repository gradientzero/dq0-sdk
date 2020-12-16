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
connection: 'user@db'
type: 'tabular'
privacy_budget: 1000
privacy_budget_interval_days: 30
synth_allowed: true
privacy_level: 1
Database:
    Table1:
        row_privacy: true
        rows: 2000
        max_ids: 1
        sample_max_ids: true
        censor_dims: true
        use_dpsu: true
        clamp_counts: true
        clamp_columns: true
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
        name:
            type: string
        email:
            type: string
            mask: '(.*)@(.*).{3}$'
    '''
    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata
    metadata = Metadata(filename='test.yaml')

    # test
    assert metadata.name == "sample data 1"
    assert metadata.description == "some description"
    assert metadata.connection == "user@db"
    assert metadata.type == "tabular"
    assert metadata.privacy_budget == 1000
    assert metadata.privacy_budget_interval_days == 30
    assert metadata.privacy_level == 1
    assert metadata.synth_allowed is True
    assert metadata.tables is not None
    assert len(metadata.tables) == 1
    assert metadata.tables[0].row_privacy is True
    assert metadata.tables[0].rows == 2000
    assert metadata.tables[0].max_ids == 1
    assert metadata.tables[0].sample_max_ids is True
    assert metadata.tables[0].censor_dims is True
    assert metadata.tables[0].use_dpsu is True
    assert metadata.tables[0].clamp_counts is True
    assert metadata.tables[0].clamp_columns is True
    assert len(metadata.tables[0].columns) == 5
    assert metadata.tables[0].columns[0].name == "user_id"
    assert metadata.tables[0].columns[1].name == "weight"
    assert metadata.tables[0].columns[2].name == "height"
    assert metadata.tables[0].columns[3].name == "name"
    assert metadata.tables[0].columns[4].name == "email"
    assert metadata.tables[0].columns[0].private_id is True
    assert metadata.tables[0].columns[1].private_id is False
    assert metadata.tables[0].columns[0].type == "int"
    assert metadata.tables[0].columns[1].bounded is True
    assert metadata.tables[0].columns[1].use_auto_bounds is False
    assert metadata.tables[0].columns[1].lower == 0.0
    assert metadata.tables[0].columns[1].upper == 100.5
    assert metadata.tables[0].columns[1].selectable is True
    assert metadata.tables[0].columns[2].bounded is True
    assert metadata.tables[0].columns[2].use_auto_bounds is True
    assert metadata.tables[0].columns[2].auto_bounds_prob == 0.8
    assert metadata.tables[0].columns[4].selectable is False
    assert metadata.tables[0].columns[4].type == "string"
    assert metadata.tables[0].columns[4].mask == "(.*)@(.*).{3}$"

    # change metadata
    metadata.privacy_budget = 1234
    metadata.description = 'new description'

    # save metadata
    metadata.to_yaml_file('test2.yaml')

    # reload metadata
    metadata = Metadata(filename='test2.yaml')

    # test again
    assert metadata.privacy_budget == 1234
    assert metadata.description == "new description"

    # change metadata
    metadata.privacy_budget = 5678
    metadata.description = 'new description 2'

    # dump metadata
    meta_string = metadata.to_yaml()

    # reload metadata
    metadata = Metadata(yaml=meta_string)

    # test again
    assert metadata.privacy_budget == 5678
    assert metadata.description == "new description 2"

    # test to_dict
    m_dict = metadata.to_dict()
    assert m_dict['name'] == "sample data 1"
    assert m_dict['Database']['Table1']['row_privacy'] is True
    assert m_dict['Database']['Table1']['weight']['selectable'] is True

    # tets to_dict sm
    sm_dict = metadata.to_dict_sm()
    assert 'name' not in sm_dict
    assert sm_dict['Database']['Table1']['row_privacy'] is True
    assert 'selectable' not in sm_dict['Database']['Table1']['weight']
    assert sm_dict['Database']['Table1']['weight']['upper'] == 100.5

    # clean up
    os.remove('test.yaml')
    os.remove('test2.yaml')
