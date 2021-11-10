from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils

class DefaultDatabase:
    @staticmethod
    def default_attributes_database(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeBoolean(key='metadata_is_public', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def merge_default_attributes_with(database_attributes_list, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(database_attributes_list, list):
            raise Exception("database_attributes_list is not of list type")
        default_database_attributes_list = DefaultDatabase.default_attributes_database(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        tmp_database_attributes_list = Attribute.merge_many(list_a=default_database_attributes_list, list_b=database_attributes_list, overwrite=True) if database_attributes_list is not None else default_database_attributes_list
        return [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in tmp_database_attributes_list] if tmp_database_attributes_list is not None else None
