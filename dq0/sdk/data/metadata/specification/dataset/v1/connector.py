from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.dataset.v1.connector_csv import ConnectorCSV
from dq0.sdk.data.metadata.specification.dataset.v1.connector_postgresql import ConnectorPostgreSQL
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions


class Connector:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        if attribute.type_name != AttributeType.TYPE_NAME_LIST:
            raise Exception(f"attribute is not of type {AttributeType.TYPE_NAME_LIST}, is of type {attribute.type_name} instead")
        attribute_type_name = attribute.get_attribute(key='type_name')
        if not isinstance(attribute_type_name, AttributeString):
            raise Exception(f"attribute type_name is not of type AttributeString, is of type {type(attribute_type_name)} instead")
        if attribute_type_name.value == 'csv':
            return ConnectorCSV.apply_defaults(attribute=attribute, role_uuids=role_uuids)
        elif attribute_type_name.value == 'postgresql':
            return ConnectorPostgreSQL.apply_defaults(attribute=attribute, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown connector type_name {attribute_type_name.value}")

    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'connector': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
        })
        attribute_type_name = attribute.get_attribute(key='type_name')
        if not isinstance(attribute_type_name, AttributeString):
            raise Exception(f"attribute type_name is not of type AttributeString, is of type {type(attribute_type_name)} instead")
        if attribute_type_name.value == 'csv':
            return ConnectorCSV.verify(attribute=attribute, role_uuids=role_uuids)
        elif attribute_type_name.value == 'postgresql':
            return ConnectorPostgreSQL.verify(attribute=attribute, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown connector type_name {attribute_type_name.value}")
