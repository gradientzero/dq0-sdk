from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils.list_utils import ListUtils
from dq0.sdk.data.metadata.utils.str_utils import StrUtils


class AttributeList(Attribute):
    def __init__(self, key, value, permissions=None):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key, permissions=permissions)
        if not isinstance(value, list):
            raise Exception(f"value {value} is not of type list, is of type {type(value)} instead")
        self._is_explicit_list = Attribute.check_list(attribute_list=value, check_data=None)
        for tmp_attribute in value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=self._is_explicit_list)
        self._value = value

    def __str__(self, request_uuids=set()):
        super_str = super().__str__(request_uuids=request_uuids)
        if super_str is None:
            return None
        return super_str + StrUtils.restricted_str_from_list(list=self.get_value(), sort=False, request_uuids=request_uuids).replace('\n', "\n  ")

    def __repr__(self):
        return "AttributeList(" + \
            "key=" + repr(self.get_key()) + ", " + \
            "value=" + repr(self.get_value()) + ", " + \
            "permissions=" + repr(self.get_permissions()) + ')'

    def __eq__(self, other):
        if not isinstance(other, AttributeList) or not super().__eq__(other=other):
            return False
        return ListUtils.list_equals_unordered(list_a=self.get_value(), list_b=other.get_value())

    def get_value(self):
        return self._value

    def copy(self):
        copied_attribute = AttributeList(
            key=self.get_key(),
            value=[tmp_attribute.copy() for tmp_attribute in self.get_value()] if self.get_value() is not None else None,
            permissions=self.get_permissions().copy() if self.get_permissions() is not None else None
        )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element())
        return copied_attribute

    def to_dict(self, request_uuids=set()):
        super_dict = super().to_dict(request_uuids=request_uuids)
        if super_dict is None:
            return None
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('value', ListUtils.list_map_to_dict(self.get_value(), request_uuids=request_uuids)),
        ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def to_list(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        if not self._is_explicit_list:
            return None
        value_list = []
        for elem in self.get_value() if self.get_value() is not None else []:
            if elem is None or isinstance(elem, AttributeList):
                continue
            value_list.append(elem.get_value())
        if len(value_list) == 0:
            return None
        return value_list

    def is_merge_compatible_with(self, other, explanation=None):
        if not super().is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_merge_compatible_with(...): super() is not compatible")
            return False
        if not Attribute.are_merge_compatible(attribute_list_a=self.get_value(), attribute_list_b=other.get_value(), explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_merge_compatible_with(...): attributes are not compatible")
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_mergeable_with(...): not merge compatible")
            return False
        if not super().is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                         request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_mergeable_with(...): super() is not mergeable")
            return False
        if not Attribute.are_mergeable(attribute_list_a=self.get_value(), attribute_list_b=other.get_value(),
                                       overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                       request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_mergeable_with(...): attributes are not mergeable")
            return False
        merged_attributes = Attribute.merge_many(attribute_list_a=self.get_value(), attribute_list_b=other.get_value(),
                                                 overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                                 request_uuids=request_uuids)
        if self.get_value() != merged_attributes and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_VALUE,
                                                                                     request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message="AttributeList.is_mergeable_with(...): value differs without write_value permissions")
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                      request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged._value = Attribute.merge_many(attribute_list_a=self.get_value(), attribute_list_b=other.get_value(), overwrite_permissions=overwrite_permissions,
                                             request_uuids=request_uuids)
        merged._is_explicit_list = Attribute.check_list(attribute_list=merged.get_value(), check_data=None)
        for tmp_attribute in merged.get_value():
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=merged._is_explicit_list)
        merged._permissions = Permissions.merge(permissions_a=self.get_permissions(), permissions_b=other.get_permissions(), overwrite=overwrite_permissions)
        return merged

    def set_default_permissions(self, default_permissions=None):
        Permissions.check(permissions=default_permissions)
        if self.get_permissions() is None:
            self._permissions = default_permissions
        for attribute in self.get_value() if self.get_value() is not None else []:
            attribute.set_default_permissions(default_permissions=default_permissions)

    def get_attribute(self, index=-1, key=None, value=None, default=None):
        if index < 0 and key is None and value is None:
            return default
        for tmp_index, tmp_attribute in enumerate(self.get_value() if self.get_value() is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.get_key()) and (value is None or value == tmp_attribute.get_value()):
                return tmp_attribute
        return default

    def add_attribute(self, attribute, index=-1):
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(index=index, key=attribute.get_key(), value=attribute.get_value()) is not None:
            raise Exception("duplicate attributes not allowed")
        if self.get_value() is None:
            self._value = []
        self._is_explicit_list = Attribute.check_list(attribute_list=self.get_value(), check_data=None)
        if index < 0:
            index = len(self.get_value())
        self.get_value().insert(index, attribute)
        for tmp_attribute in self.get_value():
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=self._is_explicit_list)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self.get_value() if self.get_value() is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.get_key()) and (value is None or value == tmp_attribute.get_value()):
                del self.get_value()[tmp_index]
                self._is_explicit_list = Attribute.check_list(attribute_list=self.get_value(), check_data=None)
                for tmp_attribute in self.get_value():
                    tmp_attribute.set_explicit_list_element(is_explicit_list_element=self._is_explicit_list)
                return
        raise Exception("attribute not found")
