from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class ConnectorPostgreSQL:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        applied_attributes = ConnectorPostgreSQL.apply_defaults_to_attributes(attributes=attribute.value, role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_attribute(role_uuids=role_uuids) if attribute.permissions is None else attribute.permissions.copy()
        return AttributeList(key=attribute.key, value=applied_attributes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.shared_attribute(role_uuids=role_uuids))
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'connector': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
        })
        ConnectorPostgreSQL.verify_attributes(attributes=attribute.value, role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'host': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'password': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'port': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            'type_name': ([AttributeType.TYPE_NAME_STRING], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
            'username': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
        }, required_keys={'type_name'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.key == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].value != 'postgresql':
            raise Exception(f"postgresql connector type_name value {type_name_attributes[0].value} does not match 'postgresql'")
