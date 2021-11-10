from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils

class DefaultTable:
    @staticmethod
    def default_attributes_table(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeBoolean(key='metadata_is_public', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeInt(key='privacy_level', value=2, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='budget_epsilon', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='budget_delta', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='synth_allowed', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='tau', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='row_privacy', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeInt(key='rows', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeInt(key='max_ids', value=1, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='sample_max_ids', value=True, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='use_dpsu', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='clamp_counts', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='clamp_columns', value=True, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='censor_dims', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def merge_default_attributes_with(table_attributes_list, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(table_attributes_list, list):
            raise Exception("table_attributes_list is not of list type")
        default_table_attributes_list = DefaultTable.default_attributes_table(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        tmp_schema_attributes_list = Attribute.merge_many(list_a=default_table_attributes_list, list_b=table_attributes_list, overwrite=True) if table_attributes_list is not None else default_table_attributes_list
        return [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in tmp_schema_attributes_list] if tmp_schema_attributes_list is not None else None
