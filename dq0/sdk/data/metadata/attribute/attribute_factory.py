from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_datetime import AttributeDatetime
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_node import AttributeNode
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType


class AttributeFactory:
    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not AttributeType.isValidTypeName(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")
        if 'key' not in yaml_dict:
            raise Exception("missing key")
        if 'value' not in yaml_dict:
            raise Exception("missing value")
 
    @staticmethod
    def fromYamlDict(yaml_dict):
        AttributeFactory.verifyYamlDict(yaml_dict=yaml_dict)
        type_name = yaml_dict.pop('type_name', None)
        key = yaml_dict.pop('key', None)
        value = yaml_dict.pop('value', None)
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            return AttributeBoolean(key, value)
        if type_name == AttributeType.TYPE_NAME_DATETIME:
            return AttributeDatetime(key, value)
        if type_name == AttributeType.TYPE_NAME_FLOAT:
            return AttributeFloat(key, value)
        if type_name == AttributeType.TYPE_NAME_INT:
            return AttributeInt(key, value)
        if type_name == AttributeType.TYPE_NAME_LIST:
            return AttributeList(key, value)
        if type_name == AttributeType.TYPE_NAME_NODE:
            return AttributeNode(key, value)
        if type_name == AttributeType.TYPE_NAME_STRING:
            return AttributeString(key, value)
        raise Exception(f"no factory function configured for type_name {type_name if type_name is not None else 'None'}")
