class NodeType:
    # No underscores allowed in these type names
    # dataset
    TYPE_NAME_DATASET = 'dataset'
    TYPE_NAME_DATABASE = 'database'
    TYPE_NAME_SCHEMA = 'schema'
    TYPE_NAME_TABLE = 'table'
    TYPE_NAME_COLUMN = 'column'
    # run
    TYPE_NAME_RUN = 'run'

    @staticmethod
    def is_valid_type_name(type_name):
        if type_name is None:
            return False
        if \
                type_name == NodeType.TYPE_NAME_DATASET or \
                type_name == NodeType.TYPE_NAME_DATABASE or \
                type_name == NodeType.TYPE_NAME_SCHEMA or \
                type_name == NodeType.TYPE_NAME_TABLE or \
                type_name == NodeType.TYPE_NAME_COLUMN or \
                type_name == NodeType.TYPE_NAME_RUN:
            return True
        return False
