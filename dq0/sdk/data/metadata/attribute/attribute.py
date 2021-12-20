from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils.str_utils import StrUtils


class Attribute:
    @staticmethod
    def check(attribute, check_data=None):
        if not isinstance(attribute, Attribute):
            raise Exception(f"attribute is not of type Attribute, is of type {type(attribute)} instead")
        if check_data is not None:
            if attribute.key not in check_data:
                raise Exception(f"attribute.key {attribute.key} is not in allowed keys {check_data.keys()}")
            allowed_type_names, allowed_permissions = check_data[attribute.key]
            if allowed_type_names is not None and attribute.type_name not in allowed_type_names:
                raise Exception(f"attribute.type_name {attribute.type_name} is not in allowed_type_names {allowed_type_names}")
            if not Permissions.is_subset_of(permissions_a=attribute.permissions, permissions_b=allowed_permissions):
                raise Exception("attribute.permissions" + f"{attribute.permissions}" + "\nare not in allowed_permissions" + f"{allowed_permissions}")

    @staticmethod
    def check_list(attribute_list, check_data=None, required_keys=None):
        if attribute_list is None:
            return
        if not isinstance(attribute_list, list):
            raise Exception(f"attribute_list is not of type list, is of type {type(attribute_list)} instead")
        keys = set()
        none_key_count = 0
        regular_key_count = 0
        for attribute in attribute_list:
            Attribute.check(attribute=attribute, check_data=check_data)
            if attribute.key is None:
                none_key_count += 1
            else:
                if attribute.key in keys:
                    raise Exception(f"duplicate attribute key {attribute.key} is not allowed")
                keys.add(attribute.key)
                regular_key_count += 1
        for required_key in required_keys if required_keys is not None else set():
            if required_key not in keys:
                raise Exception(f"required_key {required_key} is not in the list")
        if 0 < regular_key_count and 1 < none_key_count:
            raise Exception(f"may only have single none (null) key in list with regular keys, "
                            f"there is {regular_key_count} regular key(s) and {none_key_count} none key(s)")
        return regular_key_count == 0 and 0 < none_key_count

    @staticmethod
    def are_merge_compatible(attribute_list_a, attribute_list_b, explanation=None):
        if attribute_list_a is None or len(attribute_list_a) == 0 or attribute_list_b is None or len(attribute_list_b) == 0:
            return True
        _ = Attribute.check_list(attribute_list=attribute_list_a, check_data=None)
        _ = Attribute.check_list(attribute_list=attribute_list_b, check_data=None)
        for attribute_a in attribute_list_a:
            for attribute_b in attribute_list_b:
                if attribute_a.key == attribute_b.key and not attribute_a.is_merge_compatible_with(other=attribute_b, explanation=explanation):
                    Explanation.dynamic_add_message(explanation=explanation,
                                                    message=f"Attribute.are_merge_compatible(...): attributes[{attribute_a.type_name}] "
                                                    f"with matching key {attribute_a.key} are not compatible")
                    return False
        return True

    @staticmethod
    def are_mergeable(attribute_list_a, attribute_list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not Attribute.are_merge_compatible(attribute_list_a=attribute_list_a, attribute_list_b=attribute_list_b, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message="Attribute.are_mergeable(...): attributes are not compatible")
            return False
        if attribute_list_a is None or len(attribute_list_a) == 0 or attribute_list_b is None or len(attribute_list_b) == 0:
            return True
        for elem_a in attribute_list_a:
            found_match = False
            for elem_b in attribute_list_b:
                if elem_a.is_merge_compatible_with(other=elem_b, explanation=None):
                    if not elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                                    request_uuids=request_uuids, explanation=explanation):
                        Explanation.dynamic_add_message(explanation=explanation,
                                                        message=f"Attribute.are_mergeable(...): compatible attributes[{elem_a.type_name}] "
                                                        f"with key {elem_a.key} are not mergeable")
                        return False
                    else:
                        if found_match:
                            Explanation.dynamic_add_message(explanation=explanation,
                                                            message=f"Attribute.are_mergeable(...): duplicate mergeable attributes[{elem_a.type_name}] "
                                                            f"with key {elem_a.key} are not allowed")
                            return False
                        found_match = True
        return True

    @staticmethod
    def merge_many(attribute_list_a, attribute_list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not Attribute.are_mergeable(attribute_list_a=attribute_list_a, attribute_list_b=attribute_list_b,
                                       overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                       request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attribute lists that are not mergeable; list_a: {attribute_list_a} list_b: {attribute_list_b} "
                                 f"explanation: {explanation}")
        if attribute_list_a is None or len(attribute_list_a) == 0:
            return None if attribute_list_b is None or len(attribute_list_b) == 0 else [tmp_elem.copy() for tmp_elem in attribute_list_b]
        if attribute_list_b is None or len(attribute_list_b) == 0:
            return None if attribute_list_a is None or len(attribute_list_a) == 0 else [tmp_elem.copy() for tmp_elem in attribute_list_a]
        merged = []
        tmp_list_b = attribute_list_b.copy()
        for elem_a in attribute_list_a:
            elem_merged = elem_a.copy()
            for elem_b in tmp_list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                            request_uuids=request_uuids):
                    tmp_list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                                    request_uuids=request_uuids)
                    break
            merged.append(elem_merged)
        for elem_b in tmp_list_b:
            for elem_a in attribute_list_a:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                            request_uuids=request_uuids):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, key, permissions=None):
        if not AttributeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name}")
        if key is not None and not isinstance(key, str):
            raise Exception(f"key {key} is not of type str, is of type {type(key)} instead")
        Permissions.check(permissions=permissions)
        self.type_name = type_name
        self.key = key
        self.permissions = permissions
        self.is_explicit_list_element = False

    def __str__(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        if self.is_explicit_list_element:
            return "-"
        else:
            return f"  {StrUtils.str_from(self.key, quoted=True)}:"

    def __repr__(self):
        return "Attribute(" + \
            "type_name=" + repr(self.type_name) + ", " + \
            "key=" + repr(self.key) + ", " + \
            "permissions=" + repr(self.permissions) + ')'

    def __eq__(self, other):
        if not isinstance(other, Attribute):
            return False
        return \
            self.type_name == other.type_name and \
            self.key == other.key and \
            self.permissions == other.permissions

    def copy(self):
        copied_attribute = Attribute(
            type_name=self.type_name,
            key=self.key,
            permissions=self.permissions.copy() if self.permissions is not None else None
        )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element)
        return copied_attribute

    def to_dict(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self.type_name),
            ('key', self.key),
            ('permissions', self.permissions.to_dict() if self.permissions is not None else None),
        ] if tmp_value is not None}

    def is_merge_compatible_with(self, other, explanation=None):
        if not isinstance(other, Attribute):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_merge_compatible_with(...): other is not of type Attribute, "
                                            f"is of type {type(other)} instead")
            return False
        if self.type_name != other.type_name:
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_merge_compatible_with(...): "
                                            f"type_name mismatch {self.type_name} != {other.type_name}")
            return False
        if self.key != other.key:
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_merge_compatible_with(...): "
                                            f"key mismatch {self.key} != {other.key}")
            return False
        if not Permissions.are_merge_compatible(permissions_a=self.permissions, permissions_b=other.permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_merge_compatible_with(...): "
                                            f"permissions are not compatible")
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_mergeable_with(...): other is not compatible")
            return False
        if not Permissions.are_mergeable(permissions_a=self.permissions, permissions_b=other.permissions,
                                         overwrite=overwrite_permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_mergeable_with(...): permissions are not mergeable")
            return False
        merged_permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)
        if self.permissions != merged_permissions and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_PERMISSIONS,
                                                                                      request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.type_name}].is_mergeable_with(...): "
                                            f"writing permissions without write_permissions permission is not allowed")
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                      request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged.permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)
        return merged

    def set_default_permissions(self, default_permissions=None):
        Permissions.check(permissions=default_permissions)
        if self.permissions is None:
            self.permissions = default_permissions

    def set_explicit_list_element(self, is_explicit_list_element=True):
        if is_explicit_list_element and self.key is not None:
            raise Exception(f"key of explicit list element must be none, is {self.key}")
        self.is_explicit_list_element = is_explicit_list_element
