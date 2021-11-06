from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeList(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, list):
            raise Exception(f"value is not of type list, is of type {type(value)} instead")
        if len(value) == 0:
            raise Exception("list may not be empty")
        for elem in value:
            if not isinstance(elem, Attribute):
                raise Exception(f"list element is not of type Attribute, is of type {type(value)} instead")
        self.value = value

    def __str__(self):
        return MetaUtils.str_from(self.key) + ':' + MetaUtils.str_from_list(self.value)

    def __repr__(self):
        return "AttributeList(key=" + MetaUtils.repr_from(self.key) + ", value=" + MetaUtils.repr_from_list(self.value) + ')'

    def copy(self):
        return AttributeList(key=self.key, value=[tmp_attribute.copy() for tmp_attribute in self.value] if self.value is not None else None)

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('value', [tmp_attribute.to_dict() for tmp_attribute in self.value] if self.value is not None else None),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_merge_compatible_with(self, other):
        if not super().is_merge_compatible_with(other=other):
            print(f"super not merge compatible <-- AttributeList.is_merge_compatible_with:(self={self} other={other})")
            return False
        if not Attribute.are_merge_compatible(list_a=self.value, list_b=other.value):
            print(f"list not merge compatible <-- AttributeList.is_merge_compatible_with:(self={self} other={other})")
            return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not super().is_mergeable_with(other=other, overwrite=overwrite):
            print(f"super not mergeable <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not self.is_merge_compatible_with(other=other):
            print(f"self not merge compatible <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not Attribute.are_mergeable(list_a=self.value, list_b=other.value, overwrite=overwrite):
            print(f"list not mergeable <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        merged = self.copy()
        merged.value = Attribute.merge_many(list_a=self.value, list_b=other.value, overwrite=overwrite)
        return merged

    def get_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            return None
        for tmp_index, tmp_attribute in enumerate(self.value if self.value is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                return tmp_attribute
        return None

    def add_attribute(self, attribute, index=-1):
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(index=index, key=attribute.key, value=attribute.value) is not None:
            raise Exception("duplicate attributes not allowed")
        if self.value is None:
            self.value = []
        if index < 0:
            index = len(self.value)
        self.value.insert(index, attribute)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self.value if self.value is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                del self.value[tmp_index]
                return
        raise Exception("attribute not found")
