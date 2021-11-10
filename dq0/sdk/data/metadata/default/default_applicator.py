from dq0.sdk.data.metadata.default.default_column import DefaultColumn
from dq0.sdk.data.metadata.default.default_connector import DefaultConnector
from dq0.sdk.data.metadata.default.default_database import DefaultDatabase
from dq0.sdk.data.metadata.default.default_dataset import DefaultDataset
from dq0.sdk.data.metadata.default.default_schema import DefaultSchema
from dq0.sdk.data.metadata.default.default_table import DefaultTable
from dq0.sdk.data.metadata.node.node_type import NodeType

class DefaultApplicator:
    @staticmethod
    def apply_default_attributes(node_type_name, attributes_list=[], default_user_uuids=None, default_role_uuids=None):
        new_attributes_list = attributes_list
        if \
                node_type_name == NodeType.TYPE_NAME_DATASET or \
                node_type_name == NodeType.TYPE_NAME_DATABASE or \
                node_type_name == NodeType.TYPE_NAME_SCHEMA or \
                node_type_name == NodeType.TYPE_NAME_TABLE:
            new_attributes_list = DefaultConnector.merge_default_attributes_with(attributes_list=new_attributes_list)
        if node_type_name == NodeType.TYPE_NAME_DATASET:
            new_attributes_list = DefaultDataset.merge_default_attributes_with(dataset_attributes_list=new_attributes_list, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        elif node_type_name == NodeType.TYPE_NAME_DATABASE:
            new_attributes_list = DefaultDatabase.merge_default_attributes_with(database_attributes_list=new_attributes_list, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        elif node_type_name == NodeType.TYPE_NAME_SCHEMA:
            new_attributes_list = DefaultSchema.merge_default_attributes_with(schema_attributes_list=new_attributes_list, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        elif node_type_name == NodeType.TYPE_NAME_TABLE:
            new_attributes_list = DefaultTable.merge_default_attributes_with(table_attributes_list=new_attributes_list, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        elif node_type_name == NodeType.TYPE_NAME_COLUMN:
            new_attributes_list = DefaultColumn.merge_default_attributes_with(column_attributes_list=new_attributes_list, default_user_uuids=default_user_uuids, default_role_uuids=default_role_uuids)
        return new_attributes_list
