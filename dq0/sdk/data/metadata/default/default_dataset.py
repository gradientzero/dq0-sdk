from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils

class DefaultDataset:
    @staticmethod
    def default_attributes_dataset(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeBoolean(key='metadata_is_public', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def merge_default_attributes_with(dataset_attributes_list, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(dataset_attributes_list, list):
            raise Exception("dataset_attributes_list is not of list type")
        default_dataset_attributes_list = DefaultDataset.default_attributes_dataset(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        tmp_dataset_attributes_list = Attribute.merge_many(list_a=default_dataset_attributes_list, list_b=dataset_attributes_list, overwrite=True) if dataset_attributes_list is not None else default_dataset_attributes_list
        return [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in tmp_dataset_attributes_list] if tmp_dataset_attributes_list is not None else None
