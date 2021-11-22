from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.default.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType


class DefaultColumn:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = DefaultColumn.apply_defaults_to_attributes(attributes=node.attributes, role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_node(role_uuids=role_uuids) if node.permissions is None else node.permissions.copy()
        return Node(type_name=node.type_name, attributes=applied_attributes, child_nodes=None, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions=None)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            if applied_attribute.key in ['auto_bounds_prob', 'auto_lower', 'auto_upper', 'cardinality', 'lower', 'mask', 'upper']:
                applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.owner_attribute(role_uuids=role_uuids))
            else:
                applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.shared_attribute(role_uuids=role_uuids))
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_COLUMN], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        DefaultColumn.verify_attributes(attributes=node.attributes, role_uuids=role_uuids)
        DefaultColumn.verify_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            # Owner exclusive
            'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            'auto_lower': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            'auto_upper': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            'lower': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'upper': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            # Shared (User may read)
            'allowed_values': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'bounding': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'machine_learning': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'min_step': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], shared_attribute),
            'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })
        allowed_values_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'allowed_values'] if attributes is not None else []
        if 0 < len(allowed_values_attributes):
            Attribute.check_list(attribute_list=allowed_values_attributes[0].value, allowed_keys_type_names_permissions={
                None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
        bounding_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'bounding'] if attributes is not None else []
        if 0 < len(bounding_attributes):
            Attribute.check_list(attribute_list=bounding_attributes[0].value, allowed_keys_type_names_permissions={
                # Owner exclusive
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                # Shared (User may read)
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, allowed_keys_type_names_permissions={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            })
        data_type_name = None
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, allowed_keys_type_names_permissions={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'min_step': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], shared_attribute),
            })
            data_type_name_attributes = [tmp_attribute for tmp_attribute in data_attributes[0].value if tmp_attribute.key == 'data_type_name'] if data_attributes[0].value is not None else []
            if 0 < len(data_type_name_attributes):
                data_type_name = data_type_name_attributes[0].value
        data_type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data_type_name'] if attributes is not None else []
        if 0 < len(data_type_name_attributes):
            data_type_name = data_type_name_attributes[0].value 
        if data_type_name is None:
            raise Exception("attribute data_type_name is missing in column")
        if data_type_name == 'boolean' or data_type_name == 'datetime':
            DefaultColumn.verify_attributes_boolean_datetime(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'float':
            DefaultColumn.verify_attributes_float(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'int':
            DefaultColumn.verify_attributes_int(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'string':
            DefaultColumn.verify_attributes_string(attributes=attributes, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown data_type_name {data_type_name}")

    @staticmethod
    def verify_attributes_boolean_datetime(attributes, role_uuids=None):
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })

    @staticmethod
    def verify_attributes_float(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            # Owner exclusive
            'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            'auto_lower': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            'auto_upper': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            'lower': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            'upper': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            # Shared (User may read)
            'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'min_step': ([AttributeType.TYPE_NAME_FLOAT], shared_attribute),
            'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })

    @staticmethod
    def verify_attributes_int(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            'bounding': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'machine_learning': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })
        bounding_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'bounding'] if attributes is not None else []
        if 0 < len(bounding_attributes):
            Attribute.check_list(attribute_list=bounding_attributes[0].value, allowed_keys_type_names_permissions={
                # Owner exclusive
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                # Shared (User may read)
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            })
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, allowed_keys_type_names_permissions={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'min_step': ([AttributeType.TYPE_NAME_INT], shared_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, allowed_keys_type_names_permissions={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            })

    @staticmethod
    def verify_attributes_string(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            # Owner exclusive
            'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            # Shared (User may read)
            'allowed_values': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })
        allowed_values_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'allowed_values'] if attributes is not None else []
        if 0 < len(allowed_values_attributes):
            Attribute.check_list(attribute_list=allowed_values_attributes[0].value, allowed_keys_type_names_permissions={
                None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            })

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        if child_nodes is not None:
            raise Exception("child_nodes is not none")
