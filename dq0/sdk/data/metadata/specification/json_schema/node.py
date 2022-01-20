from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils


class Node:
    @staticmethod
    def attributes_property(node_type_name, attributes_groups):
        attributes_groups_items = ''
        for index, attributes_group in enumerate(attributes_groups):
            if 0 < index:
                attributes_groups_items += "\n      "
            attributes_groups_items += attributes_group.replace("\n", "\n      ")
            if index < len(attributes_groups) - 1:
                attributes_groups_items += ','
        contains_json = AttributesGroup.json_schema(
            key='data', title='Data', group_name='data', description="This item ensures, that the 'data' attributes group is present.",
            contains=Attribute.json_schema(
                key='name', title='Name', attribute_name='name', description="This item ensures that the 'name' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING)).replace("\n", "\n  ")
        return f""""attributes": {{
  "title": "Attributes",
  "description": "List of attribute groups of a '{node_type_name}' node. The 'data' group is mandatory."
  "type": "array",
  "minItems": 1,
  "contains": {contains_json},
  "items": {{
    "oneOf": [
      {attributes_groups_items}
    ]
  }},
  "uniqueItemProperties": [ "key" ]
}}"""

    @staticmethod
    def child_nodes_property(node_type_name, child_node_json):
        return f""""child_nodes": {{
  "title": "Child Nodes",
  "description": "List of child nodes of a '{node_type_name}' node."
  "type": "array",
  "minItems": 1,
  "items": {child_node_json}
}}"""

    @staticmethod
    def json_schema(title, type_name, attributes_groups, child_node_json=None):
        type_name_property = JsonSchemaUtils.type_name_property(object_name=type_name, object_type='node', type_name=type_name).replace('\n', "\n    ")
        attributes_property = Node.attributes_property(node_type_name=type_name, attributes_groups=attributes_groups).replace('\n', "\n    ")
        child_nodes_property = ''
        if child_node_json is not None:
            child_nodes_property = ",\n    " + Node.child_nodes_property(node_type_name=type_name, child_node_json=child_node_json).replace('\n', "\n    ")
        node_permissions = DefaultPermissions.json_schema_node_permissions().replace('\n', "\n    ")
        return f"""{{
  "title": "{title}",
  "description": "A '{type_name}' node in the metadata structure.",
  "type": "object",
  "properties": {{
    {type_name_property},
    {attributes_property}{child_nodes_property},
    "permissions": {node_permissions}
  }},
  "required": [ "type_name", "attributes" ],
  "additionalProperties": false
}}"""
