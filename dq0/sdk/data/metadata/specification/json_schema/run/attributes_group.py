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
                key='type_name',
                attribute_name='type name',
                description="This item ensures that the 'type_name' attribute is present.",
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
    def logging():
        contains = [
            JsonSchemaAttribute.json_schema(
                key='log_key_string',
                attribute_name='log key string',
                description="This item ensures that the 'log_key_string' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_output_path',
                attribute_name='tracker output path',
                description="This item ensures that the 'tracker_output_path' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_type',
                attribute_name='tracker type',
                description="This item ensures that the 'tracker_type' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING
            )
        ]
        attributes = [
            JsonSchemaAttribute.json_schema(
                key='log_key_string',
                attribute_name='log key string',
                description="The 'log_key_string' attribute is mandatory.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_output_path',
                attribute_name='tracker output path',
                description="The 'tracker_output_path' attribute is mandatory.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_type',
                attribute_name='tracker type',
                description="The 'tracker_type' attribute is mandatory.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_group_uuid',
                attribute_name='tracker group uuid',
                description="The 'tracker_group_uuid' attribute.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
            JsonSchemaAttribute.json_schema(
                key='tracker_run_uuid',
                attribute_name='tracker run uuid',
                description="The 'tracker_run_uuid' attribute.",
                type_name=AttributeType.TYPE_NAME_STRING
            ),
        ]
        return JsonSchemaAttributesGroup.json_schema(
            key='logging',
            group_name='logging',
            description="The 'logging' attributes group.",
            additional_description="Requires 'log_key_string', 'tracker_output_path', and 'tracker_type' attribute.",
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
            additional_description="Requires the 'query_string' attribute.",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def query_processor(attributes):
        contains = JsonSchemaAttribute.json_schema(
            key='type_name',
            attribute_name='type name',
            description="This item ensures that the 'type_name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        return JsonSchemaAttributesGroup.json_schema(
            key='query_processor',
            group_name='query processor',
            description="The 'query processor' attributes group.",
            additional_description="Requires the 'type_name' attribute.",
            contains=contains,
            attributes=attributes)

    @staticmethod
    def result_processor(attributes):
        contains = JsonSchemaAttribute.json_schema(
            key='type_name',
            attribute_name='type name',
            description="This item ensures that the 'type_name' attribute is present.",
            type_name=AttributeType.TYPE_NAME_STRING
        )
        return JsonSchemaAttributesGroup.json_schema(
            key='result_processor',
            group_name='result processor',
            description="The 'result processor' attributes group.",
            additional_description="Requires the 'type_name' attribute.",
            contains=contains,
            attributes=attributes)
