from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute import Attribute

class DefaultTable:
    @staticmethod
    def defaultAttributesTable():
        return [
            AttributeBoolean(key='metadata_is_public', value=False),
            AttributeInt(key='privacy_level', value=2),
            AttributeFloat(key='budget_epsilon', value=0.0),
            AttributeFloat(key='budget_delta', value=0.0),
            AttributeBoolean(key='synth_allowed', value=False),
            AttributeFloat(key='tau', value=0.0),
            AttributeBoolean(key='row_privacy', value=False),
            AttributeInt(key='rows', value=0),
            AttributeInt(key='max_ids', value=1),
            AttributeBoolean(key='sample_max_ids', value=True),
            AttributeBoolean(key='use_dpsu', value=False),
            AttributeBoolean(key='clamp_counts', value=False),
            AttributeBoolean(key='clamp_columns', value=True),
            AttributeBoolean(key='censor_dims', value=False),
        ]

    @staticmethod
    def mergeDefaultAttributesWith(table_attributes_list):
        if not isinstance(table_attributes_list, list):
            raise Exception("table_attributes_list is not of list type")
        default_table_attributes_list = DefaultTable.defaultAttributesTable()
        return Attribute.merge_many_with_many(list_a=default_table_attributes_list, list_b=table_attributes_list, overwrite=True) if table_attributes_list is not None else default_table_attributes_list
