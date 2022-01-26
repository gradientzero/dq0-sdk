from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils


class Node:
    @staticmethod
    def attributes_property(node_type_name, attributes_groups, additional_contains):
        attributes_groups_items = ''
        for index, attributes_group in enumerate(attributes_groups):
            if 0 < index:
                attributes_groups_items += "\n      "
            attributes_groups_items += attributes_group.replace("\n", "\n      ")
            if index < len(attributes_groups) - 1:
                attributes_groups_items += ','
        contains = AttributesGroup.json_schema(
            key='data',
            group_name='data',
            description="This item ensures, that the 'data' attributes group is present.").replace('\n', "\n  ")
        contains_json = f"  \"contains\": {contains}"
        if additional_contains is not None:
          indented_contains_json = contains.replace('\n', "\n  ")
          contains_json = "\"allOf\": [\n  {\n    "
          contains_json += f"\"contains\": {indented_contains_json}"
          contains_json += ",\n    "
          indented_contains_json = additional_contains.replace('\n', "\n    ")
          contains_json += f"\"contains\": {indented_contains_json}"
          contains_json += "\n  }\n]"
          contains_json = contains_json.replace('\n', "\n  ")
          contains_json = '  ' + contains_json
        return f""""attributes": {{
  "description": "List of attribute groups of a '{node_type_name}' node. Requires 'data' attributes group.",
  "type": "array",
  "minItems": 1,
{contains_json},
  "items": {{
    "oneOf": [
      {attributes_groups_items}
    ]
  }},
  "uniqueItemProperties": [ "key" ]
}}"""

    @staticmethod
    def child_nodes_property(node_type_name, child_node_json):
        child_nodes = child_node_json.replace('\n', "\n  ")
        return f""""child_nodes": {{
  "description": "List of child nodes of a '{node_type_name}' node.",
  "type": "array",
  "minItems": 1,
  "items": {child_nodes}
}}"""

    @staticmethod
    def json_schema(type_name, attributes_groups, attributes_groups_additional_contains=None, child_node_json_schema=None):
        type_name_property = JsonSchemaUtils.type_name_property(object_name=type_name, object_type='node', type_name=type_name).replace('\n', "\n    ")
        attributes_property = Node.attributes_property(node_type_name=type_name, attributes_groups=attributes_groups,
                                                       additional_contains=attributes_groups_additional_contains).replace('\n', "\n    ")
        child_nodes_property = ''
        if child_node_json_schema is not None:
            child_nodes_property = ",\n    " + Node.child_nodes_property(node_type_name=type_name, child_node_json=child_node_json_schema).replace(
                '\n', "\n    ")
        return f"""{{
  "description": "A '{type_name}' node in the metadata structure.",
  "type": "object",
  "properties": {{
    {type_name_property},
    {attributes_property}{child_nodes_property},
    "permissions": {{ "$ref": "#/$defs/node_permissions" }}
  }},
  "required": [ "type_name", "attributes" ],
  "additionalProperties": false
}}"""
