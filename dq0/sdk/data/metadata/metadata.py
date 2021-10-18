import os
import yaml

from dq0.sdk.data.metadata.meta_node import MetaNode
from dq0.sdk.data.metadata.meta_verifier import MetaVerifier


class Metadata:
    @staticmethod
    def from_yaml_file(filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename) as file:
            return Metadata.from_yaml(file)  

    @staticmethod
    def from_yaml(yaml_content):
        yaml_dict = yaml.load(yaml_content, Loader=yaml.FullLoader)
        return Metadata(MetaNode.fromYamlDict(yaml_dict))

    def __init__(self, root_node, verify=None):
        if verify is None:
            verify = MetaVerifier.verify
        verify(root_node)
        self.root_node = root_node

    def filter(self, filter):
        if filter is None:
            raise Exception("filter is None")
        return Metadata(filter(self.root_node))

    def to_dict(self):
        if self.root_node is None:
            return {}
        return self.root_node.to_dict()

    def merge_with(self, other):
        if other is None:
            raise Exception("other is None")
        if other.root_node is None:
            raise Exception("other.root_node is None")
        return Metadata(self.root_node.merge_with(other.root_node))
