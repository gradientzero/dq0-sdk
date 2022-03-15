from dq0.sdk.data.metadata.interface.attribute_utils import AttributeUtils
from dq0.sdk.data.metadata.interface.entity import Entity
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.permissions.permissions import Permissions


class AttributesGroup:
    def __init__(self, key, permissions, entity, attribute_list=None, create_attributes_group_func=None):
        if key is not None and not isinstance(key, str):
            raise Exception(f"key {key} is not of type str, is of type {type(key)} instead")
        Permissions.check(permissions=permissions)
        if not isinstance(entity, Entity) and not isinstance(entity, AttributesGroup):
            raise Exception(f"entity is neither of type Entity nor of type AttributesGroup, is of type {type(entity)} instead")
        self._entity = entity
        self._key = key
        self._permissions = permissions
        self._attribute_list = attribute_list
        if attribute_list is not None:
            if not isinstance(attribute_list, AttributeList):
                raise Exception("attribute_list is not of type AttributeList, "
                                f"is of type {type(attribute_list)} instead")
            if key != attribute_list.get_key():
                raise Exception(f"keys do not match: {key} != {attribute_list.get_key()}")
        self._create_attributes_group_func = create_attributes_group_func
        self._attribute_groups = {}

    def to_dict(self, request_uuids=set(), full=True):
        return self._attribute_list.to_dict(request_uuids=request_uuids, full=full) if self._attribute_list is not None else None

    def get_entity(self):
        return self._entity

    def get_key(self):
        return self._key

    def get_role_uuids(self):
        return self._entity.get_role_uuids()

    def is_empty(self):
        return self._attribute_list is None

    def set_attribute_list(self, new_attribute_list):
        if self._attribute_list is not None:
            raise Exception("cannot modify existing attribute list")
        self._attribute_list = new_attribute_list

    def delete(self):
        if len(self._attribute_list.get_value()) != 0:
            keys = set()
            for attribute in self._attribute_list.get_value():
                keys.add(attribute.get_key())
            for key in keys:
                self.delete_attribute(key=key)
        self.wipe()

    def wipe(self):
        self._attribute_list = None
        for attribute_group in self._attribute_groups.values():
            attribute_group.wipe()

    def get_attribute(self, key):
        return self._attribute_list.get_attribute(key=key) if self._attribute_list is not None else None

    def get_attribute_value(self, key):
        attribute = self.get_attribute(key=key)
        return attribute.get_value() if attribute is not None else None

    def set_attribute_value(self, type_name, key, value, permissions, allow_modification=True):
        attribute = self.get_attribute(key=key)
        if attribute is None:
            if self._attribute_list is None:
                attribute_list = AttributeList(key=self.get_key(), value=[], permissions=self._permissions)
                self._entity.add_attribute(attribute=attribute_list)
                self._attribute_list = attribute_list
            self._attribute_list.add_attribute(attribute=AttributeUtils.attribute_from(
                type_name=type_name, key=key, value=value, permissions=permissions))
        else:
            if not allow_modification:
                raise Exception(f"attribute {key} is already set and cannot be modified")
            if attribute.get_type_name() != type_name:
                raise Exception(f"type_name mismatch: {attribute.get_type_name()} != {type_name}")
            AttributeUtils.match_and_check(type_name=type_name, value=value)
            attribute._value = value

    def delete_attribute(self, key):
        if self.get_attribute(key=key) is not None:
            self._attribute_list.remove_attribute(key=key)
            if len(self._attribute_list.get_value()) == 0:
                self._entity.remove_attribute(key=self.get_key())
                self._attribute_list = None

    def add_attribute(self, attribute):
        attribute = self.get_attribute(key=attribute.get_key())
        if attribute is not None:
            raise Exception(f"attribute {attribute.get_key()} is already set and cannot be modified")
        if self._attribute_list is None:
            attribute_list = AttributeList(key=self.get_key(), value=[], permissions=self._permissions)
            self._entity.add_attribute(attribute=attribute_list)
            self._attribute_list = attribute_list
        self._attribute_list.add_attribute(attribute=attribute)

    def remove_attribute(self, key):
        self.delete_attribute(key=key)
        if key in self._attribute_groups:
            self._attribute_groups[key].wipe()

    def get_attribute_group(self, key):
        if key not in self._attribute_groups:
            attribute_list = self.get_attribute(key=key)
            if self._create_attributes_group_func is None:
                raise Exception("create_attributes_group_func is None")
            self._attribute_groups[key] = self._create_attributes_group_func(key=key, attribute_list=attribute_list)
        return self._attribute_groups[key]
