import os
import yaml

from dq0.sdk.data.metadata.node.node_factory import NodeFactory
from dq0.sdk.data.metadata.verifier import Verifier


class Metadata:
    @staticmethod
    def from_yaml_file(filename, apply_default_attributes=None, verify_func=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename) as file:
            return Metadata.from_yaml(yaml_content=file, apply_default_attributes=apply_default_attributes, verify_func=verify_func)  

    @staticmethod
    def from_yaml(yaml_content, apply_default_attributes=None, verify_func=None):
        yaml_dict = yaml.load(stream=yaml_content, Loader=yaml.FullLoader)
        return Metadata(root_node=NodeFactory.fromYamlDict(yaml_dict=yaml_dict, apply_default_attributes=apply_default_attributes), verify_func=verify_func)

    def __init__(self, root_node, verify_func=None):
        if verify_func is None:
            verify_func = Verifier.verify
        verify_func(root_node)
        self.root_node = root_node

    def __str__(self):
        return str(self.root_node)

    def __repr__(self):
        return "Metadata(root_node=" + repr(self.root_node) + ", verify_func=None)"

    def filter(self, filter_func, verify_func=None):
        if filter_func is None:
            raise Exception("filter_func is None")
        return Metadata(root_node=filter_func(node=self.root_node), verify_func=verify_func)

    def to_dict(self):
        if self.root_node is None:
            return {}
        return self.root_node.to_dict()

    def to_yaml(self):
        return yaml.dump(self.to_dict())

    def merge_with(self, other, verify_func=None):
        if other is None:
            raise Exception("other is None")
        if other.root_node is None:
            raise Exception("other.root_node is None")
        print("==================================================================================================================================")
        print("==================================================================================================================================")
        return Metadata(root_node=self.root_node.merge_with(other.root_node), verify_func=verify_func)
