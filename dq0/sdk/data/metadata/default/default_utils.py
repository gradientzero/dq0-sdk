from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class DefaultUtils:
    @staticmethod
    def find_attribute(attributes_list, key):
        for tmp_attribute in attributes_list if attributes_list is not None else []:
            if tmp_attribute is None:
                raise Exception("found None attribute in list")
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("found list element that is not of type Attribute")
            if tmp_attribute.key == key:
                return tmp_attribute.value
            if isinstance(tmp_attribute, AttributeList):
                return DefaultUtils.find_attribute(attributes_list=tmp_attribute.value, key=key)
        return None

    @staticmethod
    def merge_default_uuids_with(attribute, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(attribute, Attribute):
            raise Exception(f"attribute is not of type Attribute, is of type {type(attribute)} instead")
        merged = attribute.copy()
        merged.user_uuids = MetaUtils.merge_uuids(uuid_list_a=default_user_uuids, uuid_list_b=merged.user_uuids, overwrite=True)
        merged.role_uuids = MetaUtils.merge_uuids(uuid_list_a=default_role_uuids, uuid_list_b=merged.role_uuids, overwrite=True)
        if merged.type_name == AttributeType.TYPE_NAME_LIST:
            merged.value = [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in merged.value] if merged.value is not None else None
        return merged
