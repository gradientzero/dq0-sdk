from datetime import datetime

from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_datetime import AttributeDatetime
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType


class AttributeUtils:
    @staticmethod
    def attribute_from(type_name, key, value, permissions):
        attribute = None
        if type_name == AttributeType.TYPE_NAME_BOOLEAN:
            attribute = AttributeBoolean(key=key, value=value, permissions=permissions)
        elif type_name == AttributeType.TYPE_NAME_DATETIME:
            attribute = AttributeDatetime(key=key, value=value, permissions=permissions)
        elif type_name == AttributeType.TYPE_NAME_FLOAT:
            attribute = AttributeFloat(key=key, value=value, permissions=permissions)
        elif type_name == AttributeType.TYPE_NAME_INT:
            attribute = AttributeInt(key=key, value=value, permissions=permissions)
        elif type_name == AttributeType.TYPE_NAME_LIST:
            attribute = AttributeList(key=key, value=value, permissions=permissions)
        elif type_name == AttributeType.TYPE_NAME_STRING:
            attribute = AttributeString(key=key, value=value, permissions=permissions)
        else:
            raise Exception(f"unknown type_name {type_name}")
        return attribute

    @staticmethod
    def match_and_check(type_name, value):
        if type_name not in [AttributeType.TYPE_NAME_BOOLEAN,
                             AttributeType.TYPE_NAME_DATETIME,
                             AttributeType.TYPE_NAME_FLOAT,
                             AttributeType.TYPE_NAME_INT,
                             AttributeType.TYPE_NAME_LIST,
                             AttributeType.TYPE_NAME_STRING]:
            raise Exception(f"unknown type_name {type_name}")
        if type_name == AttributeType.TYPE_NAME_BOOLEAN and not isinstance(value, bool):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")
        if type_name == AttributeType.TYPE_NAME_DATETIME and not isinstance(value, datetime):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")
        if type_name == AttributeType.TYPE_NAME_FLOAT and not isinstance(value, float):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")
        if type_name == AttributeType.TYPE_NAME_INT and not isinstance(value, int):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")
        if type_name == AttributeType.TYPE_NAME_LIST and not isinstance(value, list):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")
        if type_name == AttributeType.TYPE_NAME_STRING and not isinstance(value, str):
            raise Exception(f"type_name is {type_name} but value is of type {type(value)} instead")

    @staticmethod
    def value_to_list(input_value):
        if input_value is None:
            return None
        if not isinstance(input_value, list):
            raise Exception(f"input_value {input_value} is not of type list, is of type {type(input_value)} instead")
        type_name = None
        new_list = []
        for attribute in input_value:
            if not isinstance(attribute, Attribute):
                raise Exception(f"attribute {attribute} is not of type Attribute, is of type {type(attribute)} instead")
            if attribute.key is not None:
                raise Exception(f"all keys must be none; key {attribute.key} is not None")
            if type_name is not None and type_name != attribute.type_name:
                raise Exception(f"type_name mismatch: {type_name} != {attribute.type_name}")
            type_name = attribute.type_name
            AttributeUtils.match_and_check(type_name=type_name, value=attribute.value)
            if type_name == AttributeType.TYPE_NAME_LIST:
                raise Exception("list may not contain attribute values of list type")
            new_list.append(attribute.value)
        return new_list

    @staticmethod
    def list_to_value(input_list, type_name, permissions=None):
        if not isinstance(input_list, list):
            raise Exception(f"input_list {input_list} is not of type list, is of type {type(input_list)} instead")
        new_list = []
        for element in input_list:
            AttributeUtils.match_and_check(type_name=type_name, value=element)
            if type_name == AttributeType.TYPE_NAME_BOOLEAN:
                new_list.append(AttributeBoolean(key=None, value=element, permissions=permissions))
            elif type_name == AttributeType.TYPE_NAME_DATETIME:
                new_list.append(AttributeDatetime(key=None, value=element, permissions=permissions))
            elif type_name == AttributeType.TYPE_NAME_FLOAT:
                new_list.append(AttributeFloat(key=None, value=element, permissions=permissions))
            elif type_name == AttributeType.TYPE_NAME_INT:
                new_list.append(AttributeInt(key=None, value=element, permissions=permissions))
            elif type_name == AttributeType.TYPE_NAME_LIST:
                raise Exception("list may not contain elements of list type")
            elif type_name == AttributeType.TYPE_NAME_STRING:
                new_list.append(AttributeString(key=None, value=element, permissions=permissions))
            else:
                raise Exception(f"unknown type_name {type_name}")
        return new_list

    @staticmethod
    def value_to_dict(input_value):
        if input_value is None:
            return None
        if not isinstance(input_value, dict):
            raise Exception(f"input_value {input_value} is not of type dict, is of type {type(input_value)} instead")
        type_name = None
        new_dict = {}
        for attribute in input_value:
            if not isinstance(attribute, Attribute):
                raise Exception(f"attribute {attribute} is not of type Attribute, is of type {type(attribute)} instead")
            if attribute.key in new_dict:
                raise Exception(f"all keys must be unique; key {attribute.key} is already present")
            if type_name is not None and type_name != attribute.type_name:
                raise Exception(f"type_name mismatch: {type_name} != {attribute.type_name}")
            type_name = attribute.type_name
            AttributeUtils.match_and_check(type_name=type_name, value=attribute.value)
            if type_name == AttributeType.TYPE_NAME_LIST:
                raise Exception("list may not contain attribute values of list type")
            new_dict[attribute.key] = attribute.value
        return new_dict

    @staticmethod
    def dict_to_value(input_dict, type_name=None, permissions=None):
        if not isinstance(input_dict, dict):
            raise Exception(f"input_dict {input_dict} is not of type dict, is of type {type(input_dict)} instead")
        new_list = []
        for key, element in input_dict.items():
            if type_name is not None:
                AttributeUtils.match_and_check(type_name=type_name, value=element)
            if isinstance(element, bool):
                new_list.append(AttributeBoolean(key=key, value=element, permissions=permissions))
            elif isinstance(element, datetime):
                new_list.append(AttributeDatetime(key=key, value=element, permissions=permissions))
            elif isinstance(element, float):
                new_list.append(AttributeFloat(key=key, value=element, permissions=permissions))
            elif isinstance(element, int):
                new_list.append(AttributeInt(key=key, value=element, permissions=permissions))
            elif isinstance(element, list):
                raise Exception("list may not contain elements of list type")
            elif isinstance(element, str):
                new_list.append(AttributeString(key=key, value=element, permissions=permissions))
            else:
                raise Exception(f"element {element} is of unknown type {type(element)}")
        return new_list
