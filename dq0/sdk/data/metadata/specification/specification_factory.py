from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.multi.dataset_multi_specification import DatasetMultiSpecification
from dq0.sdk.data.metadata.specification.dataset.standard.dataset_standard_specification import DatasetStandardSpecification
from dq0.sdk.data.metadata.specification.specification_type import SpecificationType


class SpecificationFactory:
    @staticmethod
    def check_version(version):
        if version is None:
            return
        if not isinstance(version, int):
            raise Exception(f"version {version} is not of type int, is of type {type(version)} instead")

    @staticmethod
    def from_specification_string(specification_string, role_uuids=None):
        if specification_string is None:
            return None
        string_list = specification_string.split('_')
        if len(string_list) != 3:
            raise Exception(f"specification_string {specification_string} does not consist of three parts separated by underscore")
        node_type_name = string_list[0]
        type_name = string_list[1]
        version = int(string_list[2])
        return SpecificationFactory.from_types_and_version(node_type_name=node_type_name, type_name=type_name, version=version, role_uuids=role_uuids)

    @staticmethod
    def from_types_and_version(node_type_name, type_name, version, role_uuids=None):
        if not SpecificationType.is_valid_type_name(type_name=type_name):
            raise Exception(f"type_name {type_name} is invalid")
        if not NodeType.is_valid_type_name(type_name=node_type_name):
            raise Exception(f"node_type_name {node_type_name} is invalid")
        if node_type_name == NodeType.TYPE_NAME_DATASET:
            if type_name == SpecificationType.TYPE_NAME_STANDARD:
                DatasetStandardSpecification.check_version(version=version)
                return DatasetStandardSpecification(role_uuids=role_uuids)
            elif type_name == SpecificationType.TYPE_NAME_MULTI:
                return DatasetMultiSpecification(role_uuids=role_uuids)
            else:
                raise Exception(f"unknown type_name {type_name}")
        else:
            raise Exception(f"unknown node_type_name {node_type_name}")
