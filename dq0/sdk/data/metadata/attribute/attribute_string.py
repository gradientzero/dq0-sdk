from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeString(Attribute):
    def __init__(self, key, value):
        super().__init__(type_name=AttributeType.TYPE_NAME_STRING, key=key)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, str):
            raise Exception("value is not of type string")
        self.value = value

    def __str__(self):
        return MetaUtils.str_from(self.key) + ": " + MetaUtils.str_from(self.value)

    def __repr__(self):
        return "AttributeString(key=" + MetaUtils.repr_from(self.key) + ", value=" + MetaUtils.repr_from(self.value) + ')'

    def copy(self):
        return AttributeString(key=self.key, value=self.value)

    def to_dict(self):
        super_dict = super().to_dict()
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('value', self.value),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_mergeable_with(self, other, overwrite=False):
        if not super().is_mergeable_with(other=other, overwrite=overwrite):
            print(f"super not mergeable <-- AttributeString.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not overwrite and self.value != other.value:
            print(f"value mismatch on no overwrite <-- AttributeString.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        return other.copy() if overwrite else self.copy()
