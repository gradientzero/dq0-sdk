from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTablePrivacy(MetaSection):
    def __init__(
            self,
            name,
            privacy_level=2,
            privacy_column=None):
        super().__init__(MetaSectionType.TYPE_NAME_TABLE_PRIVACY, name)
        self.privacy_level = privacy_level
        self.privacy_column = privacy_column

    def copy(self):
        return MetaSectionTablePrivacy(self.name, self.privacy_level, self.privacy_column)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('privacy_level', self.privacy_level),
            ('privacy_column', self.privacy_column),
            ] if v is not None}
        return {**super_dct, **dct}

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.privacy_level != other.privacy_level:
            raise Exception(f"sections with matching super precheck cannot have diverging privacy_levels {self.privacy_level} <--> {other.privacy_level}")
        if self.privacy_column != other.privacy_column:
            raise Exception(f"sections with matching super precheck cannot have diverging privacy_columns {self.privacy_column} <--> {other.privacy_column}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
