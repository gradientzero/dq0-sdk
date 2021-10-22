class MetaSectionType:
    TYPE_NAME_COLUMN = 'column'
    TYPE_NAME_COLUMN_BOOLEAN_DATETIME = 'column_boolean_datetime'
    TYPE_NAME_COLUMN_FLOAT = 'column_float'
    TYPE_NAME_COLUMN_INT = 'column_int'
    TYPE_NAME_COLUMN_MACHINE_LEARNING = 'column_machine_learning'
    TYPE_NAME_COLUMN_SMART_NOISE = 'column_smart_noise'
    TYPE_NAME_COLUMN_SMART_NOISE_FLOAT = 'column_smart_noise_float'
    TYPE_NAME_COLUMN_SMART_NOISE_INT = 'column_smart_noise_int'
    TYPE_NAME_COLUMN_SMART_NOISE_STRING = 'column_smart_noise_string'
    TYPE_NAME_COLUMN_STRING = 'column_string'
    TYPE_NAME_DATASET_TAGS = 'dataset_tags'
    TYPE_NAME_SCHEMA_PRIVACY = 'schema_privacy'
    TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY = 'table_differential_privacy'
    TYPE_NAME_TABLE_OTHER = 'table_other'
    TYPE_NAME_TABLE_PRIVACY = 'table_privacy'
    TYPE_NAME_TABLE_SMART_NOISE = 'table_smart_noise'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if \
                type_name == MetaSectionType.TYPE_NAME_COLUMN or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_FLOAT or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_INT or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_INT or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_STRING or \
                type_name == MetaSectionType.TYPE_NAME_COLUMN_STRING or \
                type_name == MetaSectionType.TYPE_NAME_DATASET_TAGS or \
                type_name == MetaSectionType.TYPE_NAME_SCHEMA_PRIVACY or \
                type_name == MetaSectionType.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY or \
                type_name == MetaSectionType.TYPE_NAME_TABLE_OTHER or \
                type_name == MetaSectionType.TYPE_NAME_TABLE_PRIVACY or \
                type_name == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            return True
        return False
