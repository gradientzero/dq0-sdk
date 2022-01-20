from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.explanation import Explanation
from dq0.sdk.data.metadata.structure.merge_exception import MergeException
from dq0.sdk.data.metadata.structure.permissions.action import Action
from dq0.sdk.data.metadata.structure.permissions.permissions import Permissions
from dq0.sdk.data.metadata.structure.utils.str_utils import StrUtils


class Attribute:
    @staticmethod
    def check(attribute, check_data=None):
        if not isinstance(attribute, Attribute):
            raise Exception(f"attribute is not of type Attribute, is of type {type(attribute)} instead")
        if check_data is not None:
            if attribute.get_key() not in check_data:
                raise Exception(f"attribute.get_key() {attribute.get_key()} is not in allowed keys {check_data.keys()}")
            allowed_type_names, allowed_permissions = check_data[attribute.get_key()]
            if allowed_type_names is not None and attribute.get_type_name() not in allowed_type_names:
                raise Exception(f"attribute.get_type_name() {attribute.get_type_name()} is not in allowed_type_names {allowed_type_names}")
            if not Permissions.is_subset_of(permissions_a=attribute.get_permissions(), permissions_b=allowed_permissions):
                raise Exception("attribute.get_permissions()" + f"{attribute.get_permissions()}" + "\n"
                                "are not in allowed_permissions" + f"{allowed_permissions}")

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
            if attribute.get_key() is None:
                none_key_count += 1
            else:
                if attribute.get_key() in keys:
                    raise Exception(f"duplicate attribute key {attribute.get_key()} is not allowed")
                keys.add(attribute.get_key())
                regular_key_count += 1
        for required_key in required_keys if required_keys is not None else set():
            if required_key not in keys:
                raise Exception(f"required_key {required_key} is not in the list")
        if 0 < regular_key_count and 1 < none_key_count:
            raise Exception(f"may only have single none (null) key in list with regular keys, "
                            f"there is {regular_key_count} regular key(s) and {none_key_count} none key(s)")
        return regular_key_count == 0 and 1 < none_key_count

    @staticmethod
    def are_merge_compatible(attribute_list_a, attribute_list_b, explanation=None):
        if attribute_list_a is None or len(attribute_list_a) == 0 or attribute_list_b is None or len(attribute_list_b) == 0:
            return True
        Attribute.check_list(attribute_list=attribute_list_a, check_data=None)
        Attribute.check_list(attribute_list=attribute_list_b, check_data=None)
        for attribute_a in attribute_list_a:
            for attribute_b in attribute_list_b:
                if attribute_a.get_key() == attribute_b.get_key() and not attribute_a.is_merge_compatible_with(other=attribute_b, explanation=explanation):
                    Explanation.dynamic_add_message(explanation=explanation,
                                                    message=f"Attribute.are_merge_compatible(...): attributes[{attribute_a.get_type_name()}] "
                                                    f"with matching key {attribute_a.get_key()} are not compatible")
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
                                                        message=f"Attribute.are_mergeable(...): compatible attributes[{elem_a.get_type_name()}] "
                                                        f"with key {elem_a.get_key()} are not mergeable")
                        return False
                    else:
                        if found_match:
                            Explanation.dynamic_add_message(explanation=explanation,
                                                            message=f"Attribute.are_mergeable(...): duplicate mergeable attributes[{elem_a.get_type_name()}] "
                                                            f"with key {elem_a.get_key()} are not allowed")
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
        self._type_name = type_name
        self._key = key
        self._permissions = permissions
        self._is_explicit_list_element = False

    def __str__(self, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.get_permissions(), action=Action.READ, request_uuids=request_uuids):
            return None
        if self._is_explicit_list_element:
            return "-"
        else:
            return f"  {StrUtils.str_from(self.get_key(), quoted=True)}:"

    def __repr__(self):
        return "Attribute(" + \
            "type_name=" + repr(self.get_type_name()) + ", " + \
            "key=" + repr(self.get_key()) + ", " + \
            "permissions=" + repr(self.get_permissions()) + ')'

    def __eq__(self, other):
        if not isinstance(other, Attribute):
            return False
        return \
            self.get_type_name() == other.get_type_name() and \
            self.get_key() == other.get_key() and \
            self.get_permissions() == other.get_permissions()

    def get_type_name(self):
        return self._type_name

    def get_key(self):
        return self._key

    def get_permissions(self):
        return self._permissions

    def is_explicit_list_element(self):
        return self._is_explicit_list_element

    def copy(self):
        copied_attribute = Attribute(
            type_name=self.get_type_name(),
            key=self.get_key(),
            permissions=self.get_permissions().copy() if self.get_permissions() is not None else None
        )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self._is_explicit_list_element)
        return copied_attribute

    def to_dict_simple(self, value, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.get_permissions(), action=Action.READ, request_uuids=request_uuids):
            return None
        return {self.get_key(): value}

    def to_dict_full(self, value, request_uuids=set()):
        if not Permissions.is_allowed_with(permissions=self.get_permissions(), action=Action.READ, request_uuids=request_uuids):
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self.get_type_name()),
            ('key', self.get_key()),
            ('permissions', self.get_permissions().to_dict() if self.get_permissions() is not None else None),
            ('value', value),
        ] if tmp_value is not None}

    def to_dict(self, value, request_uuids=set(), full=True):
        if full:
            return self.to_dict_full(value=value, request_uuids=request_uuids)
        return self.to_dict_simple(value=value, request_uuids=request_uuids)

    def is_merge_compatible_with(self, other, explanation=None):
        if not isinstance(other, Attribute):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_merge_compatible_with(...): other is not of type Attribute, "
                                            f"is of type {type(other)} instead")
            return False
        if self.get_type_name() != other.get_type_name():
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_merge_compatible_with(...): "
                                            f"type_name mismatch {self.get_type_name()} != {other.get_type_name()}")
            return False
        if self.get_key() != other.get_key():
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_merge_compatible_with(...): "
                                            f"key mismatch {self.get_key()} != {other.get_key()}")
            return False
        if not Permissions.are_merge_compatible(permissions_a=self.get_permissions(), permissions_b=other.get_permissions(), explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_merge_compatible_with(...): "
                                            f"permissions are not compatible")
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_mergeable_with(...): other is not compatible")
            return False
        if not Permissions.are_mergeable(permissions_a=self.get_permissions(), permissions_b=other.get_permissions(),
                                         overwrite=overwrite_permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_mergeable_with(...): permissions are not mergeable")
            return False
        merged_permissions = Permissions.merge(permissions_a=self.get_permissions(), permissions_b=other.get_permissions(), overwrite=overwrite_permissions)
        if self.get_permissions() != merged_permissions and not Permissions.is_allowed_with(permissions=self.get_permissions(), action=Action.WRITE_PERMISSIONS,
                                                                                            request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation,
                                            message=f"Attribute[{self.get_type_name()}].is_mergeable_with(...): "
                                            f"writing permissions without write_permissions permission is not allowed")
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set()):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions,
                                      request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged._permissions = Permissions.merge(permissions_a=self.get_permissions(), permissions_b=other.get_permissions(), overwrite=overwrite_permissions)
        return merged

    def set_default_permissions(self, default_permissions=None):
        Permissions.check(permissions=default_permissions)
        if self.get_permissions() is None:
            self._permissions = default_permissions

    def set_explicit_list_element(self, is_explicit_list_element=True):
        if is_explicit_list_element and self.get_key() is not None:
            raise Exception(f"key of explicit list element must be none, is {self.get_key()}")
        self._is_explicit_list_element = is_explicit_list_element
