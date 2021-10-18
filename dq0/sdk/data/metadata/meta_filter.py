from dq0.sdk.data.metadata.meta_node import MetaNode
from dq0.sdk.data.metadata.section.meta_section import MetaSection


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


class MetaFilterMachineLearning(MetaFilter):
    @staticmethod
    def filter(node):
        return super().filter(node, [MetaSection.TYPE_NAME_COLUMN_MACHINE_LEARNING])


class MetaFilterSmartNoise(MetaFilter):
    @staticmethod
    def filter(node):
        return super().filter(node, [MetaSection.TYPE_NAME_TABLE_SMART_NOISE, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_INT, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_STRING])