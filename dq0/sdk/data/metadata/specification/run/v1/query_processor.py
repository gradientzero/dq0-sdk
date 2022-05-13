from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.run.v1.query_processor_classic_dp import QueryProcessorClassicDP
from dq0.sdk.data.metadata.specification.run.v1.query_processor_dummy import QueryProcessorDummy
from dq0.sdk.data.metadata.specification.run.v1.query_processor_opendp import QueryProcessorOpenDP
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class QueryProcessor:
    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'query_processor': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.analyst_attribute(role_uuids=role_uuids)),
        })
        attribute_type_name = attribute.get_attribute(key='type_name')
        if not isinstance(attribute_type_name, AttributeString):
            raise Exception(f"attribute type_name is not of type AttributeString, is of type {type(attribute_type_name)} instead")
        if attribute_type_name.get_value() == 'dummy':
            return QueryProcessorDummy.verify(attribute=attribute, role_uuids=role_uuids)
        elif attribute_type_name.get_value() == 'opendp':
            return QueryProcessorOpenDP.verify(attribute=attribute, role_uuids=role_uuids)
        elif attribute_type_name.get_value() == 'classic_dp':
            return QueryProcessorClassicDP.verify(attribute=attribute, role_uuids=role_uuids)
        else:
            raise Exception(f"unknown query processor type_name {attribute_type_name.get_value()}")
