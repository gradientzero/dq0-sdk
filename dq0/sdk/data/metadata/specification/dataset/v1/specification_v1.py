from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.specification_version import SpecificationVersion
from dq0.sdk.data.metadata.specification.dataset.v1.dataset import Dataset
from dq0.sdk.data.metadata.specification.specification import Specification


class SpecificationV1(Specification):
    def check_version(version):
        if not SpecificationVersion.is_valid_version(version=version):
            raise Exception(f"version {version} is invalid")
        if version != SpecificationVersion.VERSION_V1:
            raise Exception(f"version mismatch {version} != {SpecificationVersion.VERSION_V1}")

    @staticmethod
    def check(specification):
        if not isinstance(specification, SpecificationV1):
            raise Exception(f"specification is not of type SpecificationV1, is of type {type(specification)} instead")
        SpecificationV1.check_version(specification.version)

    def __init__(self, role_uuids=None):
        super().__init__(
            node_type_name=NodeType.TYPE_NAME_DATASET,
            version=SpecificationV1.VERSION,
            apply_defaults_func=Dataset.apply_defaults,
            verify_func=Dataset.verify,
            role_uuids=role_uuids)
