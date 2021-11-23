from dq0.sdk.data.metadata.default.default import Default
from dq0.sdk.data.metadata.default.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.metadata import Metadata


def show_metadata_print():
    # prepare yaml file
    content = '''metadata_format_type: 'full'
metadata_format_version: 2021112301
metadata_node:
  type_name: 'dataset'
  attributes:
  - type_name: 'string'
    key: 'name'
    value: 'test_ds'
  - type_name: 'string'
    key: 'description'
    value: "some description"
  - type_name: 'list'
    key: 'tags'
    value:
    - type_name: 'string'
      value: 'tag1'
    - type_name: 'string'
      value: 'tag2'
  - type_name: 'boolean'
    key: 'metadata_is_public'
    value: true
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
          - type_name: 'string'
            key: 'type_name'
            value: 'csv'
          - type_name: 'string'
            key: 'uri'
            value: 'user@db'
          - type_name: 'boolean'
            key: 'use_original_header'
            value: true
          - type_name: 'list'
            key: 'header_row'
            value:
            - type_name: 'int'
              value: 1
            - type_name: 'int'
              value: 2
          - type_name: 'list'
            key: 'na_values'
            value:
            - type_name: 'string'
              key: 'weight'
              value: '?'
            - type_name: 'string'
              key: 'height'
              value: '??'
        - type_name: 'int'
          key: 'privacy_level'
          value: 1
        - type_name: 'string'
          key: 'privacy_column'
          value: 'user_id'
        - type_name: 'float'
          key: 'budget_epsilon'
          value: 1000.0
        - type_name: 'float'
          key: 'budget_delta'
          value: 500.0
        - type_name: 'boolean'
          key: 'synth_allowed'
          value: true
        - type_name: 'float'
          key: 'tau'
          value: 99.0
        - type_name: 'boolean'
          key: 'row_privacy'
          value: true
        - type_name: 'int'
          key: 'rows'
          value: 2000
        - type_name: 'int'
          key: 'max_ids'
          value: 1
        - type_name: 'boolean'
          key: 'sample_max_ids'
          value: true
        - type_name: 'boolean'
          key: 'use_dpsu'
          value: true
        - type_name: 'boolean'
          key: 'clamp_counts'
          value: true
        - type_name: 'boolean'
          key: 'clamp_columns'
          value: true
        - type_name: 'boolean'
          key: 'censor_dims'
          value: true
        child_nodes:
        - type_name: 'column'
          attributes:
          - type_name: 'string'
            key: 'name'
            value: 'user_id'
          - type_name: 'list'
            key: 'data'
            value:
            - type_name: 'string'
              key: 'data_type_name'
              value: 'int'
          - type_name: 'boolean'
            key: 'private_id'
            value: true
        - type_name: 'column'
          attributes:
          - type_name: 'string'
            key: 'name'
            value: 'weight'
          - type_name: 'string'
            key: 'data_type_name'
            value: 'float'
          - type_name: 'boolean'
            key: 'selectable'
            value: true
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
          - type_name: 'string'
            key: 'name'
            value: 'height'
          - type_name: 'string'
            key: 'data_type_name'
            value: 'float'
          - type_name: 'boolean'
            key: 'bounded'
            value: true
          - type_name: 'boolean'
            key: 'use_auto_bounds'
            value: true
          - type_name: 'float'
            key: 'auto_bounds_prob'
            value: 0.8
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
          - type_name: 'string'
            key: 'name'
            value: 'name'
          - type_name: 'string'
            key: 'data_type_name'
            value: 'string'
          - type_name: 'boolean'
            key: 'synthesizable'
            value: true
        - type_name: 'column'
          attributes:
          - type_name: 'string'
            key: 'name'
            value: 'email'
          - type_name: 'string'
            key: 'data_type_name'
            value: 'string'
          - type_name: 'string'
            key: 'mask'
            value: '(.*)@(.*).{3}$'
          - type_name: 'int'
            key: 'cardinality'
            value: 123
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

    # print original content
    print("\n\n+==========+==========+==========+==========+==========+==========+==========+==========+==========+\n\nORIGINAL CONTENT:\n\n+----------+\n\n")

    print(content)

    # load metadata
    metadata, default = Metadata.from_yaml(yaml_content=content, role_uuids=role_uuids)

    print("\n\n+==========+==========+==========+==========+==========+==========+==========+==========+==========+\n\nTO_YAML():\n\n+----------+\n\n")

    # print metadata to_yaml function
    print(metadata.to_yaml(request_uuids=owner_uuids))

    print("\n\n+==========+==========+==========+==========+==========+==========+==========+==========+==========+\n\nSTR():\n\n+----------+\n\n")

    # print metadata str function
    print(metadata.__str__(request_uuids=owner_uuids))

    print("\n\n+==========+==========+==========+==========+==========+==========+==========+==========+==========+\n\nREPR():\n\n+----------+\n\n")

    # print metadata repr function
    print(repr(metadata))

    print("\n\n+==========+==========+==========+==========+==========+==========+==========+==========+==========+\n\n")


if __name__ == "__main__":
    show_metadata_print()
