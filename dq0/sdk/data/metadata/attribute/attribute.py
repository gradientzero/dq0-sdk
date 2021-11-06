from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.merge_exception import MergeException


class Attribute:
    @staticmethod
    def init_check_many(list):
        tmp_list = [tmp_elem for tmp_elem in list] if list is not None else []
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            if elem_a is None:
                raise Exception("attribute cannot be None")
            for elem_b in tmp_list:
                if elem_b is None:
                    raise Exception("attribute cannot be None")
                if elem_a.key == elem_b.key:
                    raise Exception(f"duplicate attribute key {elem_a.key if elem_a.key is not None else 'None'} detected")

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

    def __init__(self, type_name, key):
        if not AttributeType.isValidTypeName(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name
        self.key = key

    def copy(self):
        return Attribute(
            self.type_name,
            self.key,
            )

    def to_dict(self):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self.type_name),
            ('key', self.key),
            ] if tmp_value is not None}

    def is_merge_compatible_with(self, other):
        if other is None:
            print(f"other is None <-- Attribute.is_merge_compatible_with:(self={self} other=None)")
            return False
        if self.type_name != other.type_name:
            print(f"type_names mismatch <-- Attribute.is_merge_compatible_with:(self={self} other={other})")
            return False
        if self.key != other.key:
            print(f"keys mismatch <-- Attribute.is_merge_compatible_with:(self={self} other={other})")
            return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not self.is_merge_compatible_with(other=other):
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        return self.copy()
