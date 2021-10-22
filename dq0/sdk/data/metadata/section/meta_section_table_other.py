from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableOther(MetaSection):
    def __init__(
            self, 
            name, 
            synth_allowed=False,
            tau=0.0):
        super().__init__(MetaSectionType.TYPE_NAME_TABLE_OTHER, name)
        self.synth_allowed = synth_allowed
        self.tau = tau

    def copy(self):
        return MetaSectionTableOther(self.name, self.synth_allowed, self.tau)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('synth_allowed', self.synth_allowed),
            ('tau', self.tau),
            ] if v is not None}
        return {**super_dct, **dct}

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.synth_allowed != other.synth_allowed:
            raise Exception(f"sections with matching super precheck cannot have diverging synth_allowed flags {self.synth_allowed} <--> {other.synth_allowed}")
        if self.tau != other.tau:
            raise Exception(f"sections with matching super precheck cannot have diverging taus {self.tau} <--> {other.tau}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
