class MetaConnectorType:
    TYPE_NAME_CSV = 'csv'
    TYPE_NAME_POSTGRES = 'postgres'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if type_name == MetaConnectorType.TYPE_NAME_CSV or type_name == MetaConnectorType.TYPE_NAME_POSTGRES:
            return True
        return False
