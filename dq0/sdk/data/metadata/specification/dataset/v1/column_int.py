from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


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
