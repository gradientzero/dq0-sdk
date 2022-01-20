from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class Attribute:
    @staticmethod
    def key_property(attribute_name, key, any_key=False):
        type_value = 'string'
        const_field = ",\n  \"const\": " + f"\"{key}\""
        if any_key:
            key = "any key"
            const_field = ''
        if not any_key and key is None:
            key = 'null'
            type_value = 'null'
            const_field = ''
        return f""""key": {{
  "description": "The '{attribute_name}' attribute's key is '{key}'",
  "type": "{type_value}"{const_field}
}}"""

    @staticmethod
    def value_property(attribute_name, type_name, additional_value=None, additional_description=None):
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
        if additional_value is not None:
            value_additional = ",\n  " + additional_value.replace('\n', "\n  ")
        return f""""value": {{
  "description": "The '{attribute_name}' attribute's value.{' ' + additional_description if additional_description is not None else ''}",
  "type": "{value_type}"{value_format}{value_additional}
}}"""

    @staticmethod
    def json_schema(key, attribute_name, description, type_name, additional_value=None, additional_description=None, any_key=False):
        indent = "    "
        type_name_property = JsonSchemaUtils.type_name_property(object_name=attribute_name, object_type='attribute', type_name=type_name).replace(
            '\n', '\n' + indent)
        key_property = Attribute.key_property(attribute_name=attribute_name, key=key, any_key=any_key).replace('\n', '\n' + indent)
        key_value = ", \"key\""
        if key is None:
            key_value = ''
        if any_key:
            key_value = ", \"key\""
            key_property = Attribute.key_property(attribute_name=attribute_name, key=key, any_key=any_key).replace('\n', '\n' + indent)
        value_property = Attribute.value_property(attribute_name=attribute_name, type_name=type_name, additional_value=additional_value,
                                                  additional_description=additional_description).replace(
            '\n', '\n' + indent)
        return f"""{{
  "description": "{description}",
  "type": "object",
  "properties": {{
    {type_name_property},
    {key_property},
    {value_property},
    "permissions": {{ "$ref": "#/$defs/attribute_permissions" }}
  }},
  "required": [ "type_name"{key_value}, "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def any_key_value_list(key, attribute_name, description, item_attribute_name, item_description):
        indent = "    "
        type_name_property = JsonSchemaUtils.type_name_property(object_name=attribute_name, object_type='attribute',
                                                                type_name=AttributeType.TYPE_NAME_LIST).replace('\n', '\n' + indent)
        key_property = Attribute.key_property(attribute_name=attribute_name, key=key).replace('\n', '\n' + indent)
        boolean_value = Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description,
                                              type_name=AttributeType.TYPE_NAME_BOOLEAN, any_key=True).replace('\n', '\n' + indent)
        date_time_value = Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description,
                                                type_name=AttributeType.TYPE_NAME_DATETIME, any_key=True).replace('\n', '\n' + indent)
        number_value = Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description,
                                             type_name=AttributeType.TYPE_NAME_FLOAT, any_key=True).replace('\n', '\n' + indent)
        integer_value = Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description,
                                              type_name=AttributeType.TYPE_NAME_INT, any_key=True).replace('\n', '\n' + indent)
        string_value = Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description,
                                             type_name=AttributeType.TYPE_NAME_STRING, any_key=True).replace('\n', '\n' + indent)
        value_property = Attribute.value_property(attribute_name=attribute_name, type_name=AttributeType.TYPE_NAME_LIST,
                                                  additional_value=f""""minItems": 1,
"items": {{
  "oneOf": [
    {boolean_value},
    {date_time_value},
    {number_value},
    {integer_value},
    {string_value}
  ]
}},
"uniqueItemProperties": [ "key" ]""").replace('\n', '\n' + indent)
        return f"""{{
  "description": "{description}",
  "type": "object",
  "properties": {{
    {type_name_property},
    {key_property},
    {value_property},
    "permissions": {{ "$ref": "#/$defs/attribute_permissions" }}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def no_key_list(key, attribute_name, description, item_attribute_name, item_description, item_type_name, item_additional_value=None):
        additional_value = f""""min_items": 1,
"items": {Attribute.json_schema(key=None, attribute_name=item_attribute_name, description=item_description, type_name=item_type_name,
                                additional_value=item_additional_value)}"""
        return Attribute.json_schema(
            key=key,
            attribute_name=attribute_name,
            description=description,
            type_name=AttributeType.TYPE_NAME_LIST,
            additional_value=additional_value)
