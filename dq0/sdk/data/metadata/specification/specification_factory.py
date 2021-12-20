from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.specification_version import SpecificationVersion
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1 as DatasetSpecificationV1


class SpecificationFactory:
    @staticmethod
    def from_specification_string(specification_string, role_uuids=None):
        if specification_string is None:
            return None
        string_list = specification_string.split('_')
        if len(string_list) != 2:
            raise Exception(f"specification_string {specification_string} does not consist of two parts separated by underscore")
        node_type_name = string_list[0]
        version = string_list[1]
        return SpecificationFactory.from_type_and_version(node_type_name=node_type_name, version=version, role_uuids=role_uuids)

    @staticmethod
    def from_type_and_version(node_type_name, version, role_uuids=None):
        if not NodeType.is_valid_type_name(type_name=node_type_name):
            raise Exception(f"node_type_name {node_type_name} is invalid")
        if not SpecificationVersion.is_valid_version(version=version):
            raise Exception(f"version {version} is invalid")
        if node_type_name == NodeType.TYPE_NAME_DATASET:
            if version == SpecificationVersion.VERSION_V1:
                return DatasetSpecificationV1(role_uuids=role_uuids)
            else:
                raise Exception(f"unknown version {version}")
        else:
            raise Exception(f"unknown node_type_name {node_type_name}")
