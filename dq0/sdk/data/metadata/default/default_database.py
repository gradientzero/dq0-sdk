from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute import Attribute

class DefaultDatabase:
    @staticmethod
    def defaultAttributesDatabase():
        return [
            AttributeBoolean(key='metadata_is_public', value=False),
        ]

    @staticmethod
    def mergeDefaultAttributesWith(database_attributes_list):
        if not isinstance(database_attributes_list, list):
            raise Exception("database_attributes_list is not of list type")
        default_database_attributes_list = DefaultDatabase.defaultAttributesDatabase()
        return Attribute.merge_many_with_many(list_a=default_database_attributes_list, list_b=database_attributes_list, overwrite=True) if database_attributes_list is not None else default_database_attributes_list
