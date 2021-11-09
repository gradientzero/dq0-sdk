from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute import Attribute


class DefaultUtils:
    @staticmethod
    def find_attribute(attributes_list, key):
        for tmp_attribute in attributes_list if attributes_list is not None else []:
            if tmp_attribute is None:
                raise Exception("found None attribute in list")
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("found list element that is not of type Attribute")
            if tmp_attribute.key == key:
                return tmp_attribute.value
            if isinstance(tmp_attribute, AttributeList):
                return DefaultUtils.find_attribute(attributes_list=tmp_attribute.value, key=key)
        return None
