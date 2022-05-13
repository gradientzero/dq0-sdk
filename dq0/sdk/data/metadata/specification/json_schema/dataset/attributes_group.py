from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesGroup:
    @staticmethod
    def data(attributes, additional_contains=None, additional_description=''):
        contains = JsonSchemaAttribute.json_schema(
            key='name',
            attribute_name='name',
            description="This item ensures that the 'name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        if additional_contains is not None:
            additional_contains.append(contains)
            contains = additional_contains
        return JsonSchemaAttributesGroup.json_schema(
            key='data',
            group_name='data',
            description="The 'data' attributes group. This group is required.",
            additional_description=f"Requires a 'name' attribute.{additional_description}",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def differential_privacy(attributes, contains=None, additional_description=None):
        return JsonSchemaAttributesGroup.json_schema(
            key='differential_privacy',
            group_name="differential privacy",
            description="The 'differential privacy' attributes group.",
            attributes=attributes,
            additional_description=additional_description,
            contains=contains)

    @staticmethod
    def private_sql(attributes):
        return JsonSchemaAttributesGroup.json_schema(
            key='private_sql',
            group_name="private sql",
            description="The 'private sql' attributes group.",
            attributes=attributes)

    @staticmethod
    def private_sql_and_synthesis(attributes):
        return JsonSchemaAttributesGroup.json_schema(
            key='private_sql_and_synthesis',
            group_name="private sql and synthesis",
            description="The 'private sql and synthesis' attributes group.",
            attributes=attributes)

    @staticmethod
    def private_synthesis(attributes):
        return JsonSchemaAttributesGroup.json_schema(
            key='private_synthesis',
            group_name="private synthesis",
            description="The 'private synthesis' attributes group.",
            attributes=attributes)

    @staticmethod
    def machine_learning(attributes):
        return JsonSchemaAttributesGroup.json_schema(
            key='machine_learning',
            group_name="machine learning",
            description="The 'machine learning' attributes group.",
            attributes=attributes)
