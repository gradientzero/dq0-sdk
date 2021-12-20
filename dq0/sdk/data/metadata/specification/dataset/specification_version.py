class SpecificationVersion:
    # No underscores allowed in these type names
    VERSION_V1 = 'v1'

    @staticmethod
    def is_valid_version(version):
        if not isinstance(version, str):
            return False
        if \
                version == SpecificationVersion.VERSION_V1:
            return True
        return False
