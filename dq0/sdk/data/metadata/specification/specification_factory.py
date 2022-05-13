from dq0.sdk.data.metadata.specification.dataset.specification_version import SpecificationVersion as DatasetSpecificationVersion
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1 as DatasetSpecificationV1
from dq0.sdk.data.metadata.specification.run.specification_version import SpecificationVersion as RunSpecificationVersion
from dq0.sdk.data.metadata.specification.run.v1.specification_v1 import SpecificationV1 as RunSpecificationV1
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


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
        if node_type_name == NodeType.TYPE_NAME_DATASET:
            if not DatasetSpecificationVersion.is_valid_version(version=version):
                raise Exception(f"version {version} is invalid")
            if version == DatasetSpecificationVersion.VERSION_V1:
                return DatasetSpecificationV1(role_uuids=role_uuids)
            else:
                raise Exception(f"unknown version {version}")
        if node_type_name == NodeType.TYPE_NAME_RUN:
            if not RunSpecificationVersion.is_valid_version(version=version):
                raise Exception(f"version {version} is invalid")
            if version == RunSpecificationVersion.VERSION_V1:
                return RunSpecificationV1(role_uuids=role_uuids)
            else:
                raise Exception(f"unknown version {version}")
        else:
            raise Exception(f"unknown node_type_name {node_type_name}")
