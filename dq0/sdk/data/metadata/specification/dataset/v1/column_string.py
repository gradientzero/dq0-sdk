from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.dataset.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.dataset.column import Column as JsonSchemaColumn
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class ColumnString:
    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'private_sql': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_sql_and_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'machine_learning': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
        }, required_keys={'data'})
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].get_value(), check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].get_value(), check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [
                tmp_attribute for tmp_attribute in private_sql_attributes[0].get_value() if tmp_attribute.get_key() == 'allowed_values'] \
                if private_sql_attributes[0].get_value() is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].get_value(), check_data={
                    None: ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].get_value(), check_data={
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].get_value(), check_data={
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].get_value(), check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def json_schema():
        return JsonSchemaNode.json_schema(
            NodeType.TYPE_NAME_COLUMN,
            attributes_groups=[
                JsonSchemaColumn.data(data_type_name=AttributeType.TYPE_NAME_STRING),
                JsonSchemaAttributesGroup.private_sql(
                    attributes=[
                        JsonSchemaAttribute.no_key_list(
                            key='allowed_values',
                            attribute_name="allowed values",
                            description=f"The 'allowed values' attribute. A list of allowed values for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            item_attribute_name='allowed_value',
                            item_description=f"An 'allowed value' attribute. Represents a single allowed value for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            item_type_name=AttributeType.TYPE_NAME_STRING
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='mask',
                            attribute_name='mask',
                            description=f"The 'mask' attribute. Specifies a mask for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_STRING
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='private_id',
                            attribute_name="private id",
                            description=f"The 'private id' attribute. Specifies whether this '{NodeType.TYPE_NAME_COLUMN}' is a private id.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_sql_and_synthesis(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='cardinality',
                            attribute_name='cardinality',
                            description=f"The 'cardinality' attribute. Specifies the cardinality for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_synthesis(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='synthesizable',
                            attribute_name='synthesizable',
                            description=f"The 'synthesizable' attribute. Specifies whether this '{NodeType.TYPE_NAME_COLUMN}' is synthesizable.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                ),
                JsonSchemaColumn.machine_learning()
            ]
        )
