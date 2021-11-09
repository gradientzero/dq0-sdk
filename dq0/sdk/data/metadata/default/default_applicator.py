from dq0.sdk.data.metadata.default.default_column import DefaultColumn
from dq0.sdk.data.metadata.default.default_connector import DefaultConnector
from dq0.sdk.data.metadata.default.default_database import DefaultDatabase
from dq0.sdk.data.metadata.default.default_dataset import DefaultDataset
from dq0.sdk.data.metadata.default.default_schema import DefaultSchema
from dq0.sdk.data.metadata.default.default_table import DefaultTable
from dq0.sdk.data.metadata.node.node_type import NodeType

class DefaultApplicator:
    @staticmethod
    def applyDefaultAttributes(node_type_name, attributes_list=[]):
        new_attributes_list = attributes_list
        if \
                node_type_name == NodeType.TYPE_NAME_DATASET or \
                node_type_name == NodeType.TYPE_NAME_DATABASE or \
                node_type_name == NodeType.TYPE_NAME_SCHEMA or \
                node_type_name == NodeType.TYPE_NAME_TABLE:
            new_attributes_list = DefaultConnector.mergeDefaultAttributesWith(new_attributes_list)
        if node_type_name == NodeType.TYPE_NAME_DATASET:
            new_attributes_list = DefaultDataset.mergeDefaultAttributesWith(new_attributes_list)
        elif node_type_name == NodeType.TYPE_NAME_DATABASE:
            new_attributes_list = DefaultDatabase.mergeDefaultAttributesWith(new_attributes_list)
        elif node_type_name == NodeType.TYPE_NAME_SCHEMA:
            new_attributes_list = DefaultSchema.mergeDefaultAttributesWith(new_attributes_list)
        elif node_type_name == NodeType.TYPE_NAME_TABLE:
            new_attributes_list = DefaultTable.mergeDefaultAttributesWith(new_attributes_list)
        elif node_type_name == NodeType.TYPE_NAME_COLUMN:
            new_attributes_list = DefaultColumn.merge_default_attributes_with(new_attributes_list)
        return new_attributes_list
