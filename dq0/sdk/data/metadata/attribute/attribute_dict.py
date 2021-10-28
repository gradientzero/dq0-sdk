from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute


class AttributeDict(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, dict):
            raise Exception("value is not of type dict")
        if len(value) == 0:
            raise Exception("dict may not be empty")
        for tmp_key, tmp_value in value:
            if not isinstance(tmp_key, str):
                raise Exception("dict element key is not of type str")
            if not isinstance(tmp_value, Attribute):
                raise Exception("dict element value is not of type Attribute")
        self.value = value

    def copy(self):
        return AttributeDict(
            type_name=self.type_name,
            key=self.key,
            value={tmp_key: tmp_attribute.copy() for tmp_key, tmp_attribute in self.value} if self.value is not None else None,
            )

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key_outer: tmp_value_outer for tmp_key_outer, tmp_value_outer in [
            ('value', {tmp_key_inner: tmp_attribute.to_dict() for tmp_key_inner, tmp_attribute in self.value} if self.value is not None else None),
            ] if tmp_value_outer is not None}
        return {**super_dict, **self_dict}

    def merge_check_with(self, other, overwrite=False):
        if not super().merge_check_with(other=other, overwrite=overwrite):
            return False
        if not Attribute.merge_check_many_with_many(list_a=self.value, list_b=other.value, overwrite=overwrite):
            raise Exception("attributes with matching type and key may not have different values if overwrite is False")
        return True

    def merge_with(self, other, overwrite=False):
        if not self.merge_check_with(other=other, overwrite=overwrite):
            raise Exception("cannot merge attributes that fail the merge check")
        merged = self.copy()
        merged.value = Attribute.merge_many_with_many(list_a=self.value, list_b=other.value, overwrite=overwrite)
        return merged

    def get_attribute(self, key):
        if self.value is not None and key in self.value:
            return self.value[key]
        return None
