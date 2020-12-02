# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata import Metadata


def test_read_metadata():
    # prepare yaml file
    content = '''name: 'sample data 1'
description: 'some description'
type: 'tabular'
privacy_budget: 1000
privacy_budget_interval_days: 30
database:
    Table1:
        row_privacy: true
        rows: 2000
        max_ids: 1
        sample_max_ids: true
        censor_dims: false
        user_id:
            private_id: true
            type: int
        weight:
            type: float
            lower: 0.0
            upper: 100.5
        name:
            type: string
            hide: true
        email:
            type: string
            mask: '(.*)@(.*).{3}$'
    '''
    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata
    metadata = Metadata('test.yaml')

    # test
    assert metadata.name == "sample data 1"
    assert metadata.description == "some description"
    assert metadata.type == "tabular"
    assert metadata.privacy_budget == 1000
    assert metadata.privacy_budget_interval_days == 30
    assert metadata.tables is not None
    assert len(metadata.tables) == 1
    assert metadata.tables[0].row_privacy is True
    assert metadata.tables[0].rows == 2000
    assert metadata.tables[0].max_ids == 1
    assert metadata.tables[0].sample_max_ids is True
    assert metadata.tables[0].censor_dims is False
    assert len(metadata.tables[0].columns) == 4
    assert metadata.tables[0].columns[0].name == "user_id"
    assert metadata.tables[0].columns[1].name == "weight"
    assert metadata.tables[0].columns[2].name == "name"
    assert metadata.tables[0].columns[3].name == "email"
    assert metadata.tables[0].columns[0].private_id is True
    assert metadata.tables[0].columns[1].private_id is False
    assert metadata.tables[0].columns[0].type == "int"
    assert metadata.tables[0].columns[1].lower == 0.0
    assert metadata.tables[0].columns[1].upper == 100.5
    assert metadata.tables[0].columns[2].hide is True
    assert metadata.tables[0].columns[3].hide is False
    assert metadata.tables[0].columns[3].type == "string"
    assert metadata.tables[0].columns[3].mask == "(.*)@(.*).{3}$"

    # change metadata
    metadata.privacy_budget = 1234
    metadata.description = 'new description'

    # save metadata
    metadata.write_to_yaml('test2.yaml')

    # reload metadata
    metadata = Metadata('test2.yaml')

    # test again
    assert metadata.privacy_budget == 1234
    assert metadata.description == "new description"

    # clean up
    os.remove('test.yaml')
    os.remove('test2.yaml')
