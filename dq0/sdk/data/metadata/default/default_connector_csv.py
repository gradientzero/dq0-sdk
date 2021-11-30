from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.default.default_permissions import DefaultPermissions


class DefaultConnectorCSV:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, allowed_keys_type_names_permissions=None)
        applied_attributes = DefaultConnectorCSV.apply_defaults_to_attributes(attributes=attribute.value, role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_attribute(role_uuids=role_uuids) if attribute.permissions is None else attribute.permissions.copy()
        return AttributeList(key=attribute.key, value=applied_attributes, permissions=applied_permissions)
    
    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions=None)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.shared_attribute(role_uuids=role_uuids))
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, allowed_keys_type_names_permissions={
            'connector': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
        })
        DefaultConnectorCSV.verify_attributes(attributes=attribute.value, role_uuids=role_uuids)
    
    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions={
            'decimal': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'header_columns': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'header_row': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'na_values': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'sep': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'skipinitialspace': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'uri': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'use_original_header': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        })
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'type_name'] if attributes is not None else []
        if len(type_name_attributes) != 1:
            raise Exception("csv connector attributes do not contain attribute type_name")
        if type_name_attributes[0].value != 'csv':
            raise Exception(f"csv connector type_name value {type_name_attributes[0].value} does not match 'csv'")
        header_columns_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'header_columns'] if attributes is not None else []
        if 0 < len(header_columns_attributes):
            Attribute.check_list(attribute_list=header_columns_attributes[0].value, allowed_keys_type_names_permissions={
                None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
        na_value_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'na_values'] if attributes is not None else []
        if 0 < len(na_value_attributes):
            Attribute.check_list(attribute_list=na_value_attributes[0].value, allowed_keys_type_names_permissions=None)
            for tmp_attribute in na_value_attributes[0].value:
                if tmp_attribute.key is None:
                    raise Exception("na_values may not have none keys")
