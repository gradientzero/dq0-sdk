from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute import Attribute

class DefaultSchema:
    @staticmethod
    def defaultAttributesSchema():
        return [
            AttributeBoolean(key='metadata_is_public', value=False),
            AttributeInt(key='privacy_level', value=2),
        ]

    @staticmethod
    def mergeDefaultAttributesWith(schema_attributes_list):
        if not isinstance(schema_attributes_list, list):
            raise Exception("schema_attributes_list is not of list type")
        default_schema_attributes_list = DefaultSchema.defaultAttributesSchema()
        return Attribute.merge_many_with_many(list_a=default_schema_attributes_list, list_b=schema_attributes_list, overwrite=True) if schema_attributes_list is not None else default_schema_attributes_list
