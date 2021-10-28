import os
import yaml

from dq0.sdk.data.metadata.node.node_factory import NodeFactory
from dq0.sdk.data.metadata.verifier import Verifier


class Metadata:
    @staticmethod
    def from_yaml_file(filename, apply_default_attributes=None, verify=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename) as file:
            return Metadata.from_yaml(yaml_content=file, apply_default_attributes=apply_default_attributes, verify=verify)  

    @staticmethod
    def from_yaml(yaml_content, apply_default_attributes=None, verify=None):
        yaml_dict = yaml.load(stream=yaml_content, Loader=yaml.FullLoader)
        return Metadata(root_node=NodeFactory.fromYamlDict(yaml_dict=yaml_dict, apply_default_attributes=apply_default_attributes), verify=verify)

    def __init__(self, root_node, verify=None):
        if verify is None:
            verify = Verifier.verify
        verify(root_node)
        self.root_node = root_node

    def filter(self, filter, verify=None):
        if filter is None:
            raise Exception("filter is None")
        return Metadata(root_node=filter(node=self.root_node), verify=verify)

    def to_dict(self):
        if self.root_node is None:
            return {}
        return self.root_node.to_dict()

    def to_yaml(self):
        return yaml.dump(self.to_dict())

    def merge_with(self, other, verify=None):
        if other is None:
            raise Exception("other is None")
        if other.root_node is None:
            raise Exception("other.root_node is None")
        return Metadata(root_node=self.root_node.merge_with(other.root_node), verify=verify)
