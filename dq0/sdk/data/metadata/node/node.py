from dq0.sdk.data.metadata.attribute.attribute import Attribute
from dq0.sdk.data.metadata.node.node_type import NodeType


class Node:
    @staticmethod
    def init_check_many(list):
        tmp_list = [tmp_elem for tmp_elem in list] if list is not None else []
        while 0 < len(tmp_list):
            elem_a = tmp_list.pop()
            if elem_a is None:
                raise Exception("node cannot be None")
            for elem_b in tmp_list:
                if elem_b is None:
                    raise Exception("node cannot be None")
                if elem_a.merge_check_with(other=elem_b):
                    raise Exception(f"mergeable nodes detected")

    @staticmethod
    def merge_check_many_with_many(list_a, list_b, overwrite=False):
        if list_a is None or len(list_a) == 0:
            return True
        if list_b is None or len(list_b) == 0:
            return True
        for elem_a in list_a:
            found_match = False
            for elem_b in list_b:
                if elem_a.merge_check_with(elem_b, overwrite=overwrite):
                    if found_match:
                        raise Exception("element matches more than one other element")
                    found_match = True
        return True

    @staticmethod
    def merge_many_with_many(list_a, list_b, overwrite=False):
        if list_a is None or len(list_a) == 0:
            return None if list_b is None or len(list_b) == 0 else list_b
        if list_b is None or len(list_b) == 0:
            return None if list_a is None or len(list_a) == 0 else list_a
        merged = []
        for elem_a in list_a:
            elem_merged = elem_a.copy()
            for elem_b in list_b:
                if elem_a.merge_check_with(other=elem_b, overwrite=overwrite):
                    list_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(other=elem_b, overwrite=overwrite)
                    break
            merged.append(elem_merged)
        for elem_b in list_b:
            for elem_a in list_a:
                if elem_b.merge_check_with(other=elem_a, overwrite=overwrite):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, attributes=None, child_nodes=None):
        if not NodeType.isValidTypeName(type_name=type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        Attribute.init_check_many(list=attributes)
        Node.init_check_many(list=child_nodes)
        self.type_name = type_name
        self.attributes = attributes
        self.child_nodes = child_nodes

    def copy(self):
        return Node(
            type_name=self.type_name,
            attributes=[tmp_attribute.copy() for tmp_attribute in self.attributes] if self.attributes is not None else None,
            child_nodes=[tmp_child_node.copy() for tmp_child_node in self.child_nodes] if self.child_nodes is not None else None,
            )

    def to_dict(self):
        return {tmp_key: tmp_value for tmp_key, tmp_value in [
            ('type_name', self.type_name),
            ('attributes', [tmp_attribute.to_dict() for tmp_attribute in self.attributes] if self.attributes is not None else None),
            ('child_nodes', [tmp_child_node.to_dict() for tmp_child_node in self.child_nodes] if self.child_nodes is not None else None),
            ] if tmp_value is not None}

    def merge_check_with(self, other, overwrite=False):
        return not (other is None or self.type_name != other.type_name or not Attribute.merge_check_many_with_many(list_a=self.attributes, list_b=other.attributes, overwrite=overwrite) or not Node.merge_check_many_with_many(list_a=self.child_nodes, list_b=other.childnodes, overwrite=overwrite))

    def merge_with(self, other, overwrite=False):
        if not self.merge_check_with(other):
            raise Exception("cannot merge nodes that fail the merge check")
        merged = self.copy()
        merged.attributes = Attribute.merge_many_with_many(list_a=self.attributes, list_b=other.attributes, overwrite=overwrite)
        merged.child_nodes = Node.merge_many_with_many(list_a=self.child_nodes, list_b=other.child_nodes, overwrite=overwrite)
        return merged

    def get_attribute(self, key):
        for tmp_attribute in self.attributes if self.attributes is not None else []:
            if tmp_attribute.key == key:
                return tmp_attribute
        return None
