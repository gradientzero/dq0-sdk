from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.v1.database import Database
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.utils import Utils as JsonSchemaUtils


class Dataset:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Dataset.apply_defaults_to_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        applied_child_nodes = Dataset.apply_defaults_to_child_nodes(child_nodes=node.get_child_nodes(), role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_node(role_uuids=role_uuids) if node.get_permissions() is None else node.get_permissions().copy()
        return Node(type_name=node.get_type_name(), attributes=applied_attributes, child_nodes=applied_child_nodes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            if applied_attribute.get_key() in ['differential_privacy']:
                applied_attribute.set_default_permissions(default_permissions=owner_attribute)
            else:
                applied_attribute.set_default_permissions(default_permissions=shared_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def apply_defaults_to_child_nodes(child_nodes, role_uuids=None):
        Node.check_list(node_list=child_nodes, allowed_type_names=None, allowed_permissions=None)
        applied_child_nodes = [] if len(child_nodes) != 0 else None
        for child_node in child_nodes if child_nodes is not None else []:
            applied_child_nodes.append(Database.apply_defaults(node=child_node, role_uuids=role_uuids))
        return applied_child_nodes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_DATASET], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        Dataset.verify_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        Dataset.verify_child_nodes(child_nodes=node.get_child_nodes(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'differential_privacy': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
        }, required_keys={'data'})
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].get_value(), check_data={
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'tags': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            }, required_keys={'name'})
            tags_attributes = [tmp_attribute for tmp_attribute in data_attributes[0].get_value() if tmp_attribute.get_key() == 'tags'] \
                if data_attributes[0].get_value() is not None else []
            if 0 < len(tags_attributes):
                Attribute.check_list(attribute_list=tags_attributes[0].get_value(), check_data={
                    None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                })
        differential_privacy_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'differential_privacy'] \
            if attributes is not None else []
        if 0 < len(differential_privacy_attributes):
            Attribute.check_list(attribute_list=differential_privacy_attributes[0].get_value(), check_data={
                'privacy_level': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        names = set()
        for child_node in child_nodes if child_nodes is not None else []:
            Database.verify(node=child_node, role_uuids=role_uuids)
            data_attribute = child_node.get_attribute(key='data')
            name_attribute = data_attribute.get_attribute(key='name') if data_attribute is not None else None
            if name_attribute is not None and isinstance(name_attribute.get_value(), str):
                names.add(name_attribute.get_value())
        if len(names) != len(child_nodes):
            raise Exception(f"names {names} are not enough for each of the {len(child_nodes)} child nodes to have a unique name")

    @staticmethod
    def tags_json_schema():
        attribute_permissions_json_schema = JsonSchemaUtils.attribute_permissions_json_schema()
        attribute_permissions_json_schema_inner = attribute_permissions_json_schema.replace('\n', "\n          ")
        attribute_permissions_json_schema_outer = attribute_permissions_json_schema.replace('\n', "\n    ")
        return f"""{{
  "title": "Tags",
  "description": "Tags attribute object. Represents a list of string tags.",
  "type": "object",
  "properties": {{
    "type_name": {{
      "title": "Type Name",
      "description": "The tags attribute is of type 'list'.",
      "type": "string",
      "const": "list"
    }},
    "key": {{
      "title": "Key",
      "description": "This attribute's key is 'tags'.",
      "type": "string",
      "const": "tags"
    }},
    "value": {{
      "title": "Value",
      "description": "The tags attribute's value is a list of tag attributes.",
      "type": "array",
      "minItems": 1,
      "items": {{
        "title": "Item",
        "description": "Each item is a tag.",
        "type": "object",
        "properties": {{
          "type_name": {{
            "title": "Type Name",
            "description": "A tag is of type 'string'.",
            "type": "string",
            "const": "string"
          }},
          "key": {{
            "title": "Key",
            "description": "A tag may not have a key set.",
            "type": "null"
          }},
          "value": {{
            "title": "Value",
            "description": "A tag's string value.",
            "type": "string"
          }},
          "permissions": {attribute_permissions_json_schema_inner}
        }},
        "required": [ "type_name", "value" ],
        "additionalProperties": false
      }}
    }},
    "permissions": {attribute_permissions_json_schema_outer}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def data_json_schema():
        indent = "          "
        description_json_schema = JsonSchemaUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_STRING, key='description', title='Description',
            description="The description of the defined dataset.").replace('\n', "\n" + indent)
        metadata_is_public_json_schema = JsonSchemaUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_BOOLEAN, key='metadata_is_public', title="Metadata is Public",
            description="Whether the provided metadata in this file is visible to all users.").replace('\n', "\n" + indent)
        name_json_schema = JsonSchemaUtils.attribute_json_schema(
            type_name=AttributeType.TYPE_NAME_STRING, key='name', title='Name',
            description="The name of the defined dataset.")
        name_json_schema_outer = name_json_schema.replace('\n', "\n      ")
        name_json_schema_inner = name_json_schema.replace('\n', "\n" + indent)
        tags_json_schema = Dataset.tags_json_schema().replace('\n', "\n" + indent)
        attribute_permissions_json_schema = JsonSchemaUtils.attribute_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "Data",
  "description": "The data attributes group. Contains general attributes of the outer data object.",
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
      "description": "This attribute group's key is 'data'.",
      "type": "string",
      "const": "data"
    }},
    "value": {{
      "title": "Value",
      "description": "Each attribute group has a specific non-empty list of attributes as value. Here, the 'name' attribute is mandatory.",
      "type": "array",
      "minItems": 1,
      "contains": {name_json_schema_outer},
      "items": {{
        "oneOf": [
          {description_json_schema},
          {metadata_is_public_json_schema},
          {name_json_schema_inner},
          {tags_json_schema}
        ]
      }},
      "uniqueItemProperties": [ "key" ]
    }},
    "permissions": {attribute_permissions_json_schema}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def privacy_level_json_schema():
        attribute_permissions_json_schema = JsonSchemaUtils.attribute_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "Privacy Level",
  "description": "The privacy level determines the amount of data privacy protection.",
  "type": "object",
  "properties": {{
    "type_name": {{
      "title": "Type Name",
      "description": "The privacy level attribute is of type 'int'.",
      "type": "string",
      "const": "int"
    }},
    "key": {{
      "title": "Key",
      "description": "This attribute's key is 'privacy_level'.",
      "type": "string",
      "const": "privacy_level"
    }},
    "value": {{
      "title": "Value",
      "description": "The privacy level attribute's value may only have one of the values [0, 1, 2].",
      "type": "integer",
      "minimum": 0,
      "maximum": 2
    }},
    "permissions": {attribute_permissions_json_schema}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def differential_privacy_json_schema():
        indent = "          "
        privacy_level_json_schema = Dataset.privacy_level_json_schema().replace('\n', "\n" + indent)
        attribute_permissions_json_schema = JsonSchemaUtils.attribute_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "Differential Privacy",
  "description": "The differential privacy attributes group. Contains attributes pertaining differentially private data protection mechanisms.",
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
      "description": "This attribute group's key is 'differential_privacy'.",
      "type": "string",
      "const": "differential_privacy"
    }},
    "value": {{
      "title": "Value",
      "description": "Each attribute group has a specific non-empty list of attributes as value.",
      "type": "array",
      "minItems": 1,
      "items": {{
        "oneOf": [
          {privacy_level_json_schema}
        ]
      }},
      "uniqueItemProperties": [ "key" ]
    }},
    "permissions": {attribute_permissions_json_schema}
  }},
  "required": [ "type_name", "key", "value" ],
  "additionalProperties": false
}}"""

    @staticmethod
    def json_schema():
        indent = "          "
        data_json_schema = Dataset.data_json_schema()
        data_json_schema_outer = data_json_schema.replace('\n', "\n      ")
        data_json_schema_inner = data_json_schema.replace('\n', "\n" + indent)
        differential_privacy_json_schema = Dataset.differential_privacy_json_schema().replace('\n', "\n" + indent)
        database_json_schema = Database.json_schema().replace('\n', "\n      ")
        node_permissions_json_schema = JsonSchemaUtils.node_permissions_json_schema().replace('\n', "\n    ")
        return f"""{{
  "title": "Dataset",
  "description": "The main dataset node in the metadata structure.",
  "type": "object",
  "properties": {{
    "type_name": {{
      "title": "Type Name",
      "description": "The type name of a dataset is 'dataset'.",
      "type": "string",
      "const": "dataset"
    }},
    "attributes": {{
      "title": "Attributes",
      "description": "The attribute groups of a dataset. The 'data' group is mandatory.",
      "type": "array",
      "minItems": 1,
      "contains": {data_json_schema_outer},
      "items": {{
        "oneOf": [
          {data_json_schema_inner},
          {differential_privacy_json_schema}
        ]
      }},
      "uniqueItemProperties": [ "key" ]
    }},
    "child_nodes": {{
      "title": "Child Nodes",
      "description": "The child nodes of a dataset. These are the datasets databases.",
      "type": "array",
      "minItems": 1,
      "items": {database_json_schema}
    }},
    "permissions": {node_permissions_json_schema}
  }},
  "required": [ "type_name", "attributes" ],
  "additionalProperties": false
}}"""
