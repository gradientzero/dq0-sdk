from dq0.sdk.data.metadata.specification.dataset.v1.column_boolean import ColumnBoolean
from dq0.sdk.data.metadata.specification.dataset.v1.column_datetime import ColumnDatetime
from dq0.sdk.data.metadata.specification.dataset.v1.column_float import ColumnFloat
from dq0.sdk.data.metadata.specification.dataset.v1.column_int import ColumnInt
from dq0.sdk.data.metadata.specification.dataset.v1.column_string import ColumnString
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Column:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Column.apply_defaults_to_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_node(role_uuids=role_uuids) if node.get_permissions() is None else node.get_permissions().copy()
        return Node(type_name=node.get_type_name(), attributes=applied_attributes, child_nodes=None, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            if applied_attribute.get_key() in ['differential_privacy', 'private_sql', 'private_sql_and_synthesis', 'private_synthesis']:
                applied_attribute.set_default_permissions(default_permissions=owner_attribute)
            else:
                if applied_attribute.get_key() == 'machine_learning':
                    for sub_attribute in applied_attribute.get_value() if applied_attribute.get_value() is not None else []:
                        sub_attribute.set_default_permissions(default_permissions=analyst_attribute)
                applied_attribute.set_default_permissions(default_permissions=shared_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_COLUMN], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        Column.verify_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        Column.verify_child_nodes(child_nodes=node.get_child_nodes(), role_uuids=role_uuids)

    @staticmethod
    def verify_data_attributes_and_get_data_type_name(attributes, role_uuids=None):
        data_type_name = None
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].get_value(), check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
            data_type_name_attributes = [tmp_attribute for tmp_attribute in data_attributes[0].get_value() if tmp_attribute.get_key() == 'data_type_name'] \
                if data_attributes[0].get_value() is not None else []
            if 0 < len(data_type_name_attributes):
                data_type_name = data_type_name_attributes[0].get_value()
        return data_type_name

    @staticmethod
    def verify_private_sql_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].get_value(), check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [
                tmp_attribute for tmp_attribute in private_sql_attributes[0].get_value() if tmp_attribute.get_key() == 'allowed_values'] \
                if private_sql_attributes[0].get_value() is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].get_value(), check_data={
                    None: ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_STRING],
                           owner_attribute),
                })

    @staticmethod
    def verify_private_sql_and_synthesis_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].get_value(), check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            })

    @staticmethod
    def verify_private_synthesis_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].get_value(), check_data={
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'min_step': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })

    @staticmethod
    def verify_machine_learning_attributes(attributes, role_uuids=None):
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].get_value(), check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'private_sql': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_sql_and_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'machine_learning': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
        }, required_keys={'data'})
        data_type_name = Column.verify_data_attributes_and_get_data_type_name(attributes=attributes, role_uuids=role_uuids)
        Column.verify_private_sql_attributes(attributes=attributes, role_uuids=role_uuids)
        Column.verify_private_sql_and_synthesis_attributes(attributes=attributes, role_uuids=role_uuids)
        Column.verify_private_synthesis_attributes(attributes=attributes, role_uuids=role_uuids)
        Column.verify_machine_learning_attributes(attributes=attributes, role_uuids=role_uuids)
        if data_type_name is None:
            raise Exception("attribute data_type_name is missing in column")
        if data_type_name == 'boolean':
            ColumnBoolean.verify_attributes(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'datetime':
            ColumnDatetime.verify_attributes(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'float':
            ColumnFloat.verify_attributes(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'int':
            ColumnInt.verify_attributes(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'string':
            ColumnString.verify_attributes(attributes=attributes, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown data_type_name {data_type_name}")

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        if len(child_nodes) != 0:
            raise Exception("column cannot have child nodes")

    @staticmethod
    def json_schema():
        return JsonSchemaNode.json_schema(
            NodeType.TYPE_NAME_COLUMN,
            attributes_groups=[
                JsonSchemaAttributesGroup.data(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='data_type_name',
                            attribute_name='data type name',
                            description="The 'data type name' attribute. Specifies the name of the data type "
                                f"for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_STRING,
                            additional_value=f"\"enum\": [ \"{AttributeType.TYPE_NAME_BOOLEAN}\", \"{AttributeType.TYPE_NAME_DATETIME}\", "
                                f"\"{AttributeType.TYPE_NAME_FLOAT}\", \"{AttributeType.TYPE_NAME_INT}\", \"{AttributeType.TYPE_NAME_STRING}\" ]"
                        ),
                        JsonSchemaAttribute.description(
                            node_type_name=NodeType.TYPE_NAME_COLUMN
                        ),
                        JsonSchemaAttribute.metadata_is_public(
                            node_type_name=NodeType.TYPE_NAME_COLUMN
                        ),
                        JsonSchemaAttribute.name(
                            node_type_name=NodeType.TYPE_NAME_COLUMN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='selectable',
                            attribute_name='selectable',
                            description="The 'selectable' attribute. Specifies whether a selection may happen "
                                f"for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ],
                    additional_contains=[
                        JsonSchemaAttribute.json_schema(
                            key='data_type_name',
                            attribute_name='data type name',
                            description="This item ensures that the 'data_type_name' attribute is present.",
                            type_name=AttributeType.TYPE_NAME_STRING
                        )
                    ],
                    additional_description=" Requires a 'data_type_name' attribute."
                ),
                JsonSchemaAttributesGroup.private_sql(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='selectable',
                            attribute_name='selectable',
                            description="The 'selectable' attribute. Specifies whether a selection may happen "
                                f"for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                )
            ]
        )
