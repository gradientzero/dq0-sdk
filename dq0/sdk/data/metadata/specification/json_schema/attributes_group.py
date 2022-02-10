from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute
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
        return Attribute.json_schema(key=key, attribute_name=f"{group_name} group", description=description,
                                     type_name=AttributeType.TYPE_NAME_LIST, additional_value=additional_value,
                                     additional_description=additional_description)

    @staticmethod
    def data(attributes, additional_contains=None, additional_description=''):
        contains = Attribute.json_schema(
            key='name',
            attribute_name='name',
            description="This item ensures that the 'name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        if additional_contains is not None:
            additional_contains.append(contains)
            contains = additional_contains
        return AttributesGroup.json_schema(
            key='data',
            group_name='data',
            description="The 'data' attributes group. This group is required.",
            additional_description=f"Requires a 'name' attribute.{additional_description}",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def differential_privacy(attributes, contains=None, additional_description=None):
        return AttributesGroup.json_schema(
            key='differential_privacy',
            group_name="differential privacy",
            description="The 'differential privacy' attributes group.",
            attributes=attributes,
            additional_description=additional_description,
            contains=contains)

    @staticmethod
    def private_sql(attributes):
        return AttributesGroup.json_schema(
            key='private_sql',
            group_name="private sql",
            description="The 'private sql' attributes group.",
            attributes=attributes)

    @staticmethod
    def private_sql_and_synthesis(attributes):
        return AttributesGroup.json_schema(
            key='private_sql_and_synthesis',
            group_name="private sql and synthesis",
            description="The 'private sql and synthesis' attributes group.",
            attributes=attributes)

    @staticmethod
    def private_synthesis(attributes):
        return AttributesGroup.json_schema(
            key='private_synthesis',
            group_name="private synthesis",
            description="The 'private synthesis' attributes group.",
            attributes=attributes)

    @staticmethod
    def machine_learning(attributes):
        return AttributesGroup.json_schema(
            key='machine_learning',
            group_name="machine learning",
            description="The 'machine learning' attributes group.",
            attributes=attributes)
