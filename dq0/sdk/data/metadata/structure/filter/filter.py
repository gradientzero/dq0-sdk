from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node import Node


class Filter:
    # retain_nodes is a map[str, map[str, _]], mapping node_type_name to pairs of attribute_key, attribute_value
    # All specified pairs of attribute_key, attribute_value need to match for a node with type_name=node_type_name to be kept.
    # A single None node_type_name may be added to the map, which will apply the attribute pairs to all nodes and only keep those matching.
    # If the map of attribute pairs is None, all nodes with the corresponding node_type_name are kept.
    #
    # retain_attributes is a map[str, map[str, _]], mapping node_type_name to pairs of attribute_key, attribute_value
    # While this parameter has the same type as retain_nodes, its semantics are widely different.
    # Specified attribute pairs are kept for nodes of type=node_type_name. If node_type_name is None the pairs are kept for all nodes.
    # If attribute_value is None, attributes with the corresponding key are kept independent of their values.
    @staticmethod
    def filter(node, retain_nodes=None, retain_attributes=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        if not Filter.node_matches(node=node, retain_nodes=retain_nodes):
            return None
        filtered_attributes = Filter.filter_attributes(node_type_name=node.get_type_name(), attributes=node.get_attributes(),
                                                       retain_attributes=retain_attributes)
        filtered_child_nodes = Filter.filter_nodes(nodes=node.get_child_nodes(), retain_nodes=retain_nodes, retain_attributes=retain_attributes)
        return Node(type_name=node.get_type_name(), attributes=filtered_attributes, child_nodes=filtered_child_nodes, permissions=node.get_permissions())

    @staticmethod
    def filter_attributes(node_type_name, attributes, retain_attributes):
        filtered_attributes = []
        for attribute in attributes if attributes is not None else []:
            if Filter.attribute_matches(node_type_name=node_type_name, attribute=attribute, retain_attributes=retain_attributes):
                if retain_attributes is not None and attribute.get_type_name() == AttributeType.TYPE_NAME_LIST:
                    sub_retain_attributes = {key: value for key, value in [
                        (None, retain_attributes[None][attribute.get_key()]
                         if None in retain_attributes and retain_attributes[None] is not None and isinstance(
                             retain_attributes[None], dict) and attribute.get_key() in retain_attributes[None] else None),
                        (node_type_name, retain_attributes[node_type_name][attribute.get_key()] if node_type_name is not None and node_type_name in
                         retain_attributes and retain_attributes[node_type_name] is not
                         None and isinstance(retain_attributes[node_type_name], dict) and attribute.get_key() in retain_attributes[node_type_name] else None),
                    ] if key is not None or value is not None}
                    if len(sub_retain_attributes) == 0:
                        sub_retain_attributes = None
                    sub_filtered_attributes = Filter.filter_attributes(node_type_name=node_type_name, attributes=attribute.get_value(),
                                                                       retain_attributes=sub_retain_attributes)
                    if sub_filtered_attributes is not None:
                        filtered_attributes.append(AttributeList(key=attribute.get_key(), value=sub_filtered_attributes,
                                                                 permissions=attribute.get_permissions()))
                else:
                    filtered_attributes.append(attribute)
        if len(filtered_attributes) == 0:
            return None
        return filtered_attributes

    @staticmethod
    def attribute_matches(node_type_name, attribute, retain_attributes):
        Attribute.check(attribute=attribute, check_data=None)
        if retain_attributes is None:
            return True
        for tmp_node_type_name, tmp_attributes_map in retain_attributes.items():
            if tmp_node_type_name is None or tmp_node_type_name == node_type_name:
                if tmp_attributes_map is None:
                    return True
                if attribute.get_key() in tmp_attributes_map:
                    tmp_attributes_value = tmp_attributes_map[attribute.get_key()]
                    if tmp_attributes_value is None or (attribute.get_type_name() == AttributeType.TYPE_NAME_LIST and isinstance(
                            tmp_attributes_value, dict)) or tmp_attributes_value == attribute.value:
                        return True
        return False

    @staticmethod
    def filter_nodes(nodes, retain_nodes=None, retain_attributes=None):
        filtered_nodes = []
        for node in nodes if nodes is not None else []:
            if Filter.node_matches(node=node, retain_nodes=retain_nodes):
                filtered_nodes.append(Filter.filter(node=node, retain_nodes=retain_nodes, retain_attributes=retain_attributes))
        if len(filtered_nodes) == 0:
            return None
        return filtered_nodes

    @staticmethod
    def node_matches(node, retain_nodes):
        Node.check(node, allowed_type_names=None, allowed_permissions=None)
        if retain_nodes is None:
            return True
        for node_type_name, attributes_map in retain_nodes.items() if retain_nodes is not None else {}:
            if node_type_name is None or node_type_name == node.get_type_name():
                if attributes_map is None:
                    return True
                return Filter.attributes_match(attributes=node.get_attributes(), match_attributes=attributes_map)
        return False

    # match_attributes is a map[str, _] of attribute_keys to attribute_values
    @staticmethod
    def attributes_match(attributes, match_attributes):
        if attributes is None:
            return match_attributes is None
        for match_attribute_key, match_attribute_value in match_attributes.items() if match_attributes is not None else {}:
            found = False
            for tmp_attribute in attributes:
                if match_attribute_key is None or match_attribute_key == tmp_attribute.get_key():
                    found = True
                    if match_attribute_value is not None and match_attribute_value != tmp_attribute.value:
                        return False
            if not found:
                return False
        return True
