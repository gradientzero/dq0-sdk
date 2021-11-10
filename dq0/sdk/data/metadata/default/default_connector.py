from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils


class DefaultConnector:
    @staticmethod
    def default_attributes_connector_csv():
        return [
            AttributeString(key='type_name', value='csv', user_uuids=None, role_uuids=None),
            AttributeBoolean(key='use_original_header', value=True, user_uuids=None, role_uuids=None),
            AttributeString(key='sep', value=',', user_uuids=None, role_uuids=None),
            AttributeString(key='decimal', value='.', user_uuids=None, role_uuids=None),
            AttributeBoolean(key='skipinitialspace', value=False, user_uuids=None, role_uuids=None),
        ]

    @staticmethod
    def default_attributes_connector_postgres():
        return [
            AttributeString(key='type_name', value='postgres', user_uuids=None, role_uuids=None),
        ]

    @staticmethod
    def get_default_attributes_for(type_name):
        if type_name == 'csv':
            return DefaultConnector.default_attributes_connector_csv()
        if type_name == 'postgres':
            return DefaultConnector.default_attributes_connector_postgres()
        return []

    @staticmethod
    def merge_default_attributes_with_connector_attribute(connector_attribute):
        if not isinstance(connector_attribute, AttributeList):
            raise Exception("connector_attribute is not of AttributeList type")
        for tmp_attribute in connector_attribute.value if connector_attribute.value is not None else []:
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("attribute is not of Attribute type")
            if tmp_attribute.key == 'type_name':
                return AttributeList(key=connector_attribute.key, value=DefaultConnector.get_default_attributes_for(type_name=tmp_attribute.value), user_uuids=None, role_uuids=None).merge_with(other=connector_attribute, overwrite=True)
        return connector_attribute

    @staticmethod
    def merge_default_attributes_with(attributes_list):
        if attributes_list is None:
            return None
        if not isinstance(attributes_list, list):
            raise Exception(f"attributes_list is not of type list, is of type {type(attributes_list)} instead")
        new_attributes_list = []
        for tmp_attribute in attributes_list if attributes_list is not None else []:
            if tmp_attribute is None:
                raise Exception("found None attribute in list")
            if not isinstance(tmp_attribute, Attribute):
                raise Exception(f"list element is not of type Attribute, is of type {type(tmp_attribute)} instead")
            if tmp_attribute.key == 'connector' and tmp_attribute.value is not None and isinstance(tmp_attribute, AttributeList):
                new_attributes_list.append(DefaultConnector.merge_default_attributes_with_connector_attribute(tmp_attribute))
            else:
                new_attributes_list.append(tmp_attribute.copy())
        return new_attributes_list
