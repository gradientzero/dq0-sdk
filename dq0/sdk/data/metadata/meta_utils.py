from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector
from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType


class MetaUtils:
    @staticmethod
    def get_feature_target_cols_from_meta(metadata):
        feature_columns = []
        target_columns = []
        for meta_node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            for meta_node_column in meta_node_table.child_nodes:
                for section in meta_node_column.sections:
                    if section.type_name == MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING:
                        if section.is_feature:
                            feature_columns.append(meta_node_column.name)
                        if section.is_target:
                            target_columns.append(meta_node_column.name)
                        break
        return feature_columns, target_columns

    @staticmethod
    def get_header_rows_from_meta(metadata):
        header_rows = []
        for meta_node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            if meta_node_table.connector is None or meta_node_table.connector.type_name != MetaConnector.TYPE_NAME_CSV:
                raise NotImplementedError(f"only connectors of type {MetaConnector.TYPE_NAME_CSV} are implemented at the moment, was {meta_node_table.connector.type_name}")
            header_rows.append(meta_node_table.connector.header_row)
        return header_rows

    @staticmethod
    def get_col_types(metadata):
        col_types = {}
        for meta_node_table in metadata.root_node.child_nodes[0].child_nodes[0].child_nodes:
            for meta_node_column in meta_node_table.child_nodes:
                for section in meta_node_column.sections:   
                    if section.type_name == MetaSectionType.TYPE_NAME_COLUMN:
                        col_types[meta_node_column.name] = section.data_type_name
                        break
        if len(col_types.keys()) == 0:
            col_types = None
        return col_types