class MetaNodeType:
    TYPE_NAME_DATASET = 'dataset'
    TYPE_NAME_DATABASE = 'database'
    TYPE_NAME_SCHEMA = 'schema'
    TYPE_NAME_TABLE = 'table'
    TYPE_NAME_COLUMN = 'column'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if \
                type_name == MetaNodeType.TYPE_NAME_DATASET or \
                type_name == MetaNodeType.TYPE_NAME_DATABASE or \
                type_name == MetaNodeType.TYPE_NAME_SCHEMA or \
                type_name == MetaNodeType.TYPE_NAME_TABLE or \
                type_name == MetaNodeType.TYPE_NAME_COLUMN:
            return True
        return False
