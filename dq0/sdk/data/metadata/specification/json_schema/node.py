from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


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
            key='data', group_name='data', description="This item ensures, that the 'data' attributes group is present.",
            contains=Attribute.json_schema(
                key='name', attribute_name='name', description="This item ensures that the 'name' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING)).replace("\n", "\n  ")
        return f""""attributes": {{
  "description": "List of attribute groups of a '{node_type_name}' node. Requires 'data' attributes group with 'name' attribute.",
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
        child_nodes = child_node_json.replace('\n', "\n  ")
        return f""""child_nodes": {{
  "description": "List of child nodes of a '{node_type_name}' node.",
  "type": "array",
  "minItems": 1,
  "items": {child_nodes}
}}"""

    @staticmethod
    def json_schema(type_name, attributes_groups, child_node_json_schema=None):
        type_name_property = JsonSchemaUtils.type_name_property(object_name=type_name, object_type='node', type_name=type_name).replace('\n', "\n    ")
        attributes_property = Node.attributes_property(node_type_name=type_name, attributes_groups=attributes_groups).replace('\n', "\n    ")
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

    @staticmethod
    def description_attribute(node_type_name):
        return Attribute.json_schema(
            key='description',
            attribute_name='description',
            description=f"The 'description' attribute. Describes the '{node_type_name}'.",
            type_name=AttributeType.TYPE_NAME_STRING)

    @staticmethod
    def metadata_is_public_attribute(node_type_name):
        return Attribute.json_schema(
            key='metadata_is_public',
            attribute_name='metadata is public',
            description=f"The 'metadata is public' attribute. Specifies whether the '{node_type_name}' metadata is public.",
            type_name=AttributeType.TYPE_NAME_BOOLEAN)

    @staticmethod
    def name_attribute(node_type_name):
        return Attribute.json_schema(
            key='name',
            attribute_name='name',
            description=f"The 'name' attribute. Mandatory and required to be unique among all elements of type '{node_type_name}'.",
            type_name=AttributeType.TYPE_NAME_STRING)

    @staticmethod
    def data_attributes_group(attributes):
        return AttributesGroup.json_schema(
            key='data',
            group_name='data',
            description="The 'data' attributes group. This group is mandatory and must contain at least the 'name' attribute.",
            attributes=attributes)

    @staticmethod
    def privacy_level_attribute(node_type_name):
        additional_value = """"minimum": 0,
"maximum": 2"""
        return Attribute.json_schema(
            key='privacy_level',
            attribute_name='privacy level',
            description=f"The 'privacy level' attribute. Sets the level of privacy protection for '{node_type_name}'. "
                "A child node's setting of 'privacy level' will take precedence for the respective child node. "
                "Allowed values are [0, 1, 2].",
            type_name=AttributeType.TYPE_NAME_INT,
            additional_value=additional_value)

    @staticmethod
    def differential_privacy_attributes_group(attributes):
        return AttributesGroup.json_schema(
            key='differential_privacy',
            group_name='differential privacy',
            description="The 'differential privacy' attributes group.",
            attributes=attributes)
