from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.node.node import Node


class AttributeNode(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_NODE, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, Node):
            raise Exception("value is not of type node")
        self.value = value

    def copy(self):
        return AttributeNode(
            type_name=self.type_name,
            key=self.key,
            value=self.value.copy() if self.value is not None else None,
            )

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('value', self.value.to_dict() if self.value is not None else None),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def merge_check_with(self, other, overwrite=False):
        if not super().merge_check_with(other=other, overwrite=overwrite):
            return False
        if not self.value.merge_check_with(other=other.value, overwrite=overwrite):
            raise Exception("attributes with matching type and key may not have different values if overwrite is False")
        return True

    def merge_with(self, other, overwrite=False):
        if not self.merge_check_with(other=other, overwrite=overwrite):
            raise Exception("cannot merge attributes that fail the merge check")
        merged = self.copy()
        merged.value = self.value.merge_with(other=other.value, overwrite=overwrite)
        return merged
