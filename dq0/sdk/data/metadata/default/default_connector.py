from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute import Attribute


class DefaultConnector:
    @staticmethod
    def defaultAttributesConnectorCSV():
        return [
            AttributeString(key='type_name', value='csv'),
            AttributeBoolean(key='use_original_header', value=True),
            AttributeString(key='sep', value=','),
            AttributeString(key='decimal', value='.'),
            AttributeBoolean(key='skipinitialspace', value=False),
        ]

    @staticmethod
    def defaultAttributesConnectorPostgres():
        return [
            AttributeString(key='type_name', value='postgres'),
        ]

    @staticmethod
    def getDefaultAttributesFor(type_name):
        if type_name == 'csv':
            return DefaultConnector.defaultAttributesConnectorCSV()
        if type_name == 'postgres':
            return DefaultConnector.defaultAttributesConnectorPostgres()
        return []

    @staticmethod
    def mergeDefaultAttributesWithConnectorAttribute(connector_attribute):
        if not isinstance(connector_attribute, AttributeList):
            raise Exception("connector_attribute is not of AttributeList type")
        for tmp_attribute in connector_attribute.value if connector_attribute.value is not None else []:
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("attribute is not of Attribute type")
            if tmp_attribute.key == 'type_name':
                return AttributeList(key=connector_attribute.key, value=DefaultConnector.getDefaultAttributesFor(type_name=tmp_attribute.value)).merge_with(other=connector_attribute, overwrite=True)
        return connector_attribute

    @staticmethod
    def mergeDefaultAttributesWith(attributes_list):
        if attributes_list is None:
            return None
        if not isinstance(attributes_list, list):
            raise Exception("attributes_list is not of list type")
        new_attributes_list = []
        for tmp_attribute in attributes_list if attributes_list is not None else []:
            if tmp_attribute is None:
                raise Exception("found None attribute in list")
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("found list element that is not of type Attribute")
            if tmp_attribute.key == 'connector' and tmp_attribute.value is not None and isinstance(tmp_attribute, AttributeList):
                new_attributes_list.append(DefaultConnector.mergeDefaultAttributesWithConnectorAttribute(tmp_attribute))
            else:
                new_attributes_list.append(tmp_attribute.copy())
        return new_attributes_list
