from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.run.attribute import Attribute as JsonSchemaRunAttribute
from dq0.sdk.data.metadata.specification.json_schema.run.attributes_group import AttributesGroup as JsonSchemaRunAttributesGroup
from dq0.sdk.data.metadata.specification.run.v1.query_processor import QueryProcessor
from dq0.sdk.data.metadata.specification.run.v1.query_processor_dummy import QueryProcessorDummy
from dq0.sdk.data.metadata.specification.run.v1.query_processor_opendp import QueryProcessorOpenDP
from dq0.sdk.data.metadata.specification.run.v1.result_processor import ResultProcessor
from dq0.sdk.data.metadata.specification.run.v1.result_processor_dummy import ResultProcessorDummy
from dq0.sdk.data.metadata.specification.run.v1.result_processor_opendp import ResultProcessorOpenDP
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class Sql:
    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'sql': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.analyst_attribute(role_uuids=role_uuids)),
        })
        Sql.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'query_string': ([AttributeType.TYPE_NAME_STRING], analyst_attribute),
            'query_processor': ([AttributeType.TYPE_NAME_LIST], analyst_attribute),
            'result_processor': ([AttributeType.TYPE_NAME_LIST], analyst_attribute),
        }, required_keys={'query_string'})
        query_processor_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'query_processor'] \
            if attributes is not None else []
        if 0 < len(query_processor_attributes):
            QueryProcessor.verify(attribute=query_processor_attributes[0], role_uuids=role_uuids)
        result_processor_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'result_processor'] \
            if attributes is not None else []
        if 0 < len(result_processor_attributes):
            ResultProcessor.verify(attribute=result_processor_attributes[0], role_uuids=role_uuids)

    @staticmethod
    def json_schema():
        return JsonSchemaRunAttributesGroup.sql(
            attributes=[
                JsonSchemaRunAttribute.query_string(),
                QueryProcessorDummy.json_schema(),
                QueryProcessorOpenDP.json_schema(),
                ResultProcessorDummy.json_schema(),
                ResultProcessorOpenDP.json_schema()
            ]
        )
