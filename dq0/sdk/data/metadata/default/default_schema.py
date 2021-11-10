from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils

class DefaultSchema:
    @staticmethod
    def default_attributes_schema(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeBoolean(key='metadata_is_public', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeInt(key='privacy_level', value=2, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def merge_default_attributes_with(schema_attributes_list, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(schema_attributes_list, list):
            raise Exception("schema_attributes_list is not of list type")
        default_schema_attributes_list = DefaultSchema.default_attributes_schema(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        tmp_schema_attributes_list = Attribute.merge_many(list_a=default_schema_attributes_list, list_b=schema_attributes_list, overwrite=True) if schema_attributes_list is not None else default_schema_attributes_list
        return [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in tmp_schema_attributes_list] if tmp_schema_attributes_list is not None else None
