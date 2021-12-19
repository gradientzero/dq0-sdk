from dq0.sdk.data.metadata.metadata import Metadata


class meta:
    def __init__(self, metadata, dataset_specification=None, other_specification=None):
        if not isinstance(metadata, Metadata):
            raise Exception(f"metadata is not of type Metadata, is of type {type(metadata)} instead")
        if metadata.dataset_node is not None and dataset_specification is None:
            raise Exception("dataset_specification missing")
        self.dataset_specification = dataset_specification
        if dataset_specification is not None:
            dataset_specification.verify(node=metadata.dataset_node)
        if metadata.other_node is not None and other_specification is None:
            raise Exception("other_specification missing")
        self.other_specification = other_specification
        if other_specification is not None:
            other_specification.verify(node=metadata.other_node)
        self.metadata = metadata
