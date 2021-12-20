from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.node.node import Node
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Column:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Column.apply_defaults_to_attributes(attributes=node.attributes, role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_node(role_uuids=role_uuids) if node.permissions is None else node.permissions.copy()
        return Node(type_name=node.type_name, attributes=applied_attributes, child_nodes=None, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            if applied_attribute.key in ['differential_privacy', 'private_sql', 'private_sql_and_synthesis', 'private_synthesis']:
                applied_attribute.set_default_permissions(default_permissions=owner_attribute)
            else:
                if applied_attribute.key == 'machine_learning':
                    for sub_attribute in applied_attribute.value if applied_attribute.value is not None else []:
                        sub_attribute.set_default_permissions(default_permissions=analyst_attribute)
                applied_attribute.set_default_permissions(default_permissions=shared_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_COLUMN], allowed_permissions=DefaultPermissions.shared_node(role_uuids=role_uuids))
        Column.verify_attributes(attributes=node.attributes, role_uuids=role_uuids)
        Column.verify_child_nodes(child_nodes=node.child_nodes, role_uuids=role_uuids)

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
        data_type_name = None
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
            data_type_name_attributes = [tmp_attribute for tmp_attribute in data_attributes[0].value if tmp_attribute.key == 'data_type_name'] \
                if data_attributes[0].value is not None else []
            if 0 < len(data_type_name_attributes):
                data_type_name = data_type_name_attributes[0].value
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [tmp_attribute for tmp_attribute in private_sql_attributes[0].value if tmp_attribute.key == 'allowed_values'] \
                if private_sql_attributes[0].value is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].value, check_data={
                    None: ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_STRING],
                           owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].value, check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_DATETIME, AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'min_step': ([AttributeType.TYPE_NAME_FLOAT, AttributeType.TYPE_NAME_INT], owner_attribute),
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })
        if data_type_name is None:
            raise Exception("attribute data_type_name is missing in column")
        if data_type_name == 'boolean':
            Column.verify_attributes_boolean(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'datetime':
            Column.verify_attributes_datetime(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'float':
            Column.verify_attributes_float(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'int':
            Column.verify_attributes_int(attributes=attributes, role_uuids=role_uuids)
        elif data_type_name == 'string':
            Column.verify_attributes_string(attributes=attributes, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown data_type_name {data_type_name}")

    @staticmethod
    def verify_attributes_boolean(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'private_sql': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'private_synthesis': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
            'machine_learning': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
        }, required_keys={'data'})
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_attributes_datetime(attributes, role_uuids=None):
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
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_DATETIME], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_DATETIME], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [tmp_attribute for tmp_attribute in private_sql_attributes[0].value if tmp_attribute.key == 'allowed_values'] \
                if private_sql_attributes[0].value is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].value, check_data={
                    None: ([AttributeType.TYPE_NAME_DATETIME], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].value, check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_DATETIME], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_DATETIME], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_attributes_float(attributes, role_uuids=None):
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
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [tmp_attribute for tmp_attribute in private_sql_attributes[0].value if tmp_attribute.key == 'allowed_values'] \
                if private_sql_attributes[0].value is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].value, check_data={
                    None: ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].value, check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'discrete': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'min_step': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_attributes_int(attributes, role_uuids=None):
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
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'differential_privacy_sql'] \
            if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'auto_bounds_prob': ([AttributeType.TYPE_NAME_FLOAT], owner_attribute),
                'auto_lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'auto_upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'use_auto_bounds': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [tmp_attribute for tmp_attribute in private_sql_attributes[0].value if tmp_attribute.key == 'allowed_values'] \
                if private_sql_attributes[0].value is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].value, check_data={
                    None: ([AttributeType.TYPE_NAME_INT], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].value, check_data={
                'bounded': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'lower': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'upper': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'min_step': ([AttributeType.TYPE_NAME_INT], owner_attribute),
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_attributes_string(attributes, role_uuids=None):
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
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'data'] if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].value, check_data={
                'data_type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'description': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'metadata_is_public': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
                'selectable': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            }, required_keys={'data_type_name', 'name'})
        private_sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql'] if attributes is not None else []
        if 0 < len(private_sql_attributes):
            Attribute.check_list(attribute_list=private_sql_attributes[0].value, check_data={
                'allowed_values': ([AttributeType.TYPE_NAME_LIST], owner_attribute),
                'mask': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                'private_id': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
            allowed_values_attributes = [tmp_attribute for tmp_attribute in private_sql_attributes[0].value if tmp_attribute.key == 'allowed_values'] \
                if private_sql_attributes[0].value is not None else []
            if 0 < len(allowed_values_attributes):
                Attribute.check_list(attribute_list=allowed_values_attributes[0].value, check_data={
                    None: ([AttributeType.TYPE_NAME_STRING], owner_attribute),
                })
        private_sql_and_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_sql_and_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_sql_and_synthesis_attributes):
            Attribute.check_list(attribute_list=private_sql_and_synthesis_attributes[0].value, check_data={
                'cardinality': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            })
        private_synthesis_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'private_synthesis'] \
            if attributes is not None else []
        if 0 < len(private_synthesis_attributes):
            Attribute.check_list(attribute_list=private_synthesis_attributes[0].value, check_data={
                'synthesizable': ([AttributeType.TYPE_NAME_BOOLEAN], owner_attribute),
            })
        machine_learning_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'machine_learning'] \
            if attributes is not None else []
        if 0 < len(machine_learning_attributes):
            Attribute.check_list(attribute_list=machine_learning_attributes[0].value, check_data={
                'is_feature': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
                'is_target': ([AttributeType.TYPE_NAME_BOOLEAN], analyst_attribute),
            })

    @staticmethod
    def verify_child_nodes(child_nodes, role_uuids=None):
        if child_nodes is not None:
            raise Exception("child_nodes is not none")
