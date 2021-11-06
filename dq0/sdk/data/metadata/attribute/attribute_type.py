class AttributeType:
    TYPE_NAME_BOOLEAN = 'boolean'
    TYPE_NAME_DATETIME = 'datetime'
    TYPE_NAME_DICT = 'dict'
    TYPE_NAME_FLOAT = 'float'
    TYPE_NAME_INT = 'int'
    TYPE_NAME_LIST = 'list'
    TYPE_NAME_STRING = 'string'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if \
                type_name == AttributeType.TYPE_NAME_BOOLEAN or \
                type_name == AttributeType.TYPE_NAME_DATETIME or \
                type_name == AttributeType.TYPE_NAME_DICT or \
                type_name == AttributeType.TYPE_NAME_FLOAT or \
                type_name == AttributeType.TYPE_NAME_INT or \
                type_name == AttributeType.TYPE_NAME_LIST or \
                type_name == AttributeType.TYPE_NAME_STRING:
            return True
        return False
