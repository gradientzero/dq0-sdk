from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils


class Attribute:
    @staticmethod
    def key_property(attribute_name, key):
        return f""""key": {{
  "title": "Key",
  "description": "The {attribute_name} attribute's key is '{key}'"
  "type": "string",
  "const": "{key}"
}}"""

    @staticmethod
    def value_property(attribute_name, type_name, additional=None):
        value_type = None
        value_format = ''
        value_additional = ''
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            value_type = 'boolean'
        elif type_name == AttributeType.TYPE_NAME_DATETIME:
            value_type = 'object'
            value_format = ",\n  \"format\": \"date-time\""
        elif type_name == AttributeType.TYPE_NAME_FLOAT:
            value_type = 'number'
        elif type_name == AttributeType.TYPE_NAME_INT:
            value_type = 'integer'
        elif type_name == AttributeType.TYPE_NAME_LIST:
            value_type = 'array'
        elif type_name == AttributeType.TYPE_NAME_STRING:
            value_type = 'string'
        else:
            raise Exception(f"unknown type_name {type_name} provided")
        if additional is not None:
            value_additional = ",\n  " + additional.replace('\n', "\n  ")
        return f""""value": {{
  "title": "Value",
  "description": "The {attribute_name} attribute's value.'"
  "type": "{value_type}"{value_format}{value_additional}
}}"""

    @staticmethod
    def json_schema(key, title, attribute_name, description, type_name, value_additional=None):
        indent = "    "
        type_name_property = JsonSchemaUtils.type_name_property(object_name=attribute_name, object_type='attribute', type_name=type_name).replace(
            '\n', '\n' + indent)
        key_property = Attribute.key_property(attribute_name=attribute_name, key=key).replace('\n', '\n' + indent)
        value_property = Attribute.value_property(attribute_name=attribute_name, type_name=type_name, additional=value_additional).replace(
            '\n', '\n' + indent)
        attribute_permissions = DefaultPermissions.json_schema_attribute_permissions().replace('\n', "\n    ")
        return f"""{{
  "title": "{title}",
  "description": "{description}",
  "type": "object",
  "properties": {{
    {type_name_property},
    {key_property},
    {value_property},
    "permissions": {attribute_permissions}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""
