from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.specification.dataset.standard.dataset import Dataset
from dq0.sdk.data.metadata.specification.specification_type import SpecificationType
from dq0.sdk.data.metadata.specification.specification import Specification


class DatasetStandardSpecification(Specification):
    VERSION = 2021120201

    def check_version(version):
        if version is None:
            return
        if not isinstance(version, int):
            raise Exception(f"version {version} is not of type int, is of type {type(version)} instead")
        if version != DatasetStandardSpecification.VERSION:
            raise Exception(f"version {version} is incompatible with provided version {DatasetStandardSpecification.VERSION}")

    @staticmethod
    def check(specification):
        if not isinstance(specification, DatasetStandardSpecification):
            raise Exception(f"specification is not of type DatasetStandardSpecification, is of type {type(specification)} instead")
        DatasetStandardSpecification.check_version(specification.version)

    def __init__(self, role_uuids=None):
        super().__init__(
            node_type_name=NodeType.TYPE_NAME_DATASET,
            type_name=SpecificationType.TYPE_NAME_STANDARD,
            version=DatasetStandardSpecification.VERSION,
            apply_defaults_func=Dataset.apply_defaults,
            verify_func=Dataset.verify,
            role_uuids=role_uuids)
