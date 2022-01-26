from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.column import Column as JsonSchemaColumn
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class ColumnInt:
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
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'differential_privacy_sql'] \
            if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].get_value(), check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [
                tmp_attribute for tmp_attribute in private_sql_attributes[0].get_value() if tmp_attribute.get_key() == 'allowed_values'] \
                if private_sql_attributes[0].get_value() is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].get_value(), check_data={
                    None: ([AttributeType.TYPE_NAME_INT], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].get_value(), check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].get_value(), check_data={
                'min_step': ([AttributeType.TYPE_NAME_INT], owner_attribute),
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
                JsonSchemaColumn.data(data_type_name=AttributeType.TYPE_NAME_INT),
                JsonSchemaAttributesGroup.private_sql(
                    attributes=[
                        JsonSchemaAttribute.no_key_list(
                            key='allowed_values',
                            attribute_name="allowed values",
                            description=f"The 'allowed values' attribute. A list of allowed values for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            item_attribute_name='allowed_value',
                            item_description=f"An 'allowed value' attribute. Represents a single allowed value for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            item_type_name=AttributeType.TYPE_NAME_INT
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='auto_bounds_prob',
                            attribute_name="auto bounds prob",
                            description="The 'auto bounds prob' attribute. Specifies the probability parameter for the automatic bounds "
                                f"of the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_FLOAT,
                            additional_value="\"minimum\": 0.0"
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='auto_lower',
                            attribute_name="auto lower",
                            description=f"The 'auto lower' attribute. Specifies the automatic lower bound for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='auto_upper',
                            attribute_name="auto upper",
                            description=f"The 'auto upper' attribute. Specifies the automatic upper bound for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='private_id',
                            attribute_name="private id",
                            description=f"The 'private id' attribute. Specifies whether this '{NodeType.TYPE_NAME_COLUMN}' is a private id.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='use_auto_bounds',
                            attribute_name="use auto bounds",
                            description="The 'use auto bounds' attribute. Specifies whether automatic bounds are to be used "
                                f"with the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_sql_and_synthesis(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='bounded',
                            attribute_name='bounded',
                            description="The 'bounded' attribute. Specifies whether bounds are to be used "
                                f"with the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='cardinality',
                            attribute_name='cardinality',
                            description=f"The 'cardinality' attribute. Specifies the cardinality for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='lower',
                            attribute_name='lower',
                            description=f"The 'lower' attribute. Specifies the lower bound for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='upper',
                            attribute_name='upper',
                            description=f"The 'upper' attribute. Specifies the upper bound for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_synthesis(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='min_step',
                            attribute_name="min step",
                            description=f"The 'min step' attribute. Specifies the minimum step size for the '{NodeType.TYPE_NAME_COLUMN}'.",
                            type_name=AttributeType.TYPE_NAME_INT
                        ),
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
