from dq0.sdk.data.metadata.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute


class AttributesGroup:
    @staticmethod
    def json_schema(key, title, group_name, description, contains=None, attributes=None):
        contains_json = ''
        if contains is not None:
            contains_json = "\n\"contains\": " + f"{contains},"
        items_json = ''
        if attributes is not None:
            attribute_items = ''
            for index, attribute in enumerate(attributes):
                if 0 < index:
                    attribute_items += "\n    "
                attribute_items += attribute.replace("\n", "\n    ")
                if index < len(attributes) - 1:
                    attribute_items += ','
            items_json = f"""
"items": {{
  "oneOf": [
    {attribute_items}
  ]
}},
"""
        value_additional = f""""minItems": 1,{contains_json}{items_json}
"uniqueItemProperties": [ "key" ]
"""
        return Attribute.json_schema(key=key, title=title, attribute_name=f"{group_name} group", description=description,
                                     type_name=AttributeType.TYPE_NAME_LIST, value_additional=value_additional)
