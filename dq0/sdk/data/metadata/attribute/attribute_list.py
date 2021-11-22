from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeList(Attribute):
    def __init__(self, key, value, permissions=None):
        super().__init__(type_name=AttributeType.TYPE_NAME_LIST, key=key, permissions=permissions)
        if not isinstance(value, list):
            raise Exception(f"value {value} is not of type list, is of type {type(value)} instead")
        self.is_explicit_list = Attribute.check_list(attribute_list=value, allowed_keys_type_names_permissions=None)
        for tmp_attribute in value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list)
        self.value = value

    def __str__(self, request_uuids=[]):
        super_str = super().__str__(request_uuids=request_uuids)
        if super_str is None:
            return None
        return super_str + MetaUtils.restricted_str_from_list(list=self.value, sort=False, request_uuids=request_uuids)

    def __repr__(self):
        return "AttributeList(" + \
            "key=" + repr(self.key) + ", " + \
            "value=" + repr(self.value) + ", " + \
            "permissions=" + repr(self.permissions) + ')'

    def __eq__(self, other):
        if not isinstance(other, AttributeList) or not super().__eq__(other=other):
            return False
        return MetaUtils.list_equals_unordered(list_a=self.value, list_b=other.value)

    def copy(self):
        copied_attribute = AttributeList(
                key=self.key,
                value=[tmp_attribute.copy() for tmp_attribute in self.value] if self.value is not None else None,
                permissions=self.permissions.copy() if self.permissions is not None else None
            )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element)
        return copied_attribute

    def to_dict(self, request_uuids=[]):
        super_dict = super().to_dict(request_uuids=request_uuids)
        if super_dict is None:
            return None
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('value', MetaUtils.list_map_to_dict(self.value, request_uuids=request_uuids)),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_merge_compatible_with(self, other, explanation=None):
        if not super().is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_merge_compatible_with(...): super() is not compatible")                        
            return False
        if not Attribute.are_merge_compatible(attribute_list_a=self.value, attribute_list_b=other.value, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_merge_compatible_with(...): attributes are not compatible")                        
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[], explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_mergeable_with(...): not merge compatible")            
            return False
        if not super().is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_mergeable_with(...): super() is not mergeable")            
            return False
        if not Attribute.are_mergeable(attribute_list_a=self.value, attribute_list_b=other.value, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_mergeable_with(...): attributes are not mergeable")            
            return False
        merged_attributes = Attribute.merge_many(attribute_list_a=self.value, attribute_list_b=other.value, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        if self.value != merged_attributes and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_VALUE, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeList.is_mergeable_with(...): value differs without write_value permissions")            
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[]):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged.value = Attribute.merge_many(attribute_list_a=self.value, attribute_list_b=other.value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        merged.is_explicit_list = Attribute.check_list_and_is_explicit_list(list=merged.value, additional=None)
        for tmp_attribute in merged.value:
            tmp_attribute.set_explicit_list_element(is_explicit_list_element=merged.is_explicit_list)
        merged.permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)           
        return merged
    
    def set_default_permissions(self, default_permissions=None):
        Permissions.check(permissions=default_permissions)
        if self.permissions is None:
            self.permissions = default_permissions
        for attribute in self.value if self.value is not None else []:
            attribute.set_default_permissions(default_permissions=default_permissions)

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
