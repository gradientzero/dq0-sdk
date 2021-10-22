from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionDatasetTags(MetaSection):
    def __init__(
            self, 
            name, 
            tags=None):
        super().__init__(MetaSectionType.TYPE_NAME_DATASET_TAGS, name)
        self.tags = tags

    def copy(self):
        return MetaSectionDatasetTags(self.name, self.tags)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('tags', self.tags),
            ] if v is not None}
        return {**super_dct, **dct}

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        merged = self.copy()
        for tag in other.tags if other.tags is not None else []:
            if tag not in merged.tags:
                merged.tags.append(tag)
        return merged
