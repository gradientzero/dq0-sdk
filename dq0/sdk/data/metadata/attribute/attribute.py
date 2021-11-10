from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class Attribute:
    @staticmethod
    def check_elem_and_has_none_key(attribute, list=None):
        if attribute is None:
            raise Exception("attribute is None")
        if not isinstance(attribute, Attribute):
            raise Exception(f"attribute is not of type Attribute, is of type {type(attribute)} instead")
        for elem in list if list is not None else []:
            if elem is None:
                raise Exception("attribute in list is None")
            if attribute.key is not None and attribute.key == elem.key:
                raise Exception(f"duplicate attribute key {attribute.key} detected")
        return attribute.key is None

    @staticmethod
    def check_list_and_is_explicit_list(list, additional=None):
        tmp_list = [tmp_elem for tmp_elem in list] if list is not None else []
        none_key_count = 0
        regular_key_count = 0
        if additional is not None:
            if Attribute.check_elem_and_has_none_key(attribute=additional, list=tmp_list):
                none_key_count += 1
            else:
                regular_key_count += 1
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            if Attribute.check_elem_and_has_none_key(attribute=elem_a, list=tmp_list):
                none_key_count += 1
            else:
                regular_key_count +=1
        if 0 < regular_key_count and 1 < none_key_count:
            raise Exception(f"may only have single null key in list with regular keys, there is {regular_key_count} regular keys and {none_key_count} none keys")
        return regular_key_count == 0 and 0 < none_key_count

    @staticmethod
    def are_merge_compatible(list_a, list_b):
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            for elem_b in list_b:
                if elem_a.key == elem_b.key and not elem_a.is_merge_compatible_with(other=elem_b):
                    return False
        return True

    @staticmethod
    def are_mergeable(list_a, list_b, overwrite=False):
        if not Attribute.are_merge_compatible(list_a=list_a, list_b=list_b):
            return False
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.is_merge_compatible_with(other=elem_b):
                    if not elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                        return False
                    else:
                        if found_match:
                            return False
                        found_match = True
        return True

    @staticmethod
    def merge_many(list_a, list_b, overwrite=False):
        if not Attribute.are_mergeable(list_a=list_a, list_b=list_b, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; list_a: {list_a} list_b: {list_b}")
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        tmp_list_b = [tmp_elem for tmp_elem in list_b]
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in tmp_list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                    tmp_list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite=overwrite)
                    break
            merged.append(elem_merged)
        for elem_b in tmp_list_b:
            for elem_a in list_a:
                if elem_a.is_mergeable_with(other=elem_b, overwrite=overwrite):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, key, user_uuids=None, role_uuids=None):
        if not AttributeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if user_uuids is not None:
            MetaUtils.check_uuids(user_uuids)
        if role_uuids is not None:
            MetaUtils.check_uuids(role_uuids)
        self.type_name = type_name
        self.key = key
        self.user_uuids = user_uuids
        self.role_uuids = role_uuids
        self.is_explicit_list_element=False

    def __str__(self, user_uuids=None, role_uuids=None):
        if not MetaUtils.is_allowed(requested_a=user_uuids, allowed_a=self.user_uuids, requested_b=role_uuids, allowed_b=self.role_uuids):
            return None
        if self.is_explicit_list_element:
            return "-"
        else:
            return MetaUtils.str_from(self.key, quoted=True) + ":"

    def __repr__(self):
        return "Attribute(" + \
            "type_name=" + MetaUtils.repr_from(self.type_name) + ", " + \
            "key=" + MetaUtils.repr_from(self.key) + ", " + \
            "user_uuids=" + MetaUtils.repr_from_list(list=self.user_uuids) + ", " + \
            "role_uuids=" + MetaUtils.repr_from_list(list=self.role_uuids) + ')'

    def copy(self):
        copied_attribute = Attribute(
                type_name=self.type_name,
                key=self.key,
                user_uuids=[tmp_user for tmp_user in self.user_uuids] if self.user_uuids is not None else None,
                role_uuids=[tmp_role for tmp_role in self.role_uuids] if self.role_uuids is not None else None
            )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element)
        return copied_attribute

    def to_dict(self, user_uuids=None, role_uuids=None):
        if not MetaUtils.is_allowed(requested_a=user_uuids, allowed_a=self.user_uuids, requested_b=role_uuids, allowed_b=self.role_uuids):
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('type_name', self.type_name),
                ('key', self.key),
                ('user_uuids', [tmp_user for tmp_user in self.user_uuids] if self.user_uuids is not None else None),
                ('role_uuids', [tmp_role for tmp_role in self.role_uuids] if self.role_uuids is not None else None)
            ] if tmp_value is not None}

    def is_merge_compatible_with(self, other):
        if other is None:
            # print(f"other is None <-- Attribute.is_merge_compatible_with:(self={self} other=None)")
            return False
        if self.type_name != other.type_name:
            # print(f"type_names mismatch <-- Attribute.is_merge_compatible_with:(self={self} other={other})")
            return False
        if self.key != other.key:
            # print(f"keys mismatch <-- Attribute.is_merge_compatible_with:(self={self} other={other})")
            return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not self.is_merge_compatible_with(other=other):
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        merged = self.copy()
        merged.user_uuids = MetaUtils.merge_uuids(uuid_list_a=self.user_uuids, uuid_list_b=other.user_uuids, overwrite=overwrite)
        merged.role_uuids = MetaUtils.merge_uuids(uuid_list_a=self.role_uuids, uuid_list_b=other.role_uuids, overwrite=overwrite)
        return merged

    def set_explicit_list_element(self, is_explicit_list_element=True):
        if is_explicit_list_element and self.key is not None:
            raise Exception(f"key of explicit list element must be none, is {self.key}")
        self.is_explicit_list_element=is_explicit_list_element
