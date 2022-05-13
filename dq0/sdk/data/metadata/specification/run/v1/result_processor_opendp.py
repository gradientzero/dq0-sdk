from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.run.attribute import Attribute as JsonSchemaRunAttribute
from dq0.sdk.data.metadata.specification.json_schema.run.attributes_group import AttributesGroup as JsonSchemaRunAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class ResultProcessorOpenDP:
    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'result_processor': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.analyst_attribute(role_uuids=role_uuids)),
        })
        ResultProcessorOpenDP.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'type_name': ([AttributeType.TYPE_NAME_STRING], analyst_attribute),
            'epsilon': ([AttributeType.TYPE_NAME_FLOAT], analyst_attribute),
            'delta': ([AttributeType.TYPE_NAME_FLOAT], analyst_attribute),
        }, required_keys={'type_name'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].get_value() != 'opendp':
            raise Exception(f"result processor type_name value {type_name_attributes[0].get_value()} does not match 'opendp'")

    @staticmethod
    def json_schema():
        return JsonSchemaRunAttributesGroup.result_processor(
            attributes=[
                JsonSchemaRunAttribute.processor_type_name(
                    group_name='result_processor',
                    additional_value="\"const\": \"opendp\""
                ),
                JsonSchemaAttribute.json_schema(
                    key='epsilon',
                    attribute_name='epsilon',
                    description="The 'epsilon' attribute.",
                    type_name=AttributeType.TYPE_NAME_FLOAT
                ),
                JsonSchemaAttribute.json_schema(
                    key='delta',
                    attribute_name='delta',
                    description="The 'delta' attribute.",
                    type_name=AttributeType.TYPE_NAME_FLOAT
                )
            ]
        )
