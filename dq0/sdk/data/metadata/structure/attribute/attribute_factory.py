from datetime import datetime

from dq0.sdk.data.metadata.structure.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.structure.attribute.attribute_datetime import AttributeDatetime
from dq0.sdk.data.metadata.structure.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.structure.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.permissions.permissions_factory import PermissionsFactory


class AttributeFactory:
    ATTRIBUTE_YAML_TYPE_LIST = "yaml_list"
    ATTRIBUTE_YAML_TYPE_SIMPLE = "yaml_simple"

    @staticmethod
    def verify_yaml_dict(yaml_dict):
        if not isinstance(yaml_dict, dict):
            raise Exception(f"yaml_dict is not of type dict, is of type {type(yaml_dict)} instead")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not AttributeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name}")
        if 'key' not in yaml_dict and 'value' not in yaml_dict:
            raise Exception("missing both key and value, one is required")

    @staticmethod
    def from_yaml_dict(yaml_dict):
        AttributeFactory.verify_yaml_dict(yaml_dict=yaml_dict)
        type_name = yaml_dict.pop('type_name', None)
        key = yaml_dict.pop('key', None)
        value = yaml_dict.pop('value', None)
        permissions_dict = yaml_dict.pop('permissions', None)
        permissions = PermissionsFactory.from_yaml_dict(yaml_dict=permissions_dict) if permissions_dict is not None else None
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            return AttributeBoolean(key=key, value=value, permissions=permissions)
        if type_name == AttributeType.TYPE_NAME_DATETIME:
            return AttributeDatetime(key=key, value=value, permissions=permissions)
        if type_name == AttributeType.TYPE_NAME_FLOAT:
            return AttributeFloat(key=key, value=value, permissions=permissions)
        if type_name == AttributeType.TYPE_NAME_INT:
            return AttributeInt(key=key, value=value, permissions=permissions)
        if type_name == AttributeType.TYPE_NAME_LIST:
            return AttributeList(key=key, value=[AttributeFactory.from_yaml_dict(yaml_dict=tmp_yaml_dict) for tmp_yaml_dict in value]
                                 if value is not None else None, permissions=permissions)
        if type_name == AttributeType.TYPE_NAME_STRING:
            return AttributeString(key=key, value=value, permissions=permissions)
        raise Exception(f"no factory function configured for type_name {type_name}")

    @staticmethod
    def get_type(yaml_simple_value):
        if yaml_simple_value is None:
            type_name = None
        elif isinstance(yaml_simple_value, bool):
            type_name = AttributeType.TYPE_NAME_BOOLEAN
        elif isinstance(yaml_simple_value, datetime):
            type_name = AttributeType.TYPE_NAME_DATETIME
        elif isinstance(yaml_simple_value, dict):
            type_name = AttributeType.TYPE_NAME_LIST
        elif isinstance(yaml_simple_value, float):
            type_name = AttributeType.TYPE_NAME_FLOAT
        elif isinstance(yaml_simple_value, int):
            type_name = AttributeType.TYPE_NAME_INT
        elif isinstance(yaml_simple_value, list):
            type_name = AttributeType.TYPE_NAME_LIST
        elif isinstance(yaml_simple_value, str):
            type_name = AttributeType.TYPE_NAME_STRING
        else:
            raise Exception(f"yaml_simple_value is of unknown type {type(yaml_simple_value)}")
        return type_name

    @staticmethod
    def verify_yaml_simple_and_get_type(yaml_simple_key, yaml_simple_value):
        if yaml_simple_key is not None and not isinstance(yaml_simple_key, str):
            raise Exception(f"yaml_simple_key is not of string type, is of type {type(yaml_simple_key)} instead")
        if yaml_simple_value is None:
            raise Exception("yaml_simple_value is None")
        type_name = AttributeFactory.get_type(yaml_simple_value=yaml_simple_value)
        if not AttributeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name}")
        if yaml_simple_key is None and yaml_simple_value is None:
            raise Exception("missing both key and value, one is required")
        return type_name

    @staticmethod
    def from_yaml_simple(yaml_simple_key, yaml_simple_value):
        type_name = AttributeFactory.verify_yaml_simple_and_get_type(yaml_simple_key=yaml_simple_key, yaml_simple_value=yaml_simple_value)
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            return AttributeBoolean(key=yaml_simple_key, value=yaml_simple_value, permissions=None)
        if type_name == AttributeType.TYPE_NAME_DATETIME:
            return AttributeDatetime(key=yaml_simple_key, value=yaml_simple_value, permissions=None)
        if type_name == AttributeType.TYPE_NAME_FLOAT:
            return AttributeFloat(key=yaml_simple_key, value=yaml_simple_value, permissions=None)
        if type_name == AttributeType.TYPE_NAME_INT:
            return AttributeInt(key=yaml_simple_key, value=yaml_simple_value, permissions=None)
        if type_name == AttributeType.TYPE_NAME_LIST:
            if isinstance(yaml_simple_value, dict):
                attribute_list = [AttributeFactory.from_yaml_simple(yaml_simple_key=tmp_key, yaml_simple_value=tmp_value)
                                  for tmp_key, tmp_value in yaml_simple_value.items()]
                if yaml_simple_key is None:
                    return attribute_list
                return AttributeList(key=yaml_simple_key, value=attribute_list, permissions=None)
            if isinstance(yaml_simple_value, list):
                return AttributeList(yaml_simple_key, [AttributeFactory.from_yaml_simple(yaml_simple_key=None, yaml_simple_value=tmp_value)
                                                       for tmp_value in yaml_simple_value])
            raise Exception(f"yaml_simple_value is of unknown type {type(yaml_simple_value)}")
        if type_name == AttributeType.TYPE_NAME_STRING:
            return AttributeString(yaml_simple_key, yaml_simple_value, permissions=None)
        raise Exception(f"no factory function configured for type_name {type_name}")
