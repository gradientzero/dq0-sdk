from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType


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
    def merge_check_many_with_many(list_a, list_b, overwrite=False):
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.merge_check_with(other=elem_b, overwrite=overwrite):
                    if found_match:
                        raise Exception("element matches more than one other element")
                    found_match = True
        return True

    @staticmethod
    def merge_many_with_many(list_a, list_b, overwrite=False):
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in list_b:
                if elem_a.merge_check_with(other=elem_b, overwrite=overwrite):
                    list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite=overwrite)
                    break
            merged.append(elem_merged)
        for elem_b in list_b:
            for elem_a in list_a:
                if elem_b.merge_check_with(other=elem_a, overwrite=overwrite):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, key):
        if not AttributeType.isValidTypeName(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if key is None:
            raise Exception("key is None")
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

    def merge_check_with(self, other, overwrite=False):
        return not (other is None or self.type_name != other.type_name or self.key != other.key)

    def merge_with(self, other, overwrite=False):
        if not self.merge_check_with(other=other, overwrite=overwrite):
            raise Exception("cannot merge attributes that fail the merge check")
        return self.copy()
