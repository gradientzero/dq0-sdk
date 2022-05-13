from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class Attribute:
    @staticmethod
    def description(node_type_name):
        return JsonSchemaAttribute.json_schema(
            key='description',
            attribute_name='description',
            description=f"The 'description' attribute. Describes the '{node_type_name}'.",
            type_name=AttributeType.TYPE_NAME_STRING)

    @staticmethod
    def name(node_type_name):
        return JsonSchemaAttribute.json_schema(
            key='name',
            attribute_name='name',
            description=f"The 'name' attribute. Mandatory for elements of type '{node_type_name}'.",
            type_name=AttributeType.TYPE_NAME_STRING
        )

    @staticmethod
    def run_type_name(node_type_name, additional_value):
        return JsonSchemaAttribute.json_schema(
            key='type_name',
            attribute_name='type name',
            description=f"The 'type name' attribute. Specifies the type of '{node_type_name}' and is mandatory.",
            type_name=AttributeType.TYPE_NAME_STRING,
            additional_value=additional_value
        )

    @staticmethod
    def query_string():
        return JsonSchemaAttribute.json_schema(
            key='query_string',
            attribute_name='query string',
            description="The 'query string' attribute. Specifies the input sql and is mandatory.",
            type_name=AttributeType.TYPE_NAME_STRING
        )

    @staticmethod
    def processor_type_name(group_name, additional_value):
        return JsonSchemaAttribute.json_schema(
            key='type_name',
            attribute_name='type name',
            description=f"The 'type name' attribute. Specifies the type of '{group_name}' and is mandatory.",
            type_name=AttributeType.TYPE_NAME_STRING,
            additional_value=additional_value
        )
