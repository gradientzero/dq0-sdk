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
