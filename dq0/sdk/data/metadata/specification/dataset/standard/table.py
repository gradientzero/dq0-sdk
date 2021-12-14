from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.dataset.standard.column import Column
from dq0.sdk.data.metadata.specification.dataset.standard.connector_csv import ConnectorCSV


class Table:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Table.apply_defaults_to_attributes(attributes=node.attributes, role_uuids=role_uuids)
        applied_child_nodes = Table.apply_defaults_to_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_node(role_uuids=role_uuids) if node.permissions is None else node.permissions.copy()
        return Node(type_name=node.type_name, attributes=applied_attributes, child_nodes=applied_child_nodes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions=None)
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy() if attribute.key != 'connector' else ConnectorCSV.apply_defaults(attribute=attribute, role_uuids=role_uuids)
            if applied_attribute.key in ['differential_privacy', 'private_sql', 'private_synthesis']:
                applied_attribute.set_default_permissions(default_permissions=owner_attribute)
            else:
                if applied_attribute.key == 'data':
                    for sub_attribute in applied_attribute.value if applied_attribute.value is not None else []:
                        if sub_attribute.key in ['rows']:
                            sub_attribute.set_default_permissions(default_permissions=owner_attribute)
                applied_attribute.set_default_permissions(default_permissions=shared_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def apply_defaults_to_child_nodes(child_nodes, role_uuids=None):
        Node.check_list(node_list=child_nodes, allowed_type_names=None, allowed_permissions=None)
        applied_child_nodes = [] if child_nodes is not None else None
        for child_node in child_nodes if child_nodes is not None else []:
            applied_child_nodes.append(Column.apply_defaults(node=child_node, role_uuids=role_uuids))
        return applied_child_nodes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_TABLE], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        Table.verify_attributes(attributes=node.attributes, role_uuids=role_uuids)
        Table.verify_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            'connector': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'differential_privacy': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_sql': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
        })
        connector_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'connector'] if attributes is not None else []
        if 0 < len(connector_attributes):
            ConnectorCSV.verify(attribute=connector_attributes[0], role_uuids=role_uuids)
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, allowed_keys_type_names_permissions={
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'rows': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        differential_privacy_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'differential_privacy'] \
            if attributes is not None else []
        if 0 < len(differential_privacy_attributes):
            Attribute.check_list(attribute_list=differential_privacy_attributes[0].value, allowed_keys_type_names_permissions={
                'budget_delta': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'budget_epsilon': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'privacy_column': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'privacy_level': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, allowed_keys_type_names_permissions={
                'censor_dims': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'clamp_columns': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'clamp_counts': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'max_ids': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'row_privacy': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'sample_max_ids': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'tau': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'use_dpsu': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, allowed_keys_type_names_permissions={
                'synth_allowed': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        for child_node in child_nodes if child_nodes is not None else []:
            Column.verify(node=child_node, role_uuids=role_uuids)
