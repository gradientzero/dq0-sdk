from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils


class DefaultColumn:
    @staticmethod
    def default_column_boolean_attributes(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeString(key='data_type_name', value='boolean', user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='selectable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='synthesizable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_feature', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_target', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='private_id', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def default_column_datetime_attributes(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeString(key='data_type_name', value='datetime', user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='selectable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='synthesizable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_feature', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_target', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='private_id', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def default_column_float_attributes(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeString(key='data_type_name', value='float', user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='selectable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='use_auto_bounds', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='auto_bounds_prob', value=0.9, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='discrete', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='min_step', value=1.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='synthesizable', value=True, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_feature', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='is_target', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='private_id', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='bounded', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='auto_lower', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='auto_upper', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='lower', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeFloat(key='upper', value=0.0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def default_column_int_attributes(default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeList(key='bounding', value=[
                AttributeBoolean(key='use_auto_bounds', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeFloat(key='auto_bounds_prob', value=0.9, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeBoolean(key='bounded', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeInt(key='auto_lower', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeInt(key='auto_upper', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeInt(key='lower', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeInt(key='upper', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            ], user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeList(key='machine_learning', value=[
                AttributeBoolean(key='is_feature', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeBoolean(key='is_target', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            ], user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeList(key='data', value=[
                AttributeString(key='data_type_name', value='int', user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeBoolean(key='discrete', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
                AttributeInt(key='min_step', value=1, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            ], user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='selectable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='synthesizable', value=True, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean(key='private_id', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def default_column_string_attributes(cardinality=0, default_user_uuids=None, default_role_uuids=None):
        return [
            AttributeString('data_type_name', value='string', user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean('selectable', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeInt('cardinality', value=0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean('synthesizable', value=cardinality != 0, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean('is_feature', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean('is_target', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
            AttributeBoolean('private_id', value=False, user_uuids=default_user_uuids, role_uuids=default_role_uuids),
        ]

    @staticmethod
    def get_default_attributes_for(data_type_name, cardinality=0, default_user_uuids=None, default_role_uuids=None):
        if data_type_name == 'boolean':
            return DefaultColumn.default_column_boolean_attributes(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        if data_type_name == 'datetime':
            return DefaultColumn.default_column_datetime_attributes(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        if data_type_name == 'float':
            return DefaultColumn.default_column_float_attributes(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        if data_type_name == 'int':
            return DefaultColumn.default_column_int_attributes(default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        if data_type_name == 'string':
            return DefaultColumn.default_column_string_attributes(cardinality=cardinality, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        return []

    @staticmethod
    def merge_default_attributes_with(column_attributes_list, default_user_uuids=None, default_role_uuids=None):
        if not isinstance(column_attributes_list, list):
            raise Exception("connector_attribute_list is not of list type")
        data_type_name = DefaultUtils.find_attribute(attributes_list=column_attributes_list, key='data_type_name')
        cardinality = DefaultUtils.find_attribute(attributes_list=column_attributes_list, key='cardinality')
        if cardinality is None:
            cardinality = 0
        default_column_attributes_list = DefaultColumn.get_default_attributes_for(data_type_name=data_type_name, cardinality=cardinality, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        tmp_column_attributes_list = Attribute.merge_many(list_a=default_column_attributes_list, list_b=column_attributes_list, overwrite=True) if column_attributes_list is not None else default_column_attributes_list
        return [DefaultUtils.merge_default_uuids_with(attribute=tmp_attribute, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids) for tmp_attribute in tmp_column_attributes_list] if tmp_column_attributes_list is not None else None
