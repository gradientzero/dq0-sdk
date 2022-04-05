from dq0.sdk.data.metadata.specification.dataset.v1.database import Database
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.dataset.attribute import Attribute as JsonSchemaDatasetAttribute
from dq0.sdk.data.metadata.specification.json_schema.dataset.attributes_group import AttributesGroup as JsonSchemaDatasetAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


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
        }, required_keys={'data', 'differential_privacy'})
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
            }, required_keys={'privacy_level'})

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
    def json_schema():
        return JsonSchemaNode.json_schema(
            NodeType.TYPE_NAME_DATASET,
            attributes_groups=[
                JsonSchemaDatasetAttributesGroup.data(
                    attributes=[
                        JsonSchemaDatasetAttribute.description(
                            node_type_name=NodeType.TYPE_NAME_DATASET
                        ),
                        JsonSchemaDatasetAttribute.metadata_is_public(
                            node_type_name=NodeType.TYPE_NAME_DATASET
                        ),
                        JsonSchemaDatasetAttribute.name(
                            node_type_name=NodeType.TYPE_NAME_DATASET
                        ),
                        JsonSchemaAttribute.no_key_list(
                            key='tags',
                            attribute_name='tags',
                            description=f"The 'tags' attribute. A list of 'tag' values attached to the '{NodeType.TYPE_NAME_DATASET}'.",
                            item_attribute_name='tag',
                            item_description=f"A 'tag' attribute. Represents a single 'tag' value attached to the '{NodeType.TYPE_NAME_DATASET}'.",
                            item_type_name=AttributeType.TYPE_NAME_STRING
                        )
                    ]
                ),
                JsonSchemaDatasetAttributesGroup.differential_privacy(
                    attributes=[
                        JsonSchemaDatasetAttribute.privacy_level(
                            node_type_name=NodeType.TYPE_NAME_DATASET
                        )
                    ],
                    contains=JsonSchemaAttribute.json_schema(
                        key='privacy_level',
                        attribute_name="privacy level",
                        description="This item ensures that the 'privacy_level' attribute is present.",
                        type_name=AttributeType.TYPE_NAME_INT
                    ),
                    additional_description="Requires a 'privacy_level' attribute."
                )
            ],
            attributes_groups_additional_contains=JsonSchemaAttributesGroup.json_schema(
                key='differential_privacy',
                group_name="differential privacy",
                description="This item ensures, that the 'differential privacy' attributes group is present."
            ),
            attributes_groups_additional_description="Requires 'differential_privacy' attributes group.",
            child_node_json_schema=Database.json_schema()
        )