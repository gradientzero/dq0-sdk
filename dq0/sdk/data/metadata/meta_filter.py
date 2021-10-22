from dq0.sdk.data.metadata.meta_node import MetaNode
from dq0.sdk.data.metadata.section.meta_section import MetaSection
from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType


class MetaFilter:
    @staticmethod
    def check(node):
        if node is None:
            raise Exception("node is none")
        if not isinstance(node, MetaNode):
            raise Exception("node is not an instance of MetaNode")
        if node.type_name is None:
            raise Exception("node.type_name is none")

    @staticmethod
    def filter(node, retain_section_type_names=None):
        MetaFilter.check(node)
        node = node.copy()
        if retain_section_type_names is not None and node.sections is not None:
            retained_sections = []
            for section in node.sections:
                if section.type_name is None:
                    raise Exception("section.type_name is none")
                if section.type_name in retain_section_type_names:
                    retained_sections.append(section)
            node.sections = retained_sections
        if node.child_nodes is not None:
            modified_child_nodes = []
            for child_node in node.child_nodes:
                modified_child_nodes.append(MetaFilter.filter(child_node, retain_section_type_names))
            node.child_nodes = modified_child_nodes
        return node

    @staticmethod
    def filterMachineLearning(node):
        return MetaFilter.filter(node, [MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING])

    @staticmethod
    def filterSmartNoise(node):
        return MetaFilter.filter(node, [MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_INT, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_STRING])
