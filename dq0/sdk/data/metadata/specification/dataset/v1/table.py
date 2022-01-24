from dq0.sdk.data.metadata.specification.dataset.v1.column import Column
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Table:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Table.apply_defaults_to_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        applied_child_nodes = Table.apply_defaults_to_child_nodes(child_nodes=node.get_child_nodes(), role_uuids=role_uuids)
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
            if applied_attribute.get_key() in ['differential_privacy', 'private_sql', 'private_synthesis']:
                applied_attribute.set_default_permissions(default_permissions=owner_attribute)
            else:
                if applied_attribute.get_key() == 'data':
                    for sub_attribute in applied_attribute.get_value() if applied_attribute.get_value() is not None else []:
                        if sub_attribute.get_key() in ['rows']:
                            sub_attribute.set_default_permissions(default_permissions=owner_attribute)
                applied_attribute.set_default_permissions(default_permissions=shared_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def apply_defaults_to_child_nodes(child_nodes, role_uuids=None):
        Node.check_list(node_list=child_nodes, allowed_type_names=None, allowed_permissions=None)
        applied_child_nodes = [] if len(child_nodes) != 0 else None
        for child_node in child_nodes if child_nodes is not None else []:
            applied_child_nodes.append(Column.apply_defaults(node=child_node, role_uuids=role_uuids))
        return applied_child_nodes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_TABLE], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        Table.verify_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        Table.verify_child_nodes(child_nodes=node.get_child_nodes(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'differential_privacy': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_sql': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
        }, required_keys={'data'})
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].get_value(), check_data={
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'rows': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            }, required_keys={'name'})
        differential_privacy_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'differential_privacy'] \
            if attributes is not None else []
        if 0 < len(differential_privacy_attributes):
            Attribute.check_list(attribute_list=differential_privacy_attributes[0].get_value(), check_data={
                'budget_delta': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'budget_epsilon': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'privacy_column': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'privacy_level': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].get_value(), check_data={
                'censor_dims': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'clamp_columns': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'clamp_counts': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'max_ids': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'row_privacy': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'sample_max_ids': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'tau': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'use_dpsu': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].get_value(), check_data={
                'synth_allowed': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        names = set()
        for child_node in child_nodes if child_nodes is not None else []:
            Column.verify(node=child_node, role_uuids=role_uuids)
            data_attribute = child_node.get_attribute(key='data')
            name_attribute = data_attribute.get_attribute(key='name') if data_attribute is not None else None
            if name_attribute is not None and isinstance(name_attribute.get_value(), str):
                names.add(name_attribute.get_value())
        if len(names) != len(child_nodes):
            raise Exception(f"names {names} are not enough for each of the {len(child_nodes)} child nodes to have a unique name")

    @staticmethod
    def json_schema():
        return JsonSchemaNode.json_schema(
            NodeType.TYPE_NAME_TABLE,
            attributes_groups=[
                JsonSchemaAttributesGroup.data(
                    attributes=[
                        JsonSchemaAttribute.description(
                            node_type_name=NodeType.TYPE_NAME_TABLE
                        ),
                        JsonSchemaAttribute.metadata_is_public(
                            node_type_name=NodeType.TYPE_NAME_TABLE
                        ),
                        JsonSchemaAttribute.name(
                            node_type_name=NodeType.TYPE_NAME_TABLE
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='rows',
                            attribute_name='rows',
                            description="The 'rows' attribute. Specifies the number of rows "
                                f"in the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_INT,
                            additional_value="\"minimum\": 0"
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.differential_privacy(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='budget_delta',
                            attribute_name='budget delta',
                            description="The 'budget delta' attribute. Specifies the delta privacy budget "
                                f"for the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_FLOAT,
                            additional_value="\"minimum\": 0.0"
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='budget_epsilon',
                            attribute_name='budget epsilon',
                            description="The 'budget epsilon' attribute. Specifies the epsilon privacy budget "
                                f"for the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_FLOAT,
                            additional_value="\"minimum\": 0.0"
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='privacy_column',
                            attribute_name='privacy column',
                            description="The 'privacy column' attribute. Specifies the column name of the privacy column "
                                f"for the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_STRING
                        ),
                        JsonSchemaAttribute.privacy_level(
                            node_type_name=NodeType.TYPE_NAME_TABLE
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_sql(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='censor_dims',
                            attribute_name='censor dims',
                            description="The 'censor dims' attribute. Specifies whether SQL queries will censor dimensions "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='clamp_columns',
                            attribute_name='clamp columns',
                            description="The 'clamp columns' attribute. Specifies whether SQL queries will clamp column values "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='clamp_counts',
                            attribute_name='clamp counts',
                            description="The 'clamp counts' attribute. Specifies whether SQL queries will clamp counting results "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='max_ids',
                            attribute_name='max ids',
                            description="The 'max ids' attribute. Specifies whether SQL queries will limit the number of ids "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_INT,
                            additional_value="\"minimum\": 0"
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='row_privacy',
                            attribute_name='row privacy',
                            description="The 'row privacy' attribute. Specifies whether SQL queries will use per row privacy "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='sample_max_ids',
                            attribute_name='sample max ids',
                            description="The 'sample max ids' attribute. Specifies whether SQL queries will sample the max amount of ids "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='tau',
                            attribute_name='tau',
                            description="The 'tau' attribute. Specifies the tau budget of Google Differential Privacy "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_FLOAT,
                            additional_value="\"minimum\": 0.0"
                        ),
                        JsonSchemaAttribute.json_schema(
                            key='use_dpsu',
                            attribute_name='use dpsu',
                            description="The 'use dpsu' attribute. Specifies whether SQL queries will use the dpsu option "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                ),
                JsonSchemaAttributesGroup.private_synthesis(
                    attributes=[
                        JsonSchemaAttribute.json_schema(
                            key='synth_allowed',
                            attribute_name='synth_allowed',
                            description="The 'synth_allowed' attribute. Specifies whether private synthetic data generation is allowed "
                                f"on the '{NodeType.TYPE_NAME_TABLE}'.",
                            type_name=AttributeType.TYPE_NAME_BOOLEAN
                        )
                    ]
                )
            ],
            child_node_json_schema=Column.json_schema()
        )
