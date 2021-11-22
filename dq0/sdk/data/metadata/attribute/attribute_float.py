from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class AttributeFloat(Attribute):
    def __init__(self, key, value, permissions=None):
        super().__init__(type_name=AttributeType.TYPE_NAME_FLOAT, key=key, permissions=permissions)
        if not isinstance(value, float):
            raise Exception(f"value {value} is not of type float, is of type {type(value)} instead")
        self.value = value

    def __str__(self, request_uuids=[]):
        super_str = super().__str__(request_uuids=request_uuids)
        if super_str is None:
            return None
        return super_str + ' ' + MetaUtils.str_from(object=self.value, quoted=False)

    def __repr__(self):
        return "AttributeFloat(" + \
            "key=" + repr(self.key) + ", " + \
            "value=" + repr(self.value) + ", " + \
            "permissions=" + repr(self.permissions) + ')'

    def __eq__(self, other):
        if not isinstance(other, AttributeFloat) or not super().__eq__(other=other):
            return False            
        return self.value == other.value

    def copy(self):
        copied_attribute = AttributeFloat(
                key=self.key,
                value=self.value,
                permissions=self.permissions.copy() if self.permissions is not None else None
            )
        copied_attribute.set_explicit_list_element(is_explicit_list_element=self.is_explicit_list_element)
        return copied_attribute
    
    def to_dict(self, request_uuids=[]):
        super_dict = super().to_dict(request_uuids=request_uuids)
        if super_dict is None:
            return None
        self_dict = {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('value', self.value),
            ] if tmp_value is not None}
        return {**super_dict, **self_dict}

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[], explanation=None):
        if not super().is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeFloat.is_mergeable_with(...): super() is not mergeable")            
            return False
        if not overwrite_value and self.value != other.value:
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeFloat.is_mergeable_with(...): value differs without overwrite_value")            
            return False
        if self.value != other.value and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_VALUE, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"AttributeFloat.is_mergeable_with(...): value differs without write_value permissions")            
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[]):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge attributes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = other.copy()
        merged.permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)           
        return merged
