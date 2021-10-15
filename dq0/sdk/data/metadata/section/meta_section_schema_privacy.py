from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionSchemaPrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_SCHEMA_PRIVACY)
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        return MetaSectionSchemaPrivacy(name, privacy_level)

    def __init__(
            self,
            name,
            privacy_level=2):
        super().__init__(MetaSection.TYPE_NAME_SCHEMA_PRIVACY, name)
        self.privacy_level = privacy_level
