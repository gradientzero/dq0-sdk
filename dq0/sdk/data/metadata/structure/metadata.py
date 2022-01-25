import os

from dq0.sdk.data.metadata.specification.specification import Specification
from dq0.sdk.data.metadata.specification.specification_factory import SpecificationFactory
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_factory import NodeFactory

import yaml


class Metadata:
    ROOT_KEYS = {'dataset'}

    @staticmethod
    def from_yaml_file(filename, role_uuids=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find {filename}")
        with open(filename, 'r') as file:
            return Metadata.from_yaml(yaml_content=file, role_uuids=role_uuids)

    @staticmethod
    def from_yaml(yaml_content, role_uuids=None):
        yaml_dict = yaml.load(stream=yaml_content, Loader=yaml.FullLoader)
        nodes = {}
        specifications = {}
        for root_key in Metadata.ROOT_KEYS:
            yaml_key = f"meta_{root_key}"
            if yaml_key not in yaml_dict:
                continue
            node_dict = yaml_dict.pop(yaml_key, None)
            node, specification = Metadata.from_yaml_dict(yaml_dict=node_dict, role_uuids=role_uuids)
            nodes[root_key] = node
            specifications[root_key] = specification
        return Metadata(nodes=nodes, specifications=specifications)

    @staticmethod
    def from_yaml_dict(yaml_dict, role_uuids=None):
        if yaml_dict is None:
            return None, None
        format_type = yaml_dict.pop('format', None)
        node_dict = yaml_dict.pop('node', None)
        specification_string = yaml_dict.pop('specification', None)
        specification = SpecificationFactory.from_specification_string(specification_string=specification_string, role_uuids=role_uuids)
        return NodeFactory.from_yaml_content(yaml_content=node_dict, format_type=format_type, force_list=False), specification

    @staticmethod
    def check_nodes(nodes):
        if not isinstance(nodes, dict):
            raise Exception(f"nodes is not of type dict, is of type {type(nodes)} instead")
        for key, node in nodes.items():
            if key not in Metadata.ROOT_KEYS:
                raise Exception(f"key {key} is not in root keys {Metadata.ROOT_KEYS}")
            if not isinstance(node, Node):
                raise Exception(f"node is not of type Node, is of type {type(node)} instead")

    @staticmethod
    def check_specifications(specifications, none_ok=False):
        if not isinstance(specifications, dict):
            raise Exception(f"specifications is not of type dict, is of type {type(specifications)} instead")
        for key, specification in specifications.items():
            if key not in Metadata.ROOT_KEYS:
                raise Exception(f"key {key} is not in root keys {Metadata.ROOT_KEYS}")
            if none_ok and specification is None:
                continue
            if not isinstance(specification, Specification):
                raise Exception(f"specification is not of type Specification, is of type {type(specification)} instead")
            Specification.check(specification=specification)

    @staticmethod
    def check_apply_verify(nodes, specifications):
        Metadata.check_nodes(nodes=nodes)
        Metadata.check_specifications(specifications=specifications)
        applied_nodes = {}
        for key, node in nodes.items():
            if key in specifications:
                applied_nodes[key] = specifications[key].apply_defaults(node=node)
                specifications[key].verify(node=applied_nodes[key])
            else:
                applied_nodes[key] = node
        return applied_nodes

    @staticmethod
    def merge_specifications(specifications_a, specifications_b):
        # b overwrites a; explicit none in b removes specification
        Metadata.check_specifications(specifications=specifications_a, none_ok=False)
        if specifications_b is None:
            return specifications_a
        Metadata.check_specifications(specifications=specifications_b, none_ok=True)
        merged_specifications = {}
        for root_key in Metadata.ROOT_KEYS:
            if root_key not in specifications_b:
                if root_key in specifications_a:
                    merged_specifications[root_key] = specifications_a[root_key]
            elif specifications_b[root_key] is not None:
                merged_specifications[root_key] = specifications_b[root_key]
        return merged_specifications

    def __init__(self, nodes, specifications={}):
        self._nodes = Metadata.check_apply_verify(nodes=nodes, specifications=specifications)
        self._specifications = specifications

    def __str__(self, request_uuids=set()):
        return_string = ''
        count = 0
        for root_key in sorted(Metadata.ROOT_KEYS):
            if root_key in self._nodes:
                count += 1
                return_string += f"meta_{root_key}" + ":\n  " + self.root_node_str(root_key=root_key, request_uuids=request_uuids).replace('\n', "\n  ")
                if count < len(self._nodes):
                    return_string += '\n'
        return return_string

    def __repr__(self):
        nodes_repr = '{'
        for root_key in sorted(Metadata.ROOT_KEYS):
            if root_key in self._nodes:
                nodes_repr += f"'{root_key}': {repr(self._nodes[root_key])}, "
        nodes_repr += '}'
        return f"Metadata(nodes={nodes_repr}, specifications={{}})"

    def __len__(self):
        return len(self._nodes)

    def get_node(self, root_key):
        if root_key not in self._nodes:
            return None
        return self._nodes[root_key]

    def get_specification(self, root_key):
        if root_key not in self._specifications:
            return None
        return self._specifications[root_key]

    def set_node(self, root_key, node, specification=None):
        if root_key not in Metadata.ROOT_KEYS:
            raise Exception(f"root_key {root_key} is not in root keys {Metadata.ROOT_KEYS}")
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        if isinstance(specification, Specification):
            self._specifications[root_key] = specification
        self._nodes[root_key] = node

    def delete_node(self, root_key):
        if root_key not in Metadata.ROOT_KEYS:
            raise Exception(f"root_key {root_key} is not in root keys {Metadata.ROOT_KEYS}")
        if root_key in self._nodes:
            del self._nodes[root_key]

    def root_node_str(self, root_key, request_uuids=set()):
        return_string = f"format: {NodeFactory.FORMAT_TYPE_SIMPLE}"
        node_string = self._nodes[root_key].__str__(request_uuids=request_uuids)
        if node_string is not None:
            return_string += "\nnode:\n  " + node_string.replace('\n', "\n  ")
        if root_key in self._specifications:
            return_string += '\n' + f"specification: '{self._specifications[root_key]}'"
        return return_string

    def apply_defaults_and_verify(self, specifications=None):
        specifications = Metadata.merge_specifications(specifications_a=self._specifications, specifications_b=specifications)
        copied_nodes = {key: node.copy() for key, node in self._nodes.items()}
        return Metadata(nodes=copied_nodes, specifications=specifications)

    def filter(self, filter_funcs, specifications=None):
        specifications = Metadata.merge_specifications(specifications_a=self._specifications, specifications_b=specifications)
        filtered_nodes = {}
        for root_key, node in self._nodes.items():
            if root_key in filter_funcs:
                filtered_nodes[root_key] = filter_funcs[root_key](node=node.copy())
            else:
                filtered_nodes[root_key] = node.copy()
        return Metadata(nodes=filtered_nodes, specifications=specifications)

    def to_dict(self, request_uuids=set(), full=True):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            (f"meta_{root_key}", self.root_node_to_dict(root_key=root_key, request_uuids=request_uuids, full=full))
            for root_key in self._nodes
        ] if tmp_value is not None}

    def root_node_to_dict(self, root_key, request_uuids=set(), full=True):
        if root_key not in self._nodes:
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('format', NodeFactory.FORMAT_TYPE_FULL if full else NodeFactory.FORMAT_TYPE_SIMPLE),
            ('node', self._nodes[root_key].to_dict(request_uuids=request_uuids, full=full)),
            ('specification', str(self._specifications[root_key]) if root_key in self._specifications else None),
        ] if tmp_value is not None}

    def to_yaml(self, request_uuids=set()):
        return yaml.dump(self.to_dict(request_uuids=request_uuids))

    def to_yaml_file(self, filename, request_uuids=set()):
        yaml_content = self.to_yaml(request_uuids=request_uuids)
        with open(filename, 'w') as file:
            file.write(yaml_content)

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=set(), specifications=None):
        if other is None:
            raise Exception("other is None")
        specifications = Metadata.merge_specifications(specifications_a=self._specifications, specifications_b=specifications)
        merged_nodes = {}
        for root_key in Metadata.ROOT_KEYS:
            node_a = self._nodes[root_key] if root_key in self._nodes else None
            node_b = other._nodes[root_key] if root_key in other._nodes else None
            if not isinstance(node_a, Node):
                if not isinstance(node_b, Node):
                    continue
                merged_nodes[root_key] = node_b.copy()
            elif not isinstance(node_b, Node):
                merged_nodes[root_key] = node_a.copy()
            else:
                merged_nodes[root_key] = node_a.merge_with(
                    other=node_b,
                    overwrite_value=overwrite_value,
                    overwrite_permissions=overwrite_permissions,
                    request_uuids=request_uuids)
        return Metadata(nodes=merged_nodes, specifications=specifications)
