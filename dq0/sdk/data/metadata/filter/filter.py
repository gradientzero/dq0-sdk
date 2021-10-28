from dq0.sdk.data.metadata.node.node import Node


class Filter:
    @staticmethod
    def check(node):
        if node is None:
            raise Exception("node is none")
        if not isinstance(node, Node):
            raise Exception("node is not an instance of MetaNode")
        if node.type_name is None:
            raise Exception("node.type_name is none")

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
        Filter.check(node=node)
        if not Filter.node_matches(node=node, retain_nodes=retain_nodes):
            return None
        node = node.copy()
        node.attributes = Filter.filter_attributes(node_type_name=node.type_name, attributes=node.attributes, retain_attributes=retain_attributes)
        node.child_nodes = Filter.filter_nodes(nodes=node.child_nodes, retain_nodes=retain_nodes)
        return node

    @staticmethod
    def filter_attributes(node_type_name, attributes, retain_attributes):
        filtered_attributes = []
        for tmp_attribute in attributes if attributes is not None else []:
            if Filter.attribute_matches(node_type_name=node_type_name, attribute=tmp_attribute, retain_attributes=retain_attributes):
                filtered_attributes.append(tmp_attribute)
        if len(filtered_attributes) == 0:
            return None
        return filtered_attributes

    @staticmethod
    def attribute_matches(node_type_name, attribute, retain_attributes):
        if attribute is None:
            return retain_attributes is None
        if retain_attributes is None:
            return True
        for tmp_node_type_name, tmp_attributes_map in retain_attributes:
            if tmp_node_type_name is None or tmp_node_type_name == node_type_name:
                if attribute.key in tmp_attributes_map:
                    tmp_attributes_value = tmp_attributes_map[attribute.key]
                    return tmp_attributes_value is None or tmp_attributes_value == attribute.value
        return False

    @staticmethod
    def filter_nodes(nodes, retain_nodes):
        filtered_nodes = []
        for tmp_node in nodes if nodes is not None else []:
            if Filter.node_matches(node=tmp_node, retain_nodes=retain_nodes):
                filtered_nodes.append(tmp_node)
        if len(filtered_nodes) == 0:
            return None
        return filtered_nodes

    @staticmethod
    def node_matches(node, retain_nodes):
        Filter.check(node)
        if retain_nodes is None:
            return True
        for node_type_name, attributes_map in retain_nodes if retain_nodes is not None else []:
            if node_type_name is None or node_type_name == node.type_name:
                if attributes_map is None:
                    return True
                return Filter.attributes_match(node.attributes, attributes_map)
        return False

    # match_attributes is a map[str, _] of attribute_keys to attribute_values
    @staticmethod
    def attributes_match(attributes, match_attributes):
        if attributes is None:
            return match_attributes is None
        for match_attribute_key, match_attribute_value in match_attributes if match_attributes is not None else []:
            found = False
            for tmp_attribute in attributes:
                if match_attribute_key is None or match_attribute_key == tmp_attribute.key:
                    found = True
                    if match_attribute_value is not None and match_attribute_value != tmp_attribute.value:
                        return False
            if not found:
                return False
        return True
