from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.explanation import Explanation
from dq0.sdk.data.metadata.merge_exception import MergeException
from dq0.sdk.data.metadata.node.node_type import NodeType
from dq0.sdk.data.metadata.permissions.action import Action
from dq0.sdk.data.metadata.permissions.permissions import Permissions
from dq0.sdk.data.metadata.utils import Utils as MetaUtils


class Node:
    @staticmethod
    def check(node, allowed_type_names=None, allowed_permissions=None):
        if not isinstance(node, Node):
            raise Exception(f"node is not of type Node, is of type {type(node)} instead")
        if not NodeType.is_valid_type_name(type_name=node.type_name):
            raise Exception(f"node.type_name {node.type_name} is not valid")
        if allowed_type_names is not None and node.type_name not in allowed_type_names:
            raise Exception(f"node.type_name {node.type_name} is not in allowed_type_names {allowed_type_names}")
        if not Permissions.is_subset_of(permissions_a=node.permissions, permissions_b=allowed_permissions):
            raise Exception(f"node.permissions {node.permissions} are not in allowed_permissions {allowed_permissions}")

    @staticmethod
    def check_list(node_list, allowed_type_names=None, allowed_permissions=None):
        if node_list is None:
            return
        if not isinstance(node_list, list):
            raise Exception(f"node_list is not of type list, is of type {type(node_list)} instead")
        for node in node_list:
            Node.check(node=node, allowed_type_names=allowed_type_names, allowed_permissions=allowed_permissions)

    @staticmethod
    def check_list_merge_duplicates(node_list, allowed_type_names=None, allowed_permissions=None):
        Node.check_list(node_list=node_list, allowed_type_names=allowed_type_names, allowed_permissions=allowed_permissions)
        tmp_list = node_list.copy() if node_list is not None else []
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            for elem_b in tmp_list:
                try:
                    if elem_a.is_mergeable_with(other=elem_b, overwrite_value=False, overwrite_permissions=False, request_uuids=None):
                        raise Exception("mergeable nodes:\n" + str(elem_a) + "\nand:\n" + str(elem_b) + "\ndetected in:\n" + str(list))
                except: MergeException

    @staticmethod
    def are_merge_compatible(node_list_a, node_list_b, explanation=None):
        Node.check_list(node_list=node_list_a, allowed_type_names=None, allowed_permissions=None)
        Node.check_list(node_list=node_list_b, allowed_type_names=None, allowed_permissions=None)
        if node_list_a is None or len(node_list_a) == 0 or node_list_b is None or len(node_list_b) == 0:
            return True
        for elem_a in node_list_a:
            for elem_b in node_list_b:
                if not elem_a.is_merge_compatible_with(other=elem_b, explanation=explanation):
                    Explanation.dynamic_add_message(explanation=explanation, message=f"Node.are_merge_compatible(...): nodes[{elem_a.type_name}] are not compatible")
                    return False
        return True

    @staticmethod
    def are_mergeable(list_a, list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=[], explanation=None):
        if not Node.are_merge_compatible(node_list_a=list_a, node_list_b=list_b):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node.are_mergeable(...): nodes are not compatible")
            return False
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=None):
                    if found_match:
                        Explanation.dynamic_add_message(explanation=explanation, message=f"Node.are_mergeable(...): duplicate mergeable nodes[{elem_a.type_name}] are not allowed")
                        return False
                    found_match = True
        return True

    @staticmethod
    def merge_many(list_a, list_b, overwrite_value=False, overwrite_permissions=False, request_uuids=[]):
        explanation = Explanation()
        if not Node.are_mergeable(list_a=list_a, list_b=list_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge nodes that are not mergeable; list_a: {list_a} list_b: {list_b} explanation: {explanation}")
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        tmp_list_b = list_b.copy()
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in tmp_list_b:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids):
                    tmp_list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
                    break
            merged.append(elem_merged)
        for elem_b in tmp_list_b:
            for elem_a in list_a:
                if elem_a.is_mergeable_with(other=elem_b, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, attributes=None, child_nodes=None, permissions=None):
        if not NodeType.is_valid_type_name(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if Attribute.check_list(attribute_list=attributes, allowed_keys_type_names_permissions=None):
            raise Exception("node may not have list of attributes with multiple null keys")
        Node.check_list_merge_duplicates(node_list=child_nodes, allowed_type_names=None, allowed_permissions=None)
        Permissions.check(permissions=permissions)
        self.type_name = type_name
        self.attributes = attributes
        self.child_nodes = child_nodes
        for index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            tmp_child_node.list_index = index if 1 < len(self.child_nodes) else -1
        self.permissions = permissions
        self.list_index = -1

    def __str__(self, request_uuids=[]):
        if not Permissions.is_allowed_with(permissions=self.permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        index_string = f"_{self.list_index}" if -1 < self.list_index else ''
        return_string = MetaUtils.str_from(object=self.type_name, quoted=False) + index_string + ':'
        if self.attributes is not None and len(self.attributes) > 0:
            return_string += "\n  attributes:" + MetaUtils.restricted_str_from_list(list=self.attributes, sort=False, request_uuids=request_uuids).replace('\n', "\n  ")
        if self.child_nodes is not None and len(self.child_nodes) > 0:
            return_string += "\n  child_nodes:" + MetaUtils.restricted_str_from_list(list=self.child_nodes, sort=False, request_uuids=request_uuids).replace('\n', "\n    ")
        return return_string

    def __repr__(self):
        return "Node(" + \
            "type_name=" + repr(self.type_name) + ", " + \
            "attributes=" + repr(self.attributes) + ", " + \
            "child_nodes=" + repr(self.child_nodes) + ", " + \
            "permissions=" + repr(self.permissions) + ')'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if not MetaUtils.list_equals_unordered(list_a=self.attributes, list_b=other.attributes):
            return False
        if not MetaUtils.list_equals_unordered(list_a=self.child_nodes, list_b=other.child_nodes):
            return False
        return \
            self.type_name == other.type_name and \
            self.permissions == other.permissions

    def copy(self):
        copied_node = Node(
                type_name=self.type_name,
                attributes=[tmp_attribute.copy() for tmp_attribute in self.attributes] if self.attributes is not None else None,
                child_nodes=[tmp_child_node.copy() for tmp_child_node in self.child_nodes] if self.child_nodes is not None else None,
                permissions=self.permissions.copy() if self.permissions is not None else None
            )
        copied_node.list_index = self.list_index
        return copied_node

    def to_dict(self, request_uuids=[]):
        if not Permissions.is_allowed_with(permissions=self.permissions, action=Action.READ, request_uuids=request_uuids):
            return None
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
                ('type_name', self.type_name),
                ('attributes', MetaUtils.list_map_to_dict(self.attributes, request_uuids=request_uuids)),
                ('child_nodes', MetaUtils.list_map_to_dict(self.child_nodes, request_uuids=request_uuids)),
                ('permissions', self.permissions.to_dict() if self.permissions is not None else None),
            ] if tmp_value is not None}

    def is_merge_compatible_with(self, other, explanation=None):
        if not isinstance(other, Node):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_merge_compatible_with(...): other is not of type Node, is of type {type(other)} instead")
            return False
        if self.type_name != other.type_name:
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_merge_compatible_with(...): type_name mismatch {self.type_name} != {other.type_name}")
            return False
        if not Attribute.are_merge_compatible(attribute_list_a=self.attributes, attribute_list_b=other.attributes, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_merge_compatible_with(...): attributes are not compatible")
            return False
        if not Node.are_merge_compatible(node_list_a=self.child_nodes, node_list_b=other.child_nodes, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_merge_compatible_with(...): child_nodes are not compatible")
            return False
        if not Permissions.are_merge_compatible(permissions_a=self.permissions, permissions_b=other.permissions):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_merge_compatible_with(...): permissions are not compatible")
            return False
        return True

    def is_mergeable_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[], explanation=None):
        if not self.is_merge_compatible_with(other=other, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): other is not compatible")            
            return False
        if not Attribute.are_mergeable(attribute_list_a=self.attributes, attribute_list_b=other.attributes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): attributes are not mergeable")            
            return False
        merged_attributes = Attribute.merge_many(attribute_list_a=self.attributes, attribute_list_b=other.attributes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        if self.attributes != merged_attributes and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_ATTRIBUTES, request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): writing attributes without write_attributes permission is not allowed")            
            return False
        if not Node.are_mergeable(list_a=self.child_nodes, list_b=other.child_nodes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): child_nodes are not mergeable")            
            return False
        merged_child_nodes = Node.merge_many(list_a=self.child_nodes, list_b=other.child_nodes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        if self.child_nodes != merged_child_nodes and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_CHILD_NODES, request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): writing child_nodes without write_child_nodes permission is not allowed")            
            return False
        if not Permissions.are_mergeable(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions, explanation=explanation):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): permissions are not mergeable")            
            return False
        merged_permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)
        if self.permissions != merged_permissions and not Permissions.is_allowed_with(permissions=self.permissions, action=Action.WRITE_PERMISSIONS, request_uuids=request_uuids):
            Explanation.dynamic_add_message(explanation=explanation, message=f"Node[{self.type_name}].is_mergeable_with(...): writing permissions without write_permissions permission is not allowed")            
            return False
        return True

    def merge_with(self, other, overwrite_value=False, overwrite_permissions=False, request_uuids=[]):
        explanation = Explanation()
        if not self.is_mergeable_with(other=other, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids, explanation=explanation):
            raise MergeException(f"cannot merge nodes that are not mergeable; self: {self} other: {other} explanation: {explanation}")
        merged = self.copy()
        merged.attributes = Attribute.merge_many(attribute_list_a=self.attributes, attribute_list_b=other.attributes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        merged.child_nodes = Node.merge_many(list_a=self.child_nodes, list_b=other.child_nodes, overwrite_value=overwrite_value, overwrite_permissions=overwrite_permissions, request_uuids=request_uuids)
        for index, tmp_child_node in enumerate(merged.child_nodes if merged.child_nodes is not None else []):
            tmp_child_node.list_index = index if 1 < len(merged.child_nodes) else -1
        merged.list_index = -1
        merged.permissions = Permissions.merge(permissions_a=self.permissions, permissions_b=other.permissions, overwrite=overwrite_permissions)
        return merged

    def get_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            return None
        for tmp_index, tmp_attribute in enumerate(self.attributes if self.attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                return tmp_attribute
        return None

    def add_attribute(self, attribute, index=-1):
        if attribute is None:
            raise Exception("attribute is none")
        if self.get_attribute(index=index, key=attribute.key, value=attribute.value) is not None:
            raise Exception("duplicate attributes not allowed")            
        if self.attributes is None:
            self.attributes = []
        if Attribute.check_list_and_is_explicit_list(list=self.attributes, additional=attribute):
            raise Exception("node may not have list of attributes with multiple null keys")
        if index < 0:
            index = len(self.attributes)
        self.attributes.insert(index, attribute)

    def remove_attribute(self, index=-1, key=None, value=None):
        if index < 0 and key is None and value is None:
            raise Exception("attribute not found")
        for tmp_index, tmp_attribute in enumerate(self.attributes if self.attributes is not None else []):
            if (index < 0 or index == tmp_index) and (key is None or key == tmp_attribute.key) and (value is None or value == tmp_attribute.value):
                del self.attributes[tmp_index]
                return
        raise Exception("attribute not found")

    def matches_attribute_map(self, attributes_map):
        for tmp_key, tmp_value in attributes_map.items() if attributes_map is not None else {}:
            if self.get_attribute(index=-1, key=tmp_key, value=tmp_value) is None:
                return False
        return True

    def get_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            return None
        for tmp_index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or tmp_child_node.matches_attribute_map(attributes_map=attributes_map)):
                return tmp_child_node
        return None

    def add_child_node(self, child_node, index=-1):
        if child_node is None:
            raise Exception("child_node is none")
        if self.get_child_node(index=index, attributes_map=child_node.attributes) is not None:
            raise Exception("duplicate child_nodes not allowed")
        if self.child_nodes is None:
            self.child_nodes = []
        if index < 0:
            index = len(self.child_nodes)
        self.child_nodes.insert(index, child_node)
        for index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            tmp_child_node.list_index = index if 1 < len(self.child_nodes) else -1

    def remove_child_node(self, index=-1, attributes_map=None):
        if index < 0 and attributes_map is None:
            raise Exception("child_node not found")
        for tmp_index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
            if (index < 0 or index == tmp_index) and (attributes_map is None or tmp_child_node.matches_attribute_map(attributes_map=attributes_map)):
                del self.child_nodes[tmp_index]
                for index, tmp_child_node in enumerate(self.child_nodes if self.child_nodes is not None else []):
                    tmp_child_node.list_index = index if 1 < len(self.child_nodes) else -1
                return
        raise Exception("child_node not found")
