from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeString(Attribute):
    def __init__(self, key, value, user_uuids=None, role_uuids=None):
        super().__init__(type_name=AttributeType.TYPE_NAME_STRING, key=key, user_uuids=user_uuids, role_uuids=role_uuids)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, str):
            raise Exception("value is not of type string")
        self.value = value

    def __str__(self, user_uuids=None, role_uuids=None):
        if not MetaUtils.is_allowed(requested_a=user_uuids, allowed_a=self.user_uuids, requested_b=role_uuids, allowed_b=self.role_uuids):
            return None
        return super().__str__() + ' ' + MetaUtils.str_from(self.value, quoted=True)

    def __repr__(self):
        return "AttributeString(" + \
            "key=" + MetaUtils.repr_from(self.key) + ", " + \
            "value=" + MetaUtils.repr_from(self.value) + ", " + \
            "user_uuids=" + MetaUtils.repr_from_list(list=self.user_uuids) + ", " + \
            "role_uuids=" + MetaUtils.repr_from_list(list=self.role_uuids) + ')'

    def copy(self):
        return AttributeString(
                key=self.key,
                value=self.value,
                user_uuids=[tmp_user for tmp_user in self.user_uuids] if self.user_uuids is not None else None,
                role_uuids=[tmp_role for tmp_role in self.role_uuids] if self.role_uuids is not None else None
            )

    def to_dict(self, user_uuids=None, role_uuids=None):
        super_dict = super().to_dict(user_uuids=user_uuids, role_uuids=role_uuids)
        if super_dict is None:
            return None
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('value', self.value),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_mergeable_with(self, other, overwrite=False):
        if not super().is_mergeable_with(other=other, overwrite=overwrite):
            # print(f"super not mergeable <-- AttributeString.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not overwrite and self.value != other.value:
            # print(f"value mismatch on no overwrite <-- AttributeString.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        merged = other.copy() if overwrite else self.copy()
        merged.user_uuids = MetaUtils.merge_uuids(uuid_list_a=self.user_uuids, uuid_list_b=other.user_uuids, overwrite=overwrite)
        merged.role_uuids = MetaUtils.merge_uuids(uuid_list_a=self.role_uuids, uuid_list_b=other.role_uuids, overwrite=overwrite)
        return merged
