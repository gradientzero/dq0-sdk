from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute import Attribute

class DefaultDataset:
    @staticmethod
    def defaultAttributesDataset():
        return [
            AttributeBoolean(key='metadata_is_public', value=False),
        ]

    @staticmethod
    def mergeDefaultAttributesWith(dataset_attributes_list):
        if not isinstance(dataset_attributes_list, list):
            raise Exception("dataset_attributes_list is not of list type")
        default_dataset_attributes_list = DefaultDataset.defaultAttributesDataset()
        return Attribute.merge_many(list_a=default_dataset_attributes_list, list_b=dataset_attributes_list, overwrite=True) if dataset_attributes_list is not None else default_dataset_attributes_list
