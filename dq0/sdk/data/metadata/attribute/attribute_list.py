from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeList(Attribute):
    def __init__(self, key, value, user_uuids=None, role_uuids=None):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key, user_uuids=user_uuids, role_uuids=role_uuids)
        if value is None:
            raise Exception("value is None")
        if not isinstance(value, list):
            raise Exception(f"value is not of type list, is of type {type(value)} instead")
        self.is_explicit_list = Attribute.check_list_and_is_explicit_list(list=value, additional=None)
        for tmp_attribute in value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list)
        self.value = value

    def __str__(self, user_uuids=None, role_uuids=None):
        if not MetaUtils.is_allowed(requested_a=user_uuids, allowed_a=self.user_uuids, requested_b=role_uuids, allowed_b=self.role_uuids):
            return None
        return super().__str__() + MetaUtils.restricted_str_from_list(list=self.value, sort=False, user_uuids=user_uuids, role_uuids=role_uuids)

    def __repr__(self):
        return "AttributeList(" + \
            "key=" + MetaUtils.repr_from(self.key) + ", " + \
            "value=" + MetaUtils.repr_from_list(self.value) + ", " + \
            "user_uuids=" + MetaUtils.repr_from_list(list=self.user_uuids) + ", " + \
            "role_uuids=" + MetaUtils.repr_from_list(list=self.role_uuids) + ')'

    def copy(self):
        copied_attribute = AttributeList(
                key=self.key,
                value=[tmp_attribute.copy() for tmp_attribute in self.value] if self.value is not None else None,
                user_uuids=[tmp_user for tmp_user in self.user_uuids] if self.user_uuids is not None else None,
                role_uuids=[tmp_role for tmp_role in self.role_uuids] if self.role_uuids is not None else None
            )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element)
        return copied_attribute

    def to_dict(self, user_uuids=None, role_uuids=None):
        super_dict = super().to_dict(user_uuids=user_uuids, role_uuids=role_uuids)
        if super_dict is None:
            return None
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('value', MetaUtils.list_map_to_dict(self.value, user_uuids=user_uuids, role_uuids=role_uuids)),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_merge_compatible_with(self, other):
        if not super().is_merge_compatible_with(other=other):
            # print(f"super not merge compatible <-- AttributeList.is_merge_compatible_with:(self={self} other={other})")
            return False
        if not Attribute.are_merge_compatible(list_a=self.value, list_b=other.value):
            # print(f"list not merge compatible <-- AttributeList.is_merge_compatible_with:(self={self} other={other})")
            return False
        return True

    def is_mergeable_with(self, other, overwrite=False):
        if not super().is_mergeable_with(other=other, overwrite=overwrite):
            # print(f"super not mergeable <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not self.is_merge_compatible_with(other=other):
            # print(f"self not merge compatible <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        if not Attribute.are_mergeable(list_a=self.value, list_b=other.value, overwrite=overwrite):
            # print(f"list not mergeable <-- AttributeList.is_mergeable_with:(self={self} other={other} overwrite={overwrite})")
            return False
        return True

    def merge_with(self, other, overwrite=False):
        if not self.is_mergeable_with(other=other, overwrite=overwrite):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other}")
        merged = self.copy()
        merged.value = Attribute.merge_many(list_a=self.value, list_b=other.value, overwrite=overwrite)
        merged.is_explicit_list = Attribute.check_list_and_is_explicit_list(list=merged.value, additional=None)
        for tmp_attribute in merged.value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=merged.is_explicit_list)
        merged.user_uuids = MetaUtils.merge_uuids(uuid_list_a=self.user_uuids, uuid_list_b=other.user_uuids, overwrite=overwrite)
        merged.role_uuids = MetaUtils.merge_uuids(uuid_list_a=self.role_uuids, uuid_list_b=other.role_uuids, overwrite=overwrite)
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
        self.is_explicit_list = Attribute.check_list_and_is_explicit_list(list=self.value, additional=attribute)
        if index < 0:
            index = len(self.value)
        self.value.insert(index, attribute)
        for tmp_attribute in self.value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self.value if self.value is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                del self.value[tmp_index]
                self.is_explicit_list = Attribute.check_list_and_is_explicit_list(list=self.value, additional=None)
                for tmp_attribute in self.value:
                    tmp_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list)
                return
        raise Exception("attribute not found")
