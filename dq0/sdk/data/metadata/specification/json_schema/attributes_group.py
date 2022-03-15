from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesGroup:
    @staticmethod
    def json_schema(key, group_name, description, additional_description=None, contains=None, attributes=None):
        contains_json = ''
        if contains is not None:
            if isinstance(contains, list):
                contains_json = "\n\"allOf\": [\n  {\n    "
                for index, contains_item in enumerate(contains):
                    indented_contains = contains_item.replace("\n", "\n    ")
                    contains_json += f"\"contains\": {indented_contains}"
                    if index < len(contains) - 1:
                        contains_json += ",\n    "
                contains_json += "\n  }\n],"
            else:
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
}},"""
        additional_value = f""""minItems": 1,{contains_json}{items_json}
"uniqueItemProperties": [ "key" ]"""
        return JsonSchemaAttribute.json_schema(
            key=key, attribute_name=f"{group_name} group", description=description,
            type_name=AttributeType.TYPE_NAME_LIST, additional_value=additional_value,
            additional_description=additional_description)
