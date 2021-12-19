from datetime import datetime
from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_datetime import AttributeDatetime
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.interface.dataset.standard.column import Column
from dq0.sdk.data.metadata.permissions.permissions import Permissions


class AttributesGroup:
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

    def __init__(self, key, permissions, column, attribute_list=None):
        if key is not None and not isinstance(key, str):
            raise Exception(f"key {key} is not of type str, is of type {type(key)} instead")
        Permissions.check(permissions=permissions)
        if not isinstance(column, Column):
            raise Exception(f"column is not of type Column, is of type {type(column)} instead")
        self.key = key
        self.permissions = permissions
        self.column = column
        self.attribute_list = attribute_list
        if attribute_list is not None:
            if not isinstance(attribute_list, AttributeList):
                raise Exception("attribute_list is not of type AttributeList, "
                                f"is of type {type(attribute_list)} instead")
            if key != attribute_list.key:
                raise Exception(f"keys do not match: {key} != {attribute_list.key}")

    def get_attribute(self, key):
        return self.attribute_list.get_attribute(key=key) if self.attribute_list is not None else None

    def get_attribute_value(self, key):
        attribute = self.attribute_list.get_attribute(key=key) if self.attribute_list is not None else None
        return attribute.value if attribute is not None else None

    def set_attribute_value(self, type_name, key, value, permissions):
        attribute = self.get_attribute(key=key)
        if attribute is None:
            if self.attribute_list is None:
                attribute_list = AttributeList(key=self.key, value=[], permissions=self.permissions)
                self.column.add_attribute(attribute=attribute_list)
                self.attribute_list = attribute_list
            self.attribute_list.add_attribute(attribute=AttributesGroup.attribute_from(
                type_name=type_name, key=key, value=value, permissions=permissions))
        else:
            if attribute.type_name != type_name:
                raise Exception(f"type_name mismatch: {attribute.type_name} != {type_name}")
            AttributesGroup.match_and_check(type_name=type_name, value=value)
            attribute.value = value

    def delete_attribute(self, key):
        if self.get_attribute(key=key) is not None:
            self.attribute_list.remove_attribute(key=key)
            if len(self.attribute_list.value) == 0:
                self.column.remove_attribute(key=self.key)
                self.attribute_list = None
