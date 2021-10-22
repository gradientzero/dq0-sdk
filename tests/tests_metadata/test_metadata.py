# -*- coding: utf-8 -*-
"""Metadata tests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.meta_filter import MetaFilter
from dq0.sdk.data.metadata.meta_verifier import MetaVerifier
from dq0.sdk.data.metadata.section.meta_section import MetaSection
from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType


def test_metadata():
    # prepare yaml file
    content = '''type_name: 'dataset'
name: 'test_ds'
description: 'some description'
is_public: true
sections:
    -
        type_name: 'dataset_tags'
        name: 'test_section_ds_tags'
        tags:
            - 'tag1'
            - 'tag2'
child_nodes:
    -
        type_name: 'database'
        name: 'test_db'
        child_nodes:
            -
                type_name: 'schema'
                name: 'test_sch'
                child_nodes:
                    -
                        type_name: 'table'
                        name: 'test_tab'
                        connector:
                            type_name: 'csv'
                            uri: 'user@db'
                            use_original_header: true
                            header_row:
                                - 1
                                - 2
                            na_values:
                                weight: '?'
                                height: '??'
                        sections:
                            -
                                type_name: 'table_differential_privacy'
                                name: 'test_section_tab_dp'
                                budget_epsilon: 1000
                                budget_delta: 500
                            -
                                type_name: 'table_smart_noise'
                                name: 'test_section_tab_sm'
                                row_privacy: true
                                rows: 2000
                                max_ids: 1
                                sample_max_ids: true
                                use_dpsu: true
                                clamp_counts: true
                                clamp_columns: true
                                censor_dims: true
                            -
                                type_name: 'table_other'
                                name: 'test_section_tab_oth'
                                synth_allowed: true
                                tau: 99
                            -
                                type_name: 'table_privacy'
                                name: 'test_section_tab_priv'
                                privacy_level: 1
                                privacy_column: 'user_id'
                        child_nodes:
                            -
                                type_name: 'column'
                                name: 'user_id'
                                sections:
                                    -
                                        type_name: 'column'
                                        name: 'test_section_col_user_id'
                                        data_type_name: 'int'
                                    -
                                        type_name: 'column_smart_noise'
                                        name: 'test_section_col_sm_user_id'
                                        private_id: true
                            -
                                type_name: 'column'
                                name: 'weight'
                                sections:
                                    -
                                        type_name: 'column'
                                        name: 'test_section_col_weight'
                                        data_type_name: 'float'
                                        selectable: true
                                    -
                                        type_name: 'column_smart_noise_float'
                                        name: 'test_section_col_sm_float_weight'
                                        bounded: true
                                        lower: 0.0
                                        upper: 100.5
                            -
                                type_name: 'column'
                                name: 'height'
                                sections:
                                    -
                                        type_name: 'column'
                                        name: 'test_section_col_height'
                                        data_type_name: 'float'
                                    -
                                        type_name: 'column_float'
                                        name: 'test_section_col_float_height'
                                        use_auto_bounds: true
                                        auto_bounds_prob: 0.8
                                        discrete: true
                                        min_step: 0.5
                                        synthesizable: false
                                    -
                                        type_name: 'column_smart_noise_float'
                                        name: 'test_section_col_sm_float_height'
                                        bounded: true
                            -
                                type_name: 'column'
                                name: 'name'
                                sections:
                                    -
                                        type_name: 'column'
                                        name: 'test_section_col_name'
                                        data_type_name: 'string'
                                    -
                                        type_name: 'column_string'
                                        name: 'test_section_col_string_name'
                                        synthesizable: true
                            -
                                type_name: 'column'
                                name: 'email'
                                sections:
                                    -
                                        type_name: 'column'
                                        name: 'test_section_col_email'
                                        data_type_name: 'string'
                                    -
                                        type_name: 'column_string'
                                        name: 'test_section_col_string_email'
                                        mask: '(.*)@(.*).{3}$'
                                        cardinality: 123
'''
    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata
    metadata = Metadata.from_yaml_file('test.yaml', MetaVerifier.verifySingleTable)

    # test
    assert metadata.root_node.type_name == 'dataset'
    assert metadata.root_node.name == 'test_ds'
    assert metadata.root_node.description == "some description"
    assert metadata.root_node.is_public is True
    assert 'tag1' in metadata.root_node.sections[0].tags
    assert 'tag2' in metadata.root_node.sections[0].tags
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.type_name == 'csv'
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.uri == 'user@db'
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.use_original_header is True
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.header_row == [1, 2]
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.sep == ','
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.decimal == '.'
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.na_values == {'weight': '?', 'height': '??'}
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.index_col is None
    assert metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector.skipinitialspace is False
    table_privacy_section = None
    table_other_section = None
    table_differential_privacy_section = None
    table_smart_noise_section = None
    for section in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].sections:
        if section.type_name == 'table_privacy':
            table_privacy_section = section
        elif section.type_name == 'table_other':
            table_other_section = section
        elif section.type_name == 'table_differential_privacy':
            table_differential_privacy_section = section
        elif section.type_name == 'table_smart_noise':
            table_smart_noise_section = section
    assert table_privacy_section.privacy_column == 'user_id'
    assert table_privacy_section.privacy_level == 1
    assert table_other_section.synth_allowed is True
    assert table_other_section.tau == 99
    assert table_differential_privacy_section.budget_epsilon == 1000
    assert table_differential_privacy_section.budget_delta == 500
    assert table_smart_noise_section.row_privacy is True
    assert table_smart_noise_section.rows == 2000
    assert table_smart_noise_section.max_ids == 1
    assert table_smart_noise_section.sample_max_ids is True
    assert table_smart_noise_section.use_dpsu is True
    assert table_smart_noise_section.clamp_counts is True
    assert table_smart_noise_section.clamp_columns is True
    assert table_smart_noise_section.censor_dims is True
    assert len(metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes) == 5
    column_user_id = None
    column_weight = None
    column_height = None
    column_name = None
    column_email = None
    for column in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes:
        if column.name == 'user_id':
            column_user_id = column
        elif column.name == 'weight':
            column_weight = column
        elif column.name == 'height':
            column_height = column
        elif column.name == 'name':
            column_name = column
        elif column.name == 'email':
            column_email = column
        else:
            raise Exception(f"wrong column found; name: {column.name}")
    assert column_user_id is not None
    assert column_weight is not None
    assert column_height is not None
    assert column_name is not None
    assert column_email is not None
    column_user_id_column_section = None
    column_user_id_column_smart_noise_section = None
    for section in column_user_id.sections:
        if section.type_name == 'column':
            column_user_id_column_section = section
        elif section.type_name == 'column_smart_noise':
            column_user_id_column_smart_noise_section = section
    assert column_user_id_column_section.data_type_name == 'int'
    assert column_user_id_column_smart_noise_section.private_id is True
    column_weight_column_section = None
    column_weight_column_float_section = None
    column_weight_column_smart_noise_section = None
    column_weight_column_smart_noise_float_section = None
    for section in column_weight.sections:
        if section.type_name == 'column':
            column_weight_column_section = section
        elif section.type_name == 'column_float':
            column_weight_column_float_section = section
        elif section.type_name == 'column_smart_noise':
            column_weight_column_smart_noise_section = section
        elif section.type_name == 'column_smart_noise_float':
            column_weight_column_smart_noise_float_section = section
    assert column_weight_column_section.selectable is True
    assert column_weight_column_float_section.synthesizable is True
    assert column_weight_column_float_section.use_auto_bounds is False
    assert column_weight_column_float_section.discrete is False
    assert column_weight_column_smart_noise_section.private_id is False
    assert column_weight_column_smart_noise_float_section.bounded is True
    assert column_weight_column_smart_noise_float_section.lower == 0.0
    assert column_weight_column_smart_noise_float_section.upper == 100.5
    column_height_column_float_section = None
    column_height_column_smart_noise_float_section = None
    for section in column_height.sections:
        if section.type_name == 'column_float':
            column_height_column_float_section = section
        elif section.type_name == 'column_smart_noise_float':
            column_height_column_smart_noise_float_section = section
    assert column_height_column_float_section.synthesizable is False
    assert column_height_column_float_section.use_auto_bounds is True
    assert column_height_column_float_section.auto_bounds_prob == 0.8
    assert column_height_column_float_section.min_step == 0.5
    assert column_height_column_float_section.discrete is True
    assert column_height_column_smart_noise_float_section.bounded is True
    column_name_column_string_section = None
    for section in column_name.sections:
        if section.type_name == 'column_string':
            column_name_column_string_section = section
    assert column_name_column_string_section.synthesizable is True
    column_email_column_section = None
    column_email_column_string_section = None
    for section in column_email.sections:
        if section.type_name == 'column':
            column_email_column_section = section
        elif section.type_name == 'column_string':
            column_email_column_string_section = section
    assert column_email_column_section.data_type_name == 'string'
    assert column_email_column_section.selectable is False
    assert column_email_column_string_section.mask == '(.*)@(.*).{3}$'
    assert column_email_column_string_section.cardinality == 123
    assert column_email_column_string_section.synthesizable is True

    # change metadata
    table_differential_privacy_section.budget_epsilon = 1234
    metadata.root_node.description = "new description"
    metadata.root_node.is_public = False

    # save metadata
    yaml_content = metadata.to_yaml()

    # reload metadata
    metadata = Metadata.from_yaml(yaml_content, MetaVerifier.verifySingleTable)

    # test again
    for section in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].sections:
        if section.type_name == 'table_differential_privacy':
            table_differential_privacy_section = section
    assert table_differential_privacy_section.budget_epsilon == 1234
    assert metadata.root_node.description == "new description"
    assert metadata.root_node.is_public is False

    # change metadata
    table_differential_privacy_section.budget_epsilon = 5678
    metadata.root_node.description = "new description 2"
    metadata.root_node.is_public = None

    # dump metadata
    yaml_content = metadata.to_yaml()

    # reload metadata
    metadata = Metadata.from_yaml(yaml_content, MetaVerifier.verifySingleTable)

    # test again
    for section in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].sections:
        if section.type_name == 'table_differential_privacy':
            table_differential_privacy_section = section
    assert table_differential_privacy_section.budget_epsilon == 5678
    assert metadata.root_node.description == "new description 2"
    assert metadata.root_node.is_public is False

    # test drop columns (drops column 'height')
    def test_filter(node):
        MetaFilter.check(node)
        node = node.copy()
        for section in node.sections if node.sections is not None else []:
            if (section.type_name == MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME or section.type_name == MetaSectionType.TYPE_NAME_COLUMN_FLOAT or section.type_name == MetaSectionType.TYPE_NAME_COLUMN_INT or section.type_name == MetaSectionType.TYPE_NAME_COLUMN_STRING) and not section.synthesizable:
                return None
        if node.child_nodes is not None:
            modified_child_nodes = []
            for child_node in node.child_nodes:
                modified_child_node = test_filter(child_node)
                if modified_child_node is not None:
                    modified_child_nodes.append(modified_child_node)
            node.child_nodes = modified_child_nodes
        return node
    metadata = metadata.filter(test_filter)
    assert len(metadata.root_node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes) == 4

    # test to_dict
    metadata_dct = metadata.to_dict()
    assert metadata_dct['name'] == 'test_ds'
    table_smart_noise_section_dct = None
    for section_dct in metadata_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_smart_noise_section_dct = section_dct
    assert table_smart_noise_section_dct['row_privacy'] is True
    column_weight_dct = None
    for column_dct in metadata_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        if column_dct['name'] == 'weight':
            column_weight_dct = column_dct
    column_weight_column_section_dct = None
    for section_dct in column_weight_dct['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_COLUMN:
            column_weight_column_section_dct = section_dct
    assert column_weight_column_section_dct['selectable'] is True

    # test to_dict sm
    metadata_sm = metadata.filter(MetaFilter.filterSmartNoise)
    metadata_sm_dct = metadata_sm.to_dict()
    table_smart_noise_section_dct = None
    for section_dct in metadata_sm_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_smart_noise_section_dct = section_dct
    assert table_smart_noise_section_dct['row_privacy'] is True
    column_weight_dct = None
    column_email_dct = None
    for column_dct in metadata_sm_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        if column_dct['name'] == 'weight':
            column_weight_dct = column_dct
        if column_dct['name'] == 'email':
            column_email_dct = column_dct
    column_weight_column_section_dct = None
    column_weight_column_smart_noise_float_section_dct = None
    for section_dct in column_weight_dct['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_COLUMN:
            column_weight_column_section_dct = section_dct
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT:
            column_weight_column_smart_noise_float_section_dct = section_dct
    assert column_weight_column_section_dct is None
    assert column_weight_column_smart_noise_float_section_dct['upper'] == 100.5

    # test to_dict ml
    metadata_ml = metadata.filter(MetaFilter.filterMachineLearning)
    metadata_ml_dct = metadata_ml.to_dict()
    table_smart_noise_section_dct = None
    for section_dct in metadata_ml_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_smart_noise_section_dct = section_dct
    assert table_smart_noise_section_dct is None
    column_weight_dct = None
    for column_dct in metadata_ml_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        if column_dct['name'] == 'weight':
            column_weight_dct = column_dct
    column_weight_column_float_section_dct = None
    for section_dct in column_weight_dct['sections']:
        if section_dct['type_name'] == MetaSectionType.TYPE_NAME_COLUMN_FLOAT:
            column_weight_column_float_section_dct = section_dct
    assert column_weight_column_float_section_dct is None
    assert metadata_ml_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['connector']['sep'] == ','
    assert metadata_ml_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['connector']['decimal'] == '.'
    assert metadata_ml_dct['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['connector']['na_values'] == {'weight': '?', 'height': '??'}

    # clean up
    os.remove('test.yaml')


def test_combine_metadata():
    # prepare yaml file
    content1 = '''type_name: 'dataset'
name: 'test_ds'
description: 'some description'
child_nodes:
    -
        type_name: 'database'
        name: 'test_db_1'
        child_nodes:
            -
                type_name: 'schema'
                name: 'test_sch'
                child_nodes:
                    -
                        type_name: 'table'
                        name: 'test_tab_1'
                        connector:
                            type_name: 'csv'
                            uri: 'user1@db'
                        sections:
                            -
                                type_name: 'table_differential_privacy'
                                budget_epsilon: 1000
                            -
                                type_name: 'table_smart_noise'
                                row_privacy: true
                                rows: 1000
                            -
                                type_name: 'table_other'
                                synth_allowed: true
                            -
                                type_name: 'table_privacy'
                                privacy_level: 1
                        child_nodes:
                            -
                                type_name: 'column'
                                name: 'user_id'
                                sections:
                                    -
                                        type_name: 'column'
                                        data_type_name: 'int'
                                    -
                                        type_name: 'column_smart_noise'
                                        private_id: true
'''

    content2 = '''type_name: 'dataset'
name: 'test_ds'
description: 'some description'
child_nodes:
    -
        type_name: 'database'
        name: 'test_db_2'
        child_nodes:
            -
                type_name: 'schema'
                name: 'test_sch'
                child_nodes:
                    -
                        type_name: 'table'
                        name: 'test_tab_2'
                        connector:
                            type_name: 'csv'
                            uri: 'user2@db'
                        sections:
                            -
                                type_name: 'table_differential_privacy'
                                budget_epsilon: 1001
                            -
                                type_name: 'table_smart_noise'
                                row_privacy: false
                                rows: 2000
                            -
                                type_name: 'table_other'
                                synth_allowed: true
                            -
                                type_name: 'table_privacy'
                                privacy_level: 1
                        child_nodes:
                            -
                                type_name: 'column'
                                name: 'email'
                                sections:
                                    -
                                        type_name: 'column'
                                        data_type_name: 'string'
                                    -
                                        type_name: 'column_smart_noise'
                                        private_id: true
'''

    content3 = '''type_name: 'dataset'
name: 'test_ds'
description: 'some description'
child_nodes:
    -
        type_name: 'database'
        name: 'test_db_1'
        child_nodes:
            -
                type_name: 'schema'
                name: 'test_sch'
                child_nodes:
                    -
                        type_name: 'table'
                        name: 'test_tab_3'
                        connector:
                            type_name: 'csv'
                            uri: 'user3@db'
                        sections:
                            -
                                type_name: 'table_differential_privacy'
                                budget_epsilon: 1000
                            -
                                type_name: 'table_smart_noise'
                                row_privacy: false
                                rows: 3000
                            -
                                type_name: 'table_other'
                                synth_allowed: true
                            -
                                type_name: 'table_privacy'
                                privacy_level: 1
                        child_nodes:
                            -
                                type_name: 'column'
                                name: 'weight'
                                sections:
                                    -
                                        type_name: 'column'
                                        data_type_name: 'int'
'''

    # load metadata
    metadata1 = Metadata.from_yaml(content1, MetaVerifier.verifySingleTable)
    metadata2 = Metadata.from_yaml(content2, MetaVerifier.verifySingleTable)
    metadata3 = Metadata.from_yaml(content3, MetaVerifier.verifySingleTable)

    metadata_merged_a = metadata1.merge_with(metadata2)
    metadata_merged_b = metadata_merged_a.merge_with(metadata3)

    database_1 = None
    database_2 = None
    for database in metadata_merged_b.root_node.child_nodes:
        if database.name == 'test_db_1':
            database_1 = database
        elif database.name == 'test_db_2':
            database_2 = database
    table_1 = None
    table_3 = None
    for table in database_1.child_nodes[0].child_nodes:
        if table.name == 'test_tab_1':
            table_1 = table
        elif table.name == 'test_tab_3':
            table_3 = table
    table_2 = database_2.child_nodes[0].child_nodes[0]
    assert table_1.connector.uri == 'user1@db'
    table_1_smart_noise_section = None
    for section in table_1.sections:
        if section.type_name == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_1_smart_noise_section = section
    assert table_1_smart_noise_section.row_privacy is True
    table_2_smart_noise_section = None
    table_2_differential_privacy_section = None
    for section in table_2.sections:
        if section.type_name == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_2_smart_noise_section = section
        elif section.type_name == MetaSectionType.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY:
            table_2_differential_privacy_section = section
    assert table_2_smart_noise_section.rows == 2000
    assert table_2_differential_privacy_section.budget_epsilon == 1001
    table_3_smart_noise_section = None
    for section in table_3.sections:
        if section.type_name == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            table_3_smart_noise_section = section
    assert table_3_smart_noise_section.row_privacy is False
    table_2_column_email = None
    for column in table_2.child_nodes:
        if column.name == 'email':
            table_2_column_email = column
    table_2_column_email_column_section = None
    for section in table_2_column_email.sections:
        if section.type_name == MetaSectionType.TYPE_NAME_COLUMN:
            table_2_column_email_column_section = section
    assert table_2_column_email_column_section.data_type_name == 'string'
 