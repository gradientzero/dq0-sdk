from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionSchemaPrivacy(MetaSection):
    def __init__(
            self,
            name,
            privacy_level=2):
        super().__init__(MetaSectionType.TYPE_NAME_SCHEMA_PRIVACY, name)
        self.privacy_level = privacy_level

    def copy(self):
        return MetaSectionSchemaPrivacy(self.name, self.privacy_level)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('privacy_level', self.privacy_level),
            ] if v is not None}
        return {**super_dct, **dct}

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
