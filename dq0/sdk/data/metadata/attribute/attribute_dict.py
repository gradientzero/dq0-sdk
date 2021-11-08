from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeDict(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, dict):
            raise Exception("value is not of type dict")
        if len(value) == 0:
            raise Exception("dict may not be empty")
        for tmp_key, tmp_value in value.items():
            if not isinstance(tmp_key, str):
                raise Exception("dict element key is not of type str")
            if not isinstance(tmp_value, Attribute):
                raise Exception("dict element value is not of type Attribute")
        self.value = value

    def __str__(self):
        return super().__str__() + MetaUtils.str_from_dict(self.value)

    def __repr__(self):
        return "AttributeDict(key=" + MetaUtils.repr_from(self.key) + ", value=" + MetaUtils.repr_from_dict(self.value) + ')'

    def copy(self):
        return AttributeDict(key=self.key, value={tmp_key: tmp_attribute.copy() for tmp_key, tmp_attribute in self.value.items()} if self.value is not None else None)

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key_outer: tmp_value_outer for tmp_key_outer, tmp_value_outer in [
            ('value', {tmp_key_inner: tmp_attribute.to_dict() for tmp_key_inner, tmp_attribute in self.value.items()} if self.value is not None else None),
            ] if tmp_value_outer is not None}
        return {**super_dict, **self_dict}

    def is_merge_compatible_with(self, other):
        if not super().is_merge_compatible_with(other=other):
            # print(f"super not merge compatible <-- AttributeDict.is_merge_compatible_with:(self={self} other={other})")    
            return False
        if self.value is None or len(self.value) == 0:
            return True
        if other.value is None or len(other.value) == 0:
            return True
        for tmp_key, tmp_attribute in self.value.items():
            if tmp_key in other.value and not tmp_attribute.is_merge_compatible_with(other=other.value[tmp_key]):
                # print(f"dict value not merge compatible for matching key <-- AttributeDict.is_merge_compatible_with:(self={self} other={other})")    
                return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not super().is_mergeable_with(other=other, overwrite=overwrite):
            # print(f"super not mergeable <-- AttributeDict.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not self.is_merge_compatible_with(other=other):
            # print(f"self not merge compatible <-- AttributeDict.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if self.value is None or len(self.value) == 0:
            return True
        if other.value is None or len(other.value) == 0:
            return True
        for tmp_key, tmp_attribute in self.value.items():
            if tmp_key in other.value and not tmp_attribute.is_mergeable_with(other=other.value[tmp_key], overwrite=overwrite):
                # print(f"dict value not mergeable for matching key <-- AttributeDict.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
                return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        merged_value = {}
        tmp_other_value = other.copy().value
        for tmp_key, tmp_attribute in self.value.items():
            if tmp_key in tmp_other_value:
                merged_value[tmp_key] = tmp_attribute.merge_with(other=tmp_other_value[tmp_key], overwrite=overwrite)
                del tmp_other_value[tmp_key]
            else:
                merged_value[tmp_key] = tmp_attribute.copy()
        merged = self.copy()
        merged.value = {**merged_value, **tmp_other_value}
        return merged

    def get_attribute(self, dict_key=None, key=None, value=None):
        if dict_key is None and key is None and value is None:
            return None
        for tmp_dict_key, tmp_attribute in self.value.items() if self.value is not None else {}:
            if (dict_key is None or dict_key == tmp_dict_key) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                return tmp_attribute
        return None

    def add_attribute(self, dict_key, attribute):
        if dict_key is None:
            raise Exception("dict_key is none")
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(dict_key=dict_key, key=attribute.key, value=attribute.value) is not None:
            raise Exception("duplicate attributes not allowed")
        if self.value is None:
            self.value = {}
        self.value[dict_key] = attribute

    def remove_attribute(self, dict_key=None, key=None, value=None):
        if dict_key is None and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_dict_key, tmp_attribute in self.value.items() if self.value is not None else {}:
            if (dict_key is None or dict_key == tmp_dict_key) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                del self.value[tmp_dict_key]
                return
        raise Exception("attribute not found")
