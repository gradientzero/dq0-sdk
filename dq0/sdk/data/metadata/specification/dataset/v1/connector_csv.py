from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json.utils import Utils as JsonUtils


class ConnectorCSV:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        applied_attributes = ConnectorCSV.apply_defaults_to_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_attribute(role_uuids=role_uuids) \
            if attribute.get_permissions() is None else attribute.get_permissions().copy()
        return AttributeList(key=attribute.get_key(), value=applied_attributes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.shared_attribute(role_uuids=role_uuids))
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'connector': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
        })
        ConnectorCSV.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'decimal': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'header_columns': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'header_row': ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_LIST], shared_attribute),
            'index_col': ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_LIST, AttributeType.TYPE_NAME_STRING], shared_attribute),
            'na_values': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'sep': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'skipinitialspace': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'uri': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'use_original_header': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        }, required_keys={'type_name'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].get_value() != 'csv':
            raise Exception(f"csv connector type_name value {type_name_attributes[0].get_value()} does not match 'csv'")
        header_columns_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'header_columns'] \
            if attributes is not None else []
        if 0 < len(header_columns_attributes):
            Attribute.check_list(attribute_list=header_columns_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
        header_row_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'header_row'] if attributes is not None else []
        if 0 < len(header_row_attributes) and header_row_attributes[0].get_type_name() == AttributeType.TYPE_NAME_LIST:
            Attribute.check_list(attribute_list=header_row_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_INT], shared_attribute),
            })
        index_col_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'index_col'] if attributes is not None else []
        if 0 < len(index_col_attributes) and index_col_attributes[0].get_type_name() == AttributeType.TYPE_NAME_LIST:
            Attribute.check_list(attribute_list=index_col_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
            if 0 < len(index_col_attributes[0].get_value()):
                Attribute.check_list(attribute_list=index_col_attributes[0].get_value(), check_data={
                    None: ([index_col_attributes[0].get_value()[0].get_type_name()], shared_attribute),
                })
        na_value_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'na_values'] if attributes is not None else []
        if 0 < len(na_value_attributes):
            Attribute.check_list(attribute_list=na_value_attributes[0].get_value(), check_data=None)
            for tmp_attribute in na_value_attributes[0].get_value():
                if tmp_attribute.get_key() is None:
                    raise Exception("na_values may not have none keys")

    @staticmethod
    def json_schema():
        indent = "          "
        decimal_json_schema = JsonUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_STRING, key='decimal', title='Decimal',
            description="Character to recognize as decimal point when reading the CSV file.").replace('\n', "\n" + indent)
        sep_json_schema = JsonUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_STRING, key='sep', title='Sep',
            description="Delimiter to use when reading the CSV file.").replace('\n', "\n" + indent)
        uri_json_schema = JsonUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_STRING, key='uri', title='URI',
            description="The URI pointing to the CSV file (usually the filepath).").replace('\n', "\n" + indent)
        # skipinitialspace_json_schema = JsonUtils.attribute_json_schema(
        #    type_name=AttributeType.TYPE_NAME_BOOLEAN, key='skipinitialspace', title='Skip Initial Space',
        #    description="Whether to skip spaces after the delimiter.").replace('\n', "\n" + indent)
        use_original_header_json_schema = JsonUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_BOOLEAN, key='use_original_header', title='Use Original Header',
            description="Whether to use the header from the CSV file.").replace('\n', "\n" + indent)
        # type_name_json_schema = ConnectorCSV.type_name_json_schema()
        # type_name_json_schema_inner = type_name_json_schema.replace('\n', "\n" + indent)
        # type_name_json_schema_outer = type_name_json_schema.replace('\n', "\n      ")

        attribute_permissions_json_schema = JsonUtils.attribute_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "Connector CSV",
  "description": "This connector defines the CSV file connection of its database.",
  "type": "object",
  "properties": {{
    "type_name": {{
      "title": "Type Name",
      "description": "The type name of each attribute group is 'list'.",
      "type": "string",
      "const": "list"
    }},
    "key": {{
      "title": "Key",
      "description": "This attribute group's key is 'connector'.",
      "type": "string",
      "const": "connector"
    }},
    "value": {{
      "title": "Value",
      "description": "Each attribute group has a specific non-empty list of attributes as value.",
      "type": "array",
      "minItems": 1,
      "items": {{
        "oneOf": [
          {decimal_json_schema},
          {sep_json_schema},
          {uri_json_schema},
          {use_original_header_json_schema}
        ]
      }},
      "uniqueItemProperties": [ "key" ]
    }},
    "permissions": {attribute_permissions_json_schema}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""
