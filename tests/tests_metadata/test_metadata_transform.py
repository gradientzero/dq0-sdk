# the unused imports are needed for the eval in the repr test
from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean  # noqa: F401
from dq0.sdk.data.metadata.attribute.attribute_datetime import AttributeDatetime  # noqa: F401
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat  # noqa: F401
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt  # noqa: F401
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList  # noqa: F401
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString  # noqa: F401
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.node.node import Node  # noqa: F401
from dq0.sdk.data.metadata.permissions.permissions import Permissions  # noqa: F401
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


def test_metadata_transform():
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

    # load metadata
    metadata = Metadata.from_yaml(yaml_content=content, role_uuids=role_uuids)

    # test to_yaml
    metadata2 = Metadata.from_yaml(yaml_content=metadata.to_yaml(request_uuids=owner_uuids), role_uuids=role_uuids)
    assert repr(metadata) == repr(metadata2)

    # test str
    metadata3 = Metadata.from_yaml(yaml_content=metadata.__str__(request_uuids=owner_uuids), role_uuids=role_uuids)
    assert repr(metadata) == repr(metadata3)

    # test repr
    assert repr(metadata) == repr(eval(repr(metadata)))
