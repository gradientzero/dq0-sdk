from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.interface.dataset.attribute_utils import AttributeUtils
from dq0.sdk.data.metadata.interface.dataset.entity import Entity
from dq0.sdk.data.metadata.permissions.permissions import Permissions


class AttributesGroup:
    def __init__(self, key, permissions, entity, attribute_list=None):
        if key is not None and not isinstance(key, str):
            raise Exception(f"key {key} is not of type str, is of type {type(key)} instead")
        Permissions.check(permissions=permissions)
        if not isinstance(entity, Entity):
            raise Exception(f"entity is not of type Entity, is of type {type(entity)} instead")
        self.key = key
        self.permissions = permissions
        self.entity = entity
        self.attribute_list = attribute_list
        if attribute_list is not None:
            if not isinstance(attribute_list, AttributeList):
                raise Exception("attribute_list is not of type AttributeList, "
                                f"is of type {type(attribute_list)} instead")
            if key != attribute_list.key:
                raise Exception(f"keys do not match: {key} != {attribute_list.key}")

    def is_empty(self):
        return self.attribute_list is None

    def delete(self):
        if len(self.attribute_list.value) != 0:
            keys = set()
            for attribute in self.attribute_list.value:
                keys.add(attribute.key)
            for key in keys:
                self.delete_attribute(key=key)

    def wipe(self):
        self.attribute_list = None

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
                self.entity.add_attribute(attribute=attribute_list)
                self.attribute_list = attribute_list
            self.attribute_list.add_attribute(attribute=AttributeUtils.attribute_from(
                type_name=type_name, key=key, value=value, permissions=permissions))
        else:
            if attribute.type_name != type_name:
                raise Exception(f"type_name mismatch: {attribute.type_name} != {type_name}")
            AttributeUtils.match_and_check(type_name=type_name, value=value)
            attribute.value = value

    def delete_attribute(self, key):
        if self.get_attribute(key=key) is not None:
            self.attribute_list.remove_attribute(key=key)
            if len(self.attribute_list.value) == 0:
                self.entity.remove_attribute(key=self.key)
                self.attribute_list = None
