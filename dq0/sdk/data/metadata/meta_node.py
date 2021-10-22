from dq0.sdk.data.metadata.meta_node_type import MetaNodeType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaNode:
    @staticmethod
    def merge_many(lst_a, lst_b):
        if lst_a is None:
            return lst_b
        if lst_b is None:
            return lst_a
        merged = []
        for elem_a in lst_a:
            elem_merged = elem_a.copy()
            for elem_b in lst_b:
                if elem_a.merge_precheck_with(elem_b):
                    lst_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(elem_b)
                    break
            merged.append(elem_merged)
        for elem_b in lst_b:
            for elem_a in lst_a:
                if elem_b.merge_precheck_with(elem_a):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(self, type_name, name=None, description=None, is_public=False, connector=None, sections=None, child_nodes=None):
        if not MetaNodeType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name
        self.name = name
        self.description = description
        self.is_public = is_public
        self.connector = connector
        self.sections = sections
        self.child_nodes = child_nodes

    def copy(self):
        return MetaNode(
            self.type_name,
            self.name,
            self.description,
            self.is_public,
            self.connector.copy() if self.connector is not None else None,
            [section.copy() for section in self.sections] if self.sections is not None else None,
            [child_node.copy() for child_node in self.child_nodes] if self.child_nodes is not None else None,
            )

    def to_dict(self):
        return {k: v for k, v in [
            ('type_name', self.type_name),
            ('name', self.name),
            ('description', self.description),
            ('is_public', self.is_public),
            ('connector', self.connector.to_dict() if self.connector is not None else None),
            ('sections', [section.to_dict() for section in self.sections] if self.sections is not None else None),
            ('child_nodes', [child_node.to_dict() for child_node in self.child_nodes] if self.child_nodes is not None else None),
            ] if v is not None}

    def merge_precheck_with(self, other):
        if other is None or self.type_name != other.type_name or self.name != other.name:
            return False
        if self.description != other.description:
            raise Exception(f"nodes with same type_name {self.type_name} and name {self.name if self.name is not None else 'None'} cannot have diverging descriptions {self.description if self.description is not None else 'None'} <--> {other.description if other.description is not None else 'None'}")
        if self.is_public != other.is_public:
            raise Exception(f"nodes with same type_name {self.type_name} and name {self.name if self.name is not None else 'None'} cannot have diverging is_public flags {self.is_public} <--> {other.is_public}")
        if (self.connector is None and other.connector is not None) or (self.connector is not None and other.connector is None):
            raise Exception(f"nodes with same type_name {self.type_name} and name {self.name if self.name is not None else 'None'} cannot have diverging connectors, where one is None and the other is not or vice versa")
        return True

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge nodes that fail the precheck")
        merged = self.copy()
        merged.connector = self.connector.merge_with(other.connector) if self.connector is not None and other.connector is not None else None
        merged.sections = MetaSection.merge_many(self.sections, other.sections)
        merged.child_nodes = MetaNode.merge_many(self.child_nodes, other.child_nodes)
        return merged
