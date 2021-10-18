from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTablePrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_TABLE_PRIVACY)
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        return MetaSectionTablePrivacy(name, privacy_level)

    def __init__(
            self,
            name,
            privacy_level=2):
        super().__init__(MetaSection.TYPE_NAME_TABLE_PRIVACY, name)
        self.privacy_level = privacy_level

    def copy(self):
        return MetaSectionTablePrivacy(self.name, self.privacy_level)

    def to_dict(self):
        dct = super().to_dict()
        dct["privacy_level"] = self.privacy_level
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.privacy_level != other.privacy_level:
            raise Exception(f"sections with matching super precheck cannot have diverging privacy_levels {self.privacy_level} <--> {other.privacy_level}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
