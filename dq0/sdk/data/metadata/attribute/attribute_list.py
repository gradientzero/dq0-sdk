from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute


class AttributeList(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, list):
            raise Exception("value is not of type list")
        if len(value) == 0:
            raise Exception("list may not be empty")
        for elem in value:
            if not isinstance(elem, Attribute):
                raise Exception("list element is not of type Attribute")
        self.value = value

    def copy(self):
        return AttributeList(
            type_name=self.type_name,
            key=self.key,
            value=[tmp_attribute.copy() for tmp_attribute in self.value] if self.value is not None else None,
            )

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('value', [tmp_attribute.to_dict() for tmp_attribute in self.value] if self.value is not None else None),
            ] if tmp_value is not None}
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
        for tmp_attribute in self.value if self.value is not None else []:
            if tmp_attribute.key == key:
                return tmp_attribute
        return None
