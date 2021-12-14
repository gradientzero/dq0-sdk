from dq0.sdk.data.metadata.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.node.node import Node


class Utils:
    @staticmethod
    def get_feature_target_cols_from_meta(metadata):
        feature_columns = []
        target_columns = []
        for node_table in metadata.dataset_node.child_nodes[0].child_nodes[0].child_nodes:
            for node_column in node_table.child_nodes:
                attribute_column_data = node_column.get_attribute(key='data')
                attribute_column_name = attribute_column_data.get_attribute(key='name') \
                    if attribute_column_data is not None else None
                if attribute_column_name is not None:
                    attribute_column_machine_learning = node_column.get_attribute(key='machine_learning')
                    attribute_column_is_feature = attribute_column_machine_learning.get_attribute(key='is_feature') \
                        if attribute_column_machine_learning is not None else None
                    if attribute_column_is_feature is not None and attribute_column_is_feature.value:
                        feature_columns.append(attribute_column_name.value)
                    attribute_column_is_target = attribute_column_machine_learning.get_attribute(key='is_target') \
                        if attribute_column_machine_learning is not None else None
                    if attribute_column_is_target is not None and attribute_column_is_target.value:
                        target_columns.append(attribute_column_name.value)
        return feature_columns, target_columns

    @staticmethod
    def get_header_columns_from_meta(metadata):
        header_columns = []
        for node_table in metadata.dataset_node.child_nodes[0].child_nodes[0].child_nodes:
            attribute_table_connector = node_table.get_attribute(key='connector')
            if attribute_table_connector is not None:
                attribute_connector_type_name = attribute_table_connector.get_attribute(key='type_name')
                if attribute_connector_type_name is not None and attribute_connector_type_name.value == 'csv':
                    attribute_connector_header_columns = attribute_table_connector.get_attribute(key='header_columns')
                    if attribute_connector_header_columns is not None:
                        for tmp_attribute_header in attribute_connector_header_columns.value:
                            header_columns.append(tmp_attribute_header.value)
        return header_columns

    @staticmethod
    def get_col_types(metadata):
        col_types = {}
        for node_table in metadata.dataset_node.child_nodes[0].child_nodes[0].child_nodes:
            for node_column in node_table.child_nodes:
                attribute_column_data = node_column.get_attribute(key='data')
                attribute_column_name = attribute_column_data.get_attribute(key='name') \
                    if attribute_column_data is not None else None
                if isinstance(attribute_column_name, AttributeString):
                    attribute_column_data_type_name = attribute_column_data.get_attribute(key='data_type_name') \
                        if attribute_column_data is not None else None
                    if isinstance(attribute_column_data_type_name, AttributeString):
                        col_types[attribute_column_name.value] = attribute_column_data_type_name.value
        return col_types if len(col_types) != 0 else None

    @staticmethod
    def get_name_and_names(node, fail_for_non_existing=False):
        if isinstance(node, Node):
            attribute_data = node.get_attribute(key='data')
            if isinstance(attribute_data, AttributeList):
                attribute_name = attribute_data.get_attribute(key='name')
                if isinstance(attribute_name, AttributeString) and \
                        attribute_name.value is not None and \
                        isinstance(attribute_name.value, str):
                    node_name = attribute_name.value
                    child_node_names = {}
                    for child_node in node.child_nodes if isinstance(node.child_nodes, list) else []:
                        child_node_name, recursive_names = Utils.get_name_and_names(
                            node=child_node, fail_for_non_existing=fail_for_non_existing)
                        if child_node_name is not None:
                            child_node_names[child_node_name] = recursive_names
                    return node_name, child_node_names
                elif fail_for_non_existing:
                    raise Exception(f"attribute {attribute_name} is not of type AttributeString, "
                                    f"is of type {type(attribute_name)} instead, or its value is empty")
            elif fail_for_non_existing:
                raise Exception(f"attribute {attribute_data} is not of type AttributeList, "
                                f"is of type {type(attribute_data)} instead")
        elif fail_for_non_existing:
            raise Exception(f"node {node} is not of type Node, is of type {type(node)} instead")
        return None, None

    @staticmethod
    def get_names(metadata, fail_for_non_existing=False):
        if not isinstance(metadata, Metadata):
            if fail_for_non_existing:
                raise Exception(f"metadata {metadata} is not of type Metadata, "
                                f"is of type {type(metadata)} instead")
            return {}
        dataset_name, recursive_names = Utils.get_name_and_names(
            node=metadata.dataset_node, fail_for_non_existing=fail_for_non_existing)
        if dataset_name is None:
            return {}
        return {dataset_name: recursive_names}
