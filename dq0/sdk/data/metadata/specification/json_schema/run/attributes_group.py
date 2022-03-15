from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesGroup:
    @staticmethod
    def data(attributes):
        contains = [
            JsonSchemaAttribute.json_schema(
                key='name',
                attribute_name='name',
                description="This item ensures that the 'name' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='run_type_name',
                attribute_name='run type name',
                description="This item ensures that the 'run_type_name' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING
            )
        ]
        return JsonSchemaAttributesGroup.json_schema(
            key='data',
            group_name='data',
            description="The 'data' attributes group. This group is required.",
            additional_description="Requires 'name' and 'type_name' attributes.",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def sql(attributes):
        contains = JsonSchemaAttribute.json_schema(
            key='query_string',
            attribute_name='query string',
            description="This item ensures that the 'query_string' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        return JsonSchemaAttributesGroup.json_schema(
            key='sql',
            group_name='sql',
            description="The 'sql' attributes group.",
            additional_description="Requires the 'query string' attribute.",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def query_processor(attributes):
        contains = JsonSchemaAttribute.json_schema(
            key='processor_type_name',
            attribute_name='processor type name',
            description="This item ensures that the 'processor_type_name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        return JsonSchemaAttributesGroup.json_schema(
            key='query_processor',
            group_name='query processor',
            description="The 'query processor' attributes group.",
            additional_description="Requires the 'processor type name' attribute.",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def result_processor(attributes):
        contains = JsonSchemaAttribute.json_schema(
            key='processor_type_name',
            attribute_name='processor type name',
            description="This item ensures that the 'processor_type_name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        return JsonSchemaAttributesGroup.json_schema(
            key='result_processor',
            group_name='result processor',
            description="The 'result processor' attributes group.",
            additional_description="Requires the 'processor type name' attribute.",
            contains=contains,
            attributes=attributes)
