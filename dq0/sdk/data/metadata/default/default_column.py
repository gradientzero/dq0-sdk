from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.default.default_utils import DefaultUtils


class DefaultColumn:
    @staticmethod
    def default_column_boolean_attributes():
        return [
            AttributeString(key='data_type_name', value='boolean'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='synthesizable', value=False),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
        ]

    @staticmethod
    def default_column_datetime_attributes():
        return [
            AttributeString(key='data_type_name', value='datetime'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='synthesizable', value=False),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
        ]

    @staticmethod
    def default_column_float_attributes():
        return [
            AttributeString(key='data_type_name', value='float'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='use_auto_bounds', value=False),
            AttributeFloat(key='auto_bounds_prob', value=0.9),
            AttributeBoolean(key='discrete', value=False),
            AttributeFloat(key='min_step', value=1.0),
            AttributeBoolean(key='synthesizable', value=True),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
            AttributeBoolean(key='bounded', value=False),
            AttributeFloat(key='auto_lower', value=0.0),
            AttributeFloat(key='auto_upper', value=0.0),
            AttributeFloat(key='lower', value=0.0),
            AttributeFloat(key='upper', value=0.0),
        ]

    @staticmethod
    def default_column_int_attributes():
        return [
            AttributeList(key='bounding', value=[
                AttributeBoolean(key='use_auto_bounds', value=False),
                AttributeFloat(key='auto_bounds_prob', value=0.9),
                AttributeBoolean(key='bounded', value=False),
                AttributeInt(key='auto_lower', value=0),
                AttributeInt(key='auto_upper', value=0),
                AttributeInt(key='lower', value=0),
                AttributeInt(key='upper', value=0),
            ]),
            AttributeList(key='machine_learning', value=[
                AttributeBoolean(key='is_feature', value=False),
                AttributeBoolean(key='is_target', value=False),
            ]),
            AttributeList(key='data', value=[
                AttributeString(key='data_type_name', value='int'),
                AttributeBoolean(key='discrete', value=False),
                AttributeInt(key='min_step', value=1),
            ]),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='synthesizable', value=True),
            AttributeBoolean(key='private_id', value=False),
        ]

    @staticmethod
    def default_column_string_attributes(cardinality=0):
        return [
            AttributeString('data_type_name', value='string'),
            AttributeBoolean('selectable', value=False),
            AttributeInt('cardinality', value=0),
            AttributeBoolean('synthesizable', value=cardinality != 0),
            AttributeBoolean('is_feature', value=False),
            AttributeBoolean('is_target', value=False),
            AttributeBoolean('private_id', value=False),
        ]

    @staticmethod
    def get_default_attributes_for(data_type_name, cardinality=0):
        if data_type_name == 'boolean':
            return DefaultColumn.default_column_boolean_attributes()
        if data_type_name == 'datetime':
            return DefaultColumn.default_column_datetime_attributes()
        if data_type_name == 'float':
            return DefaultColumn.default_column_float_attributes()
        if data_type_name == 'int':
            return DefaultColumn.default_column_int_attributes()
        if data_type_name == 'string':
            return DefaultColumn.default_column_string_attributes(cardinality=cardinality)
        return []

    @staticmethod
    def merge_default_attributes_with(column_attributes_list):
        if not isinstance(column_attributes_list, list):
            raise Exception("connector_attribute_list is not of list type")
        data_type_name = DefaultUtils.find_attribute(attributes_list=column_attributes_list, key='data_type_name')
        cardinality = DefaultUtils.find_attribute(attributes_list=column_attributes_list, key='cardinality')
        if cardinality is None:
            cardinality = 0
        default_column_attributes_list = DefaultColumn.get_default_attributes_for(data_type_name=data_type_name, cardinality=cardinality)
        return Attribute.merge_many(list_a=default_column_attributes_list, list_b=column_attributes_list, overwrite=True) if column_attributes_list is not None else default_column_attributes_list
