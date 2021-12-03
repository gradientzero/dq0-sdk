class SpecificationType:
    # No underscores allowed in these type names
    TYPE_NAME_STANDARD = 'standard'
    TYPE_NAME_MULTI = 'multi'

    @staticmethod
    def is_valid_type_name(type_name):
        if type_name is None:
            return False
        if \
                type_name == SpecificationType.TYPE_NAME_STANDARD or \
                type_name == SpecificationType.TYPE_NAME_MULTI:
            return True
        return False
