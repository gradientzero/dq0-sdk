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
    def metadata_is_public(node_type_name):
        return JsonSchemaAttribute.json_schema(
            key='metadata_is_public',
            attribute_name='metadata is public',
            description=f"The 'metadata is public' attribute. Specifies whether the '{node_type_name}' metadata is public.",
            type_name=AttributeType.TYPE_NAME_BOOLEAN)

    @staticmethod
    def name(node_type_name):
        return JsonSchemaAttribute.json_schema(
            key='name',
            attribute_name='name',
            description=f"The 'name' attribute. Mandatory and required to be unique among all elements of type '{node_type_name}'.",
            type_name=AttributeType.TYPE_NAME_STRING
        )

    @staticmethod
    def privacy_level(node_type_name):
        additional_value = """"minimum": 0,
"maximum": 2"""
        return JsonSchemaAttribute.json_schema(
            key='privacy_level',
            attribute_name='privacy level',
            description=f"The 'privacy level' attribute. Sets the level of privacy protection for '{node_type_name}'. "
                "A child node's setting of 'privacy level' will take precedence for the respective child node. "
                "Allowed values are [0, 1, 2].",
            type_name=AttributeType.TYPE_NAME_INT,
            additional_value=additional_value)
