import os

from dq0.sdk.data.metadata.filter.filter_machine_learning import FilterMachineLearning
from dq0.sdk.data.metadata.filter.filter_smart_noise import FilterSmartNoise
from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


def test_metadata():
    # prepare yaml file
    content = '''meta_dataset:
  format: 'full'
  node:
    type_name: 'dataset'
    attributes:
    - type_name: 'list'
      key: 'data'
      value:
      - type_name: 'string'
        key: 'description'
        value: "some description"
      - type_name: 'boolean'
        key: 'metadata_is_public'
        value: true
      - type_name: 'string'
        key: 'name'
        value: 'test_ds'
      - type_name: 'list'
        key: 'tags'
        value:
        - type_name: 'string'
          value: 'tag1'
        - type_name: 'string'
          value: 'tag2'
    child_nodes:
    - type_name: 'database'
      attributes:
      - type_name: 'list'
        key: 'connector'
        value:
        - type_name: 'list'
          key: 'header_columns'
          value:
          - type_name: 'string'
            value: 'weight'
          - type_name: 'string'
            value: 'height'
        - type_name: 'int'
          key: 'header_row'
          value: 0
        - type_name: 'list'
          key: 'na_values'
          value:
          - type_name: 'string'
            key: 'weight'
            value: '?'
          - type_name: 'string'
            key: 'height'
            value: '??'
        - type_name: 'string'
          key: 'type_name'
          value: 'csv'
        - type_name: 'string'
          key: 'uri'
          value: 'user@db'
        - type_name: 'boolean'
          key: 'use_original_header'
          value: false
      - type_name: 'list'
        key: 'data'
        value:
        - type_name: 'string'
          key: 'name'
          value: 'test_db'
      child_nodes:
      - type_name: 'schema'
        attributes:
        - type_name: 'list'
          key: 'data'
          value:
          - type_name: 'string'
            key: 'name'
            value: 'test_sc'
        child_nodes:
        - type_name: 'table'
          attributes:
          - type_name: 'list'
            key: 'data'
            value:
            - type_name: 'string'
              key: 'name'
              value: 'test_tb'
            - type_name: 'int'
              key: 'rows'
              value: 2000
          - type_name: 'list'
            key: 'differential_privacy'
            value:
            - type_name: 'float'
              key: 'budget_delta'
              value: 500.0
            - type_name: 'float'
              key: 'budget_epsilon'
              value: 1000.0
            - type_name: 'string'
              key: 'privacy_column'
              value: 'user_id'
            - type_name: 'int'
              key: 'privacy_level'
              value: 1
          - type_name: 'list'
            key: 'private_sql'
            value:
            - type_name: 'boolean'
              key: 'censor_dims'
              value: true
            - type_name: 'boolean'
              key: 'clamp_columns'
              value: true
            - type_name: 'boolean'
              key: 'clamp_counts'
              value: true
            - type_name: 'int'
              key: 'max_ids'
              value: 1
            - type_name: 'boolean'
              key: 'row_privacy'
              value: true
            - type_name: 'boolean'
              key: 'sample_max_ids'
              value: true
            - type_name: 'float'
              key: 'tau'
              value: 99.0
            - type_name: 'boolean'
              key: 'use_dpsu'
              value: true
          - type_name: 'list'
            key: 'private_synthesis'
            value:
            - type_name: 'boolean'
              key: 'synth_allowed'
              value: true
          child_nodes:
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'int'
              - type_name: 'string'
                key: 'name'
                value: 'user_id'
            - type_name: 'list'
              key: 'private_sql'
              value:
              - type_name: 'boolean'
                key: 'private_id'
                value: true
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'float'
              - type_name: 'string'
                key: 'name'
                value: 'weight'
              - type_name: 'boolean'
                key: 'selectable'
                value: true
            - type_name: 'list'
              key: 'private_sql_and_synthesis'
              value:
              - type_name: 'boolean'
                key: 'bounded'
                value: true
              - type_name: 'float'
                key: 'lower'
                value: 0.0
              - type_name: 'float'
                key: 'upper'
                value: 100.5
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'float'
              - type_name: 'string'
                key: 'name'
                value: 'height'
            - type_name: 'list'
              key: 'private_sql'
              value:
              - type_name: 'float'
                key: 'auto_bounds_prob'
                value: 0.8
              - type_name: 'boolean'
                key: 'use_auto_bounds'
                value: true
            - type_name: 'list'
              key: 'private_synthesis'
              value:
              - type_name: 'boolean'
                key: 'discrete'
                value: true
              - type_name: 'float'
                key: 'min_step'
                value: 0.5
              - type_name: 'boolean'
                key: 'synthesizable'
                value: false
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'string'
              - type_name: 'string'
                key: 'name'
                value: 'name'
            - type_name: 'list'
              key: 'private_synthesis'
              value:
              - type_name: 'boolean'
                key: 'synthesizable'
                value: true
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'string'
              - type_name: 'string'
                key: 'name'
                value: 'email'
            - type_name: 'list'
              key: 'private_sql'
              value:
              - type_name: 'string'
                key: 'mask'
                value: '(.*)@(.*).{3}$'
            - type_name: 'list'
              key: 'private_sql_and_synthesis'
              value:
              - type_name: 'int'
                key: 'cardinality'
                value: 123
  specification: 'dataset_v1'
'''
    user_user_uuid = '2dfe2aa3-7563-4cd5-9bbe-1b82add081fe'
    user_role_uuid = '2fd590a0-3e97-4230-bb40-3a5d6847f769'
    owner_user_uuid = '9556e5f9-e419-45c9-ada4-4339c7937e1d'
    owner_role_uuid = 'a4a231c0-f759-4d28-ad91-227c96d9408b'
    owner_uuids = {owner_role_uuid, owner_user_uuid}
    user_uuids = {user_role_uuid, user_user_uuid}
    role_uuids = {
        DefaultPermissions.OWNER_NAME: owner_uuids,
        DefaultPermissions.USER_NAME: user_uuids,
    }

    with open('test.yaml', 'w') as f:
        f.write(content)

    # load metadata and initialize interface
    metadata, specifications = Metadata.from_yaml_file(filename='test.yaml', role_uuids=role_uuids)
    m_interface = Interface(metadata=metadata, role_uuids=role_uuids, dataset_specification=specifications['dataset'])

    # test
    m_dataset = m_interface.dataset()
    assert m_dataset.name == 'test_ds'
    m_ds_data = m_dataset.data
    assert m_ds_data.description == "some description"
    assert 'tag1' in m_ds_data.tags
    assert 'tag2' in m_ds_data.tags
    assert m_ds_data.metadata_is_public
    m_database = m_dataset.database()
    m_db_connector = m_database.connector
    assert m_db_connector is not None
    assert m_db_connector.decimal is None
    assert 'weight' in m_db_connector.header_columns
    assert 'height' in m_db_connector.header_columns
    assert m_db_connector.header_row is not None
    assert not m_db_connector.header_row
    assert m_db_connector.index_col is None
    assert m_db_connector.na_values['weight'] == '?'
    assert m_db_connector.na_values['height'] == '??'
    assert m_db_connector.sep is None
    assert m_db_connector.skipinitialspace is None
    assert m_db_connector.type_name == 'csv'
    m_table = m_database.schema().table()
    assert m_table.data.rows == 2000
    m_tb_differential_privacy = m_table.differential_privacy
    assert m_tb_differential_privacy.budget_delta == 500.0
    assert m_tb_differential_privacy.budget_epsilon == 1000.0
    assert m_tb_differential_privacy.privacy_column == 'user_id'
    assert m_tb_differential_privacy.privacy_level == 1
    m_tb_private_sql = m_table.private_sql
    assert m_tb_private_sql.censor_dims
    assert m_tb_private_sql.clamp_columns
    assert m_tb_private_sql.clamp_counts
    assert m_tb_private_sql.max_ids == 1
    assert m_tb_private_sql.row_privacy
    assert m_tb_private_sql.sample_max_ids
    assert m_tb_private_sql.tau == 99.0
    assert m_tb_private_sql.use_dpsu
    assert m_table.private_synthesis.synth_allowed
    assert len(m_table.column_names()) == 5
    m_col_user_id = m_table.column(name='user_id')
    assert m_col_user_id.data.data_type_name == 'int'
    assert m_col_user_id.data.name == 'user_id'
    assert m_col_user_id.private_sql.private_id
    m_col_weight = m_table.column(name='weight')
    assert m_col_weight.data.name == 'weight'
    assert m_col_weight.data.selectable
    assert m_col_weight.private_sql.is_empty()
    assert m_col_weight.private_sql_and_synthesis.bounded
    assert m_col_weight.private_sql_and_synthesis.lower == 0.0
    assert m_col_weight.private_sql_and_synthesis.upper == 100.5
    assert m_col_weight.private_synthesis.is_empty()
    m_col_height = m_table.column(name='height')
    assert m_col_height.data.name == 'height'
    assert m_col_height.private_sql.auto_bounds_prob == 0.8
    assert m_col_height.private_sql.use_auto_bounds
    assert m_col_height.private_synthesis.discrete
    assert m_col_height.private_synthesis.min_step == 0.5
    assert m_col_height.private_synthesis.synthesizable is not None
    assert not m_col_height.private_synthesis.synthesizable
    m_col_name = m_table.column(name='name')
    assert m_col_name.data.name == 'name'
    assert m_col_name.private_synthesis.synthesizable
    m_col_email = m_table.column(name='email')
    assert m_col_email.data.data_type_name == 'string'
    assert m_col_email.data.name == 'email'
    assert m_col_email.data.selectable is None
    assert m_col_email.private_sql.mask == '(.*)@(.*).{3}$'
    assert m_col_email.private_sql_and_synthesis.cardinality == 123
    assert m_col_email.private_synthesis.is_empty()

    # change metadata
    m_ds_data.description = "new description"
    m_ds_data.metadata_is_public = False
    m_tb_differential_privacy.budget_epsilon = 1234.0

    # save and reload metadata
    yaml_content = metadata.to_yaml(request_uuids=owner_uuids)
    metadata, specifications = Metadata.from_yaml(yaml_content=yaml_content, role_uuids=role_uuids)
    m_interface = Interface(metadata=metadata, role_uuids=role_uuids, dataset_specification=specifications['dataset'])

    # test again
    m_dataset = m_interface.dataset()
    assert m_dataset.data.description == "new description"
    assert m_dataset.data.metadata_is_public is not None
    assert not m_dataset.data.metadata_is_public
    assert m_dataset.database().schema().table().differential_privacy.budget_epsilon == 1234.0

    # change metadata
    m_dataset.data.description = "new description 2"
    del m_dataset.data.metadata_is_public
    m_dataset.database().schema().table().differential_privacy.budget_epsilon = 5678.0

    # save and reload metadata
    yaml_content = metadata.to_yaml(request_uuids=owner_uuids)
    metadata, specifications = Metadata.from_yaml(yaml_content=yaml_content, role_uuids=role_uuids)
    m_interface = Interface(metadata=metadata, role_uuids=role_uuids, dataset_specification=specifications['dataset'])

    # test again
    m_dataset = m_interface.dataset()
    assert m_dataset.data.description == "new description 2"
    assert m_dataset.data.metadata_is_public is None
    assert m_dataset.database().schema().table().differential_privacy.budget_epsilon == 5678.0

    # test drop columns (drops column 'height')
    m_dataset.database().schema().table().drop_columns(attributes_map={'private_synthesis': {'synthesizable': False}})
    assert len(m_dataset.database().schema().table().column_names()) == 4

    # test to_dict
    metadata_dct = metadata.to_dict(request_uuids=owner_uuids)
    attribute_name_dct = None
    for attribute_dct in metadata_dct['meta_dataset']['node']['attributes']:
        if attribute_dct['key'] == 'data':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'name':
                    attribute_name_dct = sub_attribute_dct
                    break
            break
    assert attribute_name_dct['value'] == 'test_ds'
    attribute_row_privacy_dct = None
    for attribute_dct in metadata_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'private_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'row_privacy':
                    attribute_row_privacy_dct = sub_attribute_dct
                    break
            break
    assert attribute_row_privacy_dct['value'] is True
    column_weight_dct = None
    for column_dct in metadata_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        for attribute_dct in column_dct['attributes']:
            if attribute_dct['key'] == 'data':
                for sub_attribute_dct in attribute_dct['value']:
                    if sub_attribute_dct['key'] == 'name' and sub_attribute_dct['value'] == 'weight':
                        column_weight_dct = column_dct
                        break
                break
    attribute_selectable_dct = None
    for attribute_dct in column_weight_dct['attributes']:
        if attribute_dct['key'] == 'data':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'selectable':
                    attribute_selectable_dct = sub_attribute_dct
                    break
            break
    assert attribute_selectable_dct['value'] is True

    # test to_dict sm
    metadata_sm = metadata.filter(dataset_filter_func=FilterSmartNoise.filter)
    print(metadata_sm.__str__(request_uuids=owner_uuids))
    metadata_sm_dct = metadata_sm.to_dict(request_uuids=owner_uuids)
    attribute_row_privacy_dct = None
    for attribute_dct in metadata_sm_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'private_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'row_privacy':
                    attribute_row_privacy_dct = sub_attribute_dct
                    break
    assert attribute_row_privacy_dct['value'] is True
    column_weight_dct = None
    column_email_dct = None
    for column_dct in metadata_sm_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        for attribute_dct in column_dct['attributes']:
            if attribute_dct['key'] == 'data':
                for sub_attribute_dct in attribute_dct['value']:
                    if sub_attribute_dct['key'] == 'name' and sub_attribute_dct['value'] == 'weight':
                        column_weight_dct = column_dct
                    if sub_attribute_dct['key'] == 'name' and sub_attribute_dct['value'] == 'email':
                        column_email_dct = column_dct
            break
    attribute_selectable_dct = None
    attribute_upper_dct = None
    for attribute_dct in column_weight_dct['attributes']:
        if attribute_dct['key'] == 'data':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'selectable':
                    attribute_selectable_dct = sub_attribute_dct
                    break
        if attribute_dct['key'] == 'private_sql_and_synthesis':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'upper':
                    attribute_upper_dct = sub_attribute_dct
                    break
    assert attribute_selectable_dct is None
    assert attribute_upper_dct['value'] == 100.5
    attribute_cardinality_dct = None
    for attribute_dct in column_email_dct['attributes']:
        if attribute_dct['key'] == 'private_sql_and_synthesis':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'cardinality':
                    attribute_cardinality_dct = sub_attribute_dct
                    break
    assert attribute_cardinality_dct['value'] == 123

    # test to_dict ml
    metadata_ml = metadata.filter(dataset_filter_func=FilterMachineLearning.filter)
    print(metadata_ml.__str__(request_uuids=owner_uuids))
    metadata_ml_dct = metadata_ml.to_dict(request_uuids=owner_uuids)
    attribute_sample_max_ids_dct = None
    for attribute_dct in metadata_ml_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'private_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'sample_max_ids':
                    attribute_sample_max_ids_dct = sub_attribute_dct
                    break
            break
    assert attribute_sample_max_ids_dct is None
    column_weight_dct = None
    for column_dct in metadata_ml_dct['meta_dataset']['node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
        for attribute_dct in column_dct['attributes']:
            if attribute_dct['key'] == 'data':
                for sub_attribute_dct in attribute_dct['value']:
                    if sub_attribute_dct['key'] == 'name' and sub_attribute_dct['value'] == 'weight':
                        column_weight_dct = column_dct
                        break
                break
    attribute_synthesizable_dct = None
    assert column_weight_dct is not None
    assert 'attributes' in column_weight_dct
    for attribute_dct in column_weight_dct['attributes']:
        if attribute_dct['key'] == 'private_synthesis':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'synthesizable':
                    attribute_synthesizable_dct = sub_attribute_dct
                    break
            break
    assert attribute_synthesizable_dct is None
    attribute_connector_dct = None
    for attribute_dct in metadata_ml_dct['meta_dataset']['node']['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'connector':
            attribute_connector_dct = attribute_dct
            break
    attribute_sep_dct = None
    attribute_decimal_dct = None
    attribute_na_values_dct = None
    for attribute_dct in attribute_connector_dct['value']:
        if attribute_dct['key'] == 'sep':
            attribute_sep_dct = attribute_dct
        if attribute_dct['key'] == 'decimal':
            attribute_decimal_dct = attribute_dct
        if attribute_dct['key'] == 'na_values':
            attribute_na_values_dct = attribute_dct
    assert attribute_sep_dct is None
    assert attribute_decimal_dct is None
    attribute_na_value_weight_dct = None
    attribute_na_value_height_dct = None
    for attribute_dct in attribute_na_values_dct['value']:
        if attribute_dct['key'] == 'weight':
            attribute_na_value_weight_dct = attribute_dct
        if attribute_dct['key'] == 'height':
            attribute_na_value_height_dct = attribute_dct
    assert attribute_na_value_weight_dct['value'] == '?'
    assert attribute_na_value_height_dct['value'] == '??'

    # clean up
    os.remove('test.yaml')


def test_combine_metadata():
    # prepare yaml file
    content1 = '''meta_dataset:
  format: 'full'
  node:
    type_name: 'dataset'
    attributes:
    - type_name: 'list'
      key: 'data'
      value:
      - type_name: 'string'
        key: 'description'
        value: "some description"
      - type_name: 'string'
        key: 'name'
        value: 'test_ds'
    child_nodes:
    - type_name: 'database'
      attributes:
      - type_name: 'list'
        key: 'connector'
        value:
        - type_name: 'string'
          key: 'type_name'
          value: 'csv'
        - type_name: 'string'
          key: 'uri'
          value: 'user1@db'
      - type_name: 'list'
        key: 'data'
        value:
        - type_name: 'string'
          key: 'name'
          value: 'test_db_1'
      child_nodes:
      - type_name: 'schema'
        attributes:
        - type_name: 'list'
          key: 'data'
          value:
          - type_name: 'string'
            key: 'name'
            value: 'test_sc'
        child_nodes:
        - type_name: 'table'
          attributes:
          - type_name: 'list'
            key: 'data'
            value:
            - type_name: 'string'
              key: 'name'
              value: 'test_tab_1'
            - type_name: 'int'
              key: 'rows'
              value: 1000
          - type_name: 'list'
            key: 'differential_privacy'
            value:
            - type_name: 'float'
              key: 'budget_epsilon'
              value: 1000.0
            - type_name: 'int'
              key: 'privacy_level'
              value: 1
          - type_name: 'list'
            key: 'private_sql'
            value:
            - type_name: 'boolean'
              key: 'row_privacy'
              value: true
          - type_name: 'list'
            key: 'private_synthesis'
            value:
            - type_name: 'boolean'
              key: 'synth_allowed'
              value: true
          child_nodes:
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'int'
              - type_name: 'string'
                key: 'name'
                value: 'user_id'
            - type_name: 'list'
              key: 'private_sql'
              value:
              - type_name: 'boolean'
                key: 'private_id'
                value: true
  specification: 'dataset_v1'
'''
    content2 = '''meta_dataset:
  format: 'full'
  node:
    type_name: 'dataset'
    attributes:
    - type_name: 'list'
      key: 'data'
      value:
      - type_name: 'string'
        key: 'description'
        value: "some description"
      - type_name: 'string'
        key: 'name'
        value: 'test_ds'
    child_nodes:
    - type_name: 'database'
      attributes:
      - type_name: 'list'
        key: 'connector'
        value:
        - type_name: 'string'
          key: 'type_name'
          value: 'csv'
        - type_name: 'string'
          key: 'uri'
          value: 'user2@db'
      - type_name: 'list'
        key: 'data'
        value:
        - type_name: 'string'
          key: 'name'
          value: 'test_db_2'
      child_nodes:
      - type_name: 'schema'
        attributes:
        - type_name: 'list'
          key: 'data'
          value:
          - type_name: 'string'
            key: 'name'
            value: 'test_sc'
        child_nodes:
        - type_name: 'table'
          attributes:
          - type_name: 'list'
            key: 'data'
            value:
            - type_name: 'string'
              key: 'name'
              value: 'test_tab_2'
            - type_name: 'int'
              key: 'rows'
              value: 2000
          - type_name: 'list'
            key: 'differential_privacy'
            value:
            - type_name: 'float'
              key: 'budget_epsilon'
              value: 1001.0
            - type_name: 'int'
              key: 'privacy_level'
              value: 1
          - type_name: 'list'
            key: 'private_sql'
            value:
            - type_name: 'boolean'
              key: 'row_privacy'
              value: false
          - type_name: 'list'
            key: 'private_synthesis'
            value:
            - type_name: 'boolean'
              key: 'synth_allowed'
              value: true
          child_nodes:
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'string'
              - type_name: 'string'
                key: 'name'
                value: 'email'
            - type_name: 'list'
              key: 'private_sql'
              value:
              - type_name: 'boolean'
                key: 'private_id'
                value: true
  specification: 'dataset_v1'
'''
    content3 = '''meta_dataset:
  format: 'full'
  node:
    type_name: 'dataset'
    attributes:
    - type_name: 'list'
      key: 'data'
      value:
      - type_name: 'string'
        key: 'description'
        value: "some description"
      - type_name: 'string'
        key: 'name'
        value: 'test_ds'
    child_nodes:
    - type_name: 'database'
      attributes:
      - type_name: 'list'
        key: 'connector'
        value:
        - type_name: 'string'
          key: 'type_name'
          value: 'csv'
        - type_name: 'string'
          key: 'uri'
          value: 'user1@db'
      - type_name: 'list'
        key: 'data'
        value:
        - type_name: 'string'
          key: 'name'
          value: 'test_db_1'
      child_nodes:
      - type_name: 'schema'
        attributes:
        - type_name: 'list'
          key: 'data'
          value:
          - type_name: 'string'
            key: 'name'
            value: 'test_sc'
        child_nodes:
        - type_name: 'table'
          attributes:
          - type_name: 'list'
            key: 'data'
            value:
            - type_name: 'string'
              key: 'name'
              value: 'test_tab_3'
            - type_name: 'int'
              key: 'rows'
              value: 3000
          - type_name: 'list'
            key: 'differential_privacy'
            value:
            - type_name: 'float'
              key: 'budget_epsilon'
              value: 1000.0
            - type_name: 'int'
              key: 'privacy_level'
              value: 1
          - type_name: 'list'
            key: 'private_sql'
            value:
            - type_name: 'boolean'
              key: 'row_privacy'
              value: false
          - type_name: 'list'
            key: 'private_synthesis'
            value:
            - type_name: 'boolean'
              key: 'synth_allowed'
              value: true
          child_nodes:
          - type_name: 'column'
            attributes:
            - type_name: 'list'
              key: 'data'
              value:
              - type_name: 'string'
                key: 'data_type_name'
                value: 'int'
              - type_name: 'string'
                key: 'name'
                value: 'weight'
  specification: 'dataset_v1'
'''
    user_user_uuid = '2dfe2aa3-7563-4cd5-9bbe-1b82add081fe'
    user_role_uuid = '2fd590a0-3e97-4230-bb40-3a5d6847f769'
    owner_user_uuid = '9556e5f9-e419-45c9-ada4-4339c7937e1d'
    owner_role_uuid = 'a4a231c0-f759-4d28-ad91-227c96d9408b'
    owner_uuids = {owner_role_uuid, owner_user_uuid}
    user_uuids = {user_role_uuid, user_user_uuid}
    role_uuids = {
        DefaultPermissions.OWNER_NAME: owner_uuids,
        DefaultPermissions.USER_NAME: user_uuids,
    }

    # load metadata
    metadata1, specifications = Metadata.from_yaml(yaml_content=content1, role_uuids=role_uuids)
    metadata2, _ = Metadata.from_yaml(yaml_content=content2, role_uuids=role_uuids)
    metadata3, _ = Metadata.from_yaml(yaml_content=content3, role_uuids=role_uuids)

    dataset_specification = specifications['dataset'] if 'dataset' in specifications else None
    metadata_merged_a = metadata1.merge_with(other=metadata2, overwrite_value=False, overwrite_permissions=False, request_uuids=owner_uuids,
                                             dataset_specification=dataset_specification)
    metadata_merged_b = metadata_merged_a.merge_with(other=metadata3, overwrite_value=False, overwrite_permissions=False, request_uuids=owner_uuids,
                                                     dataset_specification=dataset_specification)
    m_interface = Interface(metadata=metadata_merged_b, role_uuids=role_uuids, dataset_specification=dataset_specification)
    m_dataset = m_interface.dataset()
    assert m_dataset.database(name='test_db_1').connector.uri == 'user1@db'
    m_db_1_sc = m_dataset.database(name='test_db_1').schema()
    assert m_db_1_sc.table(name='test_tab_1').private_sql.row_privacy
    assert m_db_1_sc.table(name='test_tab_3').private_sql.row_privacy is not None
    assert not m_db_1_sc.table(name='test_tab_3').private_sql.row_privacy
    m_db_2_tb_2 = m_dataset.database(name='test_db_2').schema().table(name='test_tab_2')
    assert m_db_2_tb_2.data.rows == 2000
    assert m_db_2_tb_2.differential_privacy.budget_epsilon == 1001.0
    assert m_db_2_tb_2.column(name='email').data.data_type_name == 'string'
