from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType


class Utils:
    @staticmethod
    def attribute_json_schema(type_name, key, title, description):
        value_type = None
        value_additional = ''
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            value_type = 'boolean'
        elif type_name == AttributeType.TYPE_NAME_DATETIME:
            value_type = 'object'
            value_additional = ",\n      \"format\": \"date-time\""
        elif type_name == AttributeType.TYPE_NAME_FLOAT:
            value_type = 'number'
        elif type_name == AttributeType.TYPE_NAME_INT:
            value_type = 'integer'
        elif type_name == AttributeType.TYPE_NAME_LIST:
            raise Exception("cannot generate json schema for list attribute")
        elif type_name == AttributeType.TYPE_NAME_STRING:
            value_type = 'string'
        else:
            raise Exception(f"unknown type_name {type_name} provided")
        if not isinstance(key, str):
            raise Exception(f"key {key} is not of type str, is of type {type(key)} instead")
        permissions_json_schema = Utils.attribute_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "{title}",
  "description": "{description}",
  "type": "object",
  "properties": {{
    "type_name": {{
      "title": "Type Name",
      "description": "This attribute's type name is '{type_name}'.",
      "type": "string",
      "const": "{type_name}"
    }},
    "key": {{
      "title": "Key",
      "description": "This attribute's key is '{key}'.",
      "type": "string",
      "const": "{key}"
    }},
    "value": {{
      "title": "Value",
      "description": "This attribute's value of type '{type_name}'.",
      "type": "{value_type}"{value_additional}
    }},
    "permissions": {permissions_json_schema}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def attribute_permissions_json_schema():
        return """{
  "title": "Permissions",
  "description": "Attribute permissions object, governing access to its parent attribute.",
  "oneOf": [
    {
      "type": "null"
    },
    {
      "type": "object",
      "properties": {
        "read": {
          "title": "Read",
          "description": "List of user/role uuids allowed to read the parent attribute (value & permissions).",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        },
        "write_permissions": {
          "title": "Write Permissions",
          "description": "List of user/role uuids allowed to write the permissions of the parent attribute.",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        },
        "write_value": {
          "title": "Write Value",
          "description": "List of user/role uuids allowed to modify the value of the parent attribute.",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        }
      },
      "minProperties": 1,
      "additionalProperties": false
    }
  ]
}"""

    @staticmethod
    def node_permissions_json_schema():
        return """{
  "title": "Permissions",
  "description": "Node permissions object, governing access to its parent node.",
  "oneOf": [
    {
      "type": "null"
    },
    {
      "type": "object",
      "properties": {
        "read": {
          "title": "Read",
          "description": "List of user/role uuids allowed to read the parent node (attributes & child nodes & permissions).",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        },
        "write_attributes": {
          "title": "Write Attributes",
          "description": "List of user/role uuids allowed to modify the attributes of the parent node.",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        },
        "write_child_nodes": {
          "title": "Write Child Nodes",
          "description": "List of user/role uuids allowed to modify the child nodes of the parent node.",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        },
        "write_permissions": {
          "title": "Write Permissions",
          "description": "List of user/role uuids allowed to write the permissions of the parent node.",
          "type": "object",
          "patternProperties": {
            "^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})+$": { "type": "null" }
          },
          "additionalProperties": false
        }
      },
      "minProperties": 1,
      "additionalProperties": false
    }
  ]
}"""
