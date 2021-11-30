import os
from dq0.sdk.data.metadata import default
from dq0.sdk.data.metadata.default.default import Default
from dq0.sdk.data.metadata.default.default_permissions import DefaultPermissions

from dq0.sdk.data.metadata.filter.filter import Filter
from dq0.sdk.data.metadata.filter.filter_machine_learning import FilterMachineLearning
from dq0.sdk.data.metadata.filter.filter_regular import FilterRegular
from dq0.sdk.data.metadata.filter.filter_smart_noise import FilterSmartNoise
from dq0.sdk.data.metadata.metadata import Metadata


def test_metadata():
    # prepare yaml file
    content = '''metadata_default_version: 2021112301
metadata_format_type: 'full'
metadata_node:
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
    child_nodes:
    - type_name: 'schema'
      child_nodes:
      - type_name: 'table'
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
          - type_name: 'boolean'
            key: 'header_row'
            value: false
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
          key: 'data_synthesis'
          value:
          - type_name: 'boolean'
            key: 'synth_allowed'
            value: true
          - type_name: 'float'
            key: 'tau'
            value: 99.0
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
          key: 'differential_privacy_sql'
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
          - type_name: 'int'
            key: 'rows'
            value: 2000
          - type_name: 'boolean'
            key: 'sample_max_ids'
            value: true
          - type_name: 'boolean'
            key: 'use_dpsu'
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
            key: 'differential_privacy_sql'
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
            key: 'differential_privacy'
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
            - type_name: 'boolean'
              key: 'discrete'
              value: true
            - type_name: 'string'
              key: 'name'
              value: 'height'
          - type_name: 'list'
            key: 'data_synthesis'
            value:
            - type_name: 'boolean'
              key: 'synthesizable'
              value: false
          - type_name: 'list'
            key: 'differential_privacy_sql'
            value:
            - type_name: 'float'
              key: 'auto_bounds_prob'
              value: 0.8
            - type_name: 'float'
              key: 'min_step'
              value: 0.5
            - type_name: 'boolean'
              key: 'use_auto_bounds'
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
              value: 'name'
          - type_name: 'list'
            key: 'data_synthesis'
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
            key: 'differential_privacy'
            value:
            - type_name: 'int'
              key: 'cardinality'
              value: 123
          - type_name: 'list'
            key: 'differential_privacy_sql'
            value:
            - type_name: 'string'
              key: 'mask'
              value: '(.*)@(.*).{3}$'
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

    # load metadata
    metadata, default = Metadata.from_yaml_file(filename='test.yaml', role_uuids=role_uuids)

    # test
    assert metadata.node.type_name == 'dataset'
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='test_ds') is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='description', value="some description") is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='tags', value=None).get_attribute(index=0, key=None, value='tag1') is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='tags', value=None).get_attribute(index=1, key=None, value='tag2') is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='metadata_is_public', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].type_name == 'table'
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='decimal', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='header_columns', value=None).get_attribute(index=0, key=None, value='weight') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='header_columns', value=None).get_attribute(index=1, key=None, value='height') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='header_row', value=False) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='index_col', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='na_values', value=None).get_attribute(index=-1, key='weight', value='?') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='na_values', value=None).get_attribute(index=-1, key='height', value='??') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='sep', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='skipinitialspace', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='type_name', value='csv') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='data_synthesis', value=None).get_attribute(index=-1, key='synth_allowed', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='data_synthesis', value=None).get_attribute(index=-1, key='tau', value=99.0) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_delta', value=500.0) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=1000.0) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='privacy_column', value='user_id') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='privacy_level', value=1) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='censor_dims', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='clamp_columns', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='clamp_counts', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='max_ids', value=1) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='row_privacy', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='rows', value=2000.0) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='sample_max_ids', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='use_dpsu', value=True) is not None
    assert len(metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes) == 5
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'user_id'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='data_type_name', value='int') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'user_id'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='user_id') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'user_id'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='private_id', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='discrete', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='weight') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='selectable', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='data_synthesis', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='bounded', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='lower', value=0.0) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='upper', value=100.5) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'weight'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='discrete', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='height') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='data_synthesis', value=None).get_attribute(index=-1, key='synthesizable', value=False) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='differential_privacy', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='auto_bounds_prob', value=0.8) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='min_step', value=0.5) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'height'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='use_auto_bounds', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'name'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='name') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'name'}}).get_attribute(index=-1, key='data_synthesis', value=None).get_attribute(index=-1, key='synthesizable', value=True) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='data_type_name', value='string') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='name', value='email') is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='selectable', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='data_synthesis', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='cardinality', value=123) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='mask', value='(.*)@(.*).{3}$') is not None

    # change metadata
    metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='description', value=None).value = "new description"
    metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='metadata_is_public', value=None).value = False
    metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=None).value = 1234.0

    # save metadata
    yaml_content = metadata.to_yaml(request_uuids=owner_uuids)

    # reload metadata
    metadata, _ = Metadata.from_yaml(yaml_content=yaml_content, role_uuids=role_uuids)

    # test again
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='description', value="new description") is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='metadata_is_public', value=False) is not None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=1234.0) is not None

    # change metadata
    metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='description', value=None).value = "new description 2"
    metadata.node.get_attribute(index=-1, key='data', value=None).remove_attribute(index=-1, key='metadata_is_public', value=None)
    metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=None).value = 5678.0

    # dump metadata
    yaml_content = metadata.to_yaml(request_uuids=owner_uuids)

    # reload metadata
    metadata, _ = Metadata.from_yaml(yaml_content=yaml_content, role_uuids=role_uuids)

    # test again
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='description', value="new description 2") is not None
    assert metadata.node.get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='metadata_is_public', value=None) is None
    assert metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=5678.0) is not None

    # test drop columns (drops column 'height')
    metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].remove_child_node(index=-1, attributes_map={'data_synthesis': {'synthesizable': False}})
    assert len(metadata.node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes) == 4

    # test to_dict
    metadata_dct = metadata.to_dict(request_uuids=owner_uuids)
    attribute_name_dct = None
    for attribute_dct in metadata_dct['metadata_node']['attributes']:
        if attribute_dct['key'] == 'data':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'name':
                    attribute_name_dct = sub_attribute_dct
                    break
            break
    assert attribute_name_dct['value'] == 'test_ds'
    attribute_row_privacy_dct = None
    for attribute_dct in metadata_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'differential_privacy_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'row_privacy':
                    attribute_row_privacy_dct = sub_attribute_dct
                    break
            break
    assert attribute_row_privacy_dct['value'] is True
    column_weight_dct = None
    for column_dct in metadata_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
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
    metadata_sm = metadata.filter(filter_func=FilterSmartNoise.filter, default=None)
    print(metadata_sm.__str__(request_uuids=owner_uuids))
    metadata_sm_dct = metadata_sm.to_dict(request_uuids=owner_uuids)
    attribute_name_dct = None
    for attribute_dct in metadata_sm_dct['metadata_node']['attributes'] if 'attributes' in metadata_sm_dct['metadata_node'] else []:
        if attribute_dct['key'] == 'data':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'name':
                    attribute_name_dct = sub_attribute_dct
                    break
        break
    assert attribute_name_dct is None
    attribute_row_privacy_dct = None
    for attribute_dct in metadata_sm_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'differential_privacy_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'row_privacy':
                    attribute_row_privacy_dct = sub_attribute_dct
                    break
    assert attribute_row_privacy_dct['value'] is True
    column_weight_dct = None
    column_email_dct = None
    for column_dct in metadata_sm_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
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
        if attribute_dct['key'] == 'differential_privacy':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'upper':
                    attribute_upper_dct = sub_attribute_dct
                    break
    assert attribute_selectable_dct is None
    assert attribute_upper_dct['value'] == 100.5
    attribute_cardinality_dct = None
    for attribute_dct in column_email_dct['attributes']:
        if attribute_dct['key'] == 'differential_privacy':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'cardinality':
                    attribute_cardinality_dct = sub_attribute_dct
                    break
    assert attribute_cardinality_dct['value'] == 123

    # test to_dict ml
    metadata_ml = metadata.filter(filter_func=FilterMachineLearning.filter, default=None)
    print(metadata_ml.__str__(request_uuids=owner_uuids))
    metadata_ml_dct = metadata_ml.to_dict(request_uuids=owner_uuids)
    attribute_connector_dct = None
    attribute_sample_max_ids_dct = None
    for attribute_dct in metadata_ml_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['attributes']:
        if attribute_dct['key'] == 'connector':
            attribute_connector_dct = attribute_dct
        if attribute_dct['key'] == 'differential_privacy_sql':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'sample_max_ids':
                    attribute_sample_max_ids_dct = sub_attribute_dct
                    break
    assert attribute_sample_max_ids_dct is None
    column_weight_dct = None
    for column_dct in metadata_ml_dct['metadata_node']['child_nodes'][0]['child_nodes'][0]['child_nodes'][0]['child_nodes']:
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
        if attribute_dct['key'] == 'data_synthesis':
            for sub_attribute_dct in attribute_dct['value']:
                if sub_attribute_dct['key'] == 'synthesizable':
                    attribute_synthesizable_dct = sub_attribute_dct
                    break
            break
    assert attribute_synthesizable_dct is None
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
    content1 = '''metadata_default_version: 2021112301
metadata_format_type: 'full'
metadata_node:
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
      key: 'data'
      value:
      - type_name: 'string'
        key: 'name'
        value: 'test_db_1'
    child_nodes:
    - type_name: 'schema'
      child_nodes:
      - type_name: 'table'
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
            value: 'test_tab_1'
        - type_name: 'list'
          key: 'data_synthesis'
          value:
          - type_name: 'boolean'
            key: 'synth_allowed'
            value: true
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
          key: 'differential_privacy_sql'
          value:
          - type_name: 'boolean'
            key: 'row_privacy'
            value: true
          - type_name: 'int'
            key: 'rows'
            value: 1000
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
            key: 'differential_privacy_sql'
            value:
            - type_name: 'boolean'
              key: 'private_id'
              value: true
'''
    content2 = '''metadata_default_version: 2021112301
metadata_format_type: 'full'
metadata_node:
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
      key: 'data'
      value:
      - type_name: 'string'
        key: 'name'
        value: 'test_db_2'
    child_nodes:
    - type_name: 'schema'
      child_nodes:
      - type_name: 'table'
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
            value: 'test_tab_2'
        - type_name: 'list'
          key: 'data_synthesis'
          value:
          - type_name: 'boolean'
            key: 'synth_allowed'
            value: true
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
          key: 'differential_privacy_sql'
          value:
          - type_name: 'boolean'
            key: 'row_privacy'
            value: false
          - type_name: 'int'
            key: 'rows'
            value: 2000
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
            key: 'differential_privacy_sql'
            value:
            - type_name: 'boolean'
              key: 'private_id'
              value: true
'''
    content3 = '''metadata_default_version: 2021112301
metadata_format_type: 'full'
metadata_node:
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
      key: 'data'
      value:
      - type_name: 'string'
        key: 'name'
        value: 'test_db_1'
    child_nodes:
    - type_name: 'schema'
      child_nodes:
      - type_name: 'table'
        attributes:
        - type_name: 'list'
          key: 'connector'
          value:
          - type_name: 'string'
            key: 'type_name'
            value: 'csv'
          - type_name: 'string'
            key: 'uri'
            value: 'user3@db'
        - type_name: 'list'
          key: 'data'
          value:
          - type_name: 'string'
            key: 'name'
            value: 'test_tab_3'
        - type_name: 'list'
          key: 'data_synthesis'
          value:
          - type_name: 'boolean'
            key: 'synth_allowed'
            value: true
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
          key: 'differential_privacy_sql'
          value:
          - type_name: 'boolean'
            key: 'row_privacy'
            value: false
          - type_name: 'int'
            key: 'rows'
            value: 3000
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
    metadata1, default = Metadata.from_yaml(yaml_content=content1, role_uuids=role_uuids)
    metadata2, _ = Metadata.from_yaml(yaml_content=content2, role_uuids=role_uuids)
    metadata3, _ = Metadata.from_yaml(yaml_content=content3, role_uuids=role_uuids)

    metadata_merged_a = metadata1.merge_with(other=metadata2, overwrite_value=False, overwrite_permissions=False, request_uuids=owner_uuids, default=None)
    metadata_merged_b = metadata_merged_a.merge_with(other=metadata3, overwrite_value=False, overwrite_permissions=False, request_uuids=owner_uuids, default=None)

    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_1'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_1'}}).get_attribute(index=-1, key='connector', value=None).get_attribute(index=-1, key='uri', value='user1@db') is not None
    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_2'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_2'}}).get_attribute(index=-1, key='differential_privacy', value=None).get_attribute(index=-1, key='budget_epsilon', value=1001.0) is not None
    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_1'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_1'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='row_privacy', value=True) is not None
    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_1'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_3'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='row_privacy', value=False) is not None
    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_2'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_2'}}).get_attribute(index=-1, key='differential_privacy_sql', value=None).get_attribute(index=-1, key='rows', value=2000) is not None
    assert metadata_merged_b.node.get_child_node(index=-1, attributes_map={'data': {'name': 'test_db_2'}}).child_nodes[0].get_child_node(index=-1, attributes_map={'data': {'name': 'test_tab_2'}}).get_child_node(index=-1, attributes_map={'data': {'name': 'email'}}).get_attribute(index=-1, key='data', value=None).get_attribute(index=-1, key='data_type_name', value='string') is not None
 