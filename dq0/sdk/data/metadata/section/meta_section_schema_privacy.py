from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionSchemaPrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_SCHEMA_PRIVACY:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_SCHEMA_PRIVACY} was {type_name}")
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        return MetaSectionSchemaPrivacy(name, privacy_level)

    def __init__(
            self,
            name,
            privacy_level=2):
        super().__init__(MetaSection.TYPE_NAME_SCHEMA_PRIVACY, name)
        self.privacy_level = privacy_level
