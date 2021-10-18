from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableOther(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_TABLE_OTHER)
        name = yaml_dict.pop('name', None)
        synth_allowed = bool(yaml_dict.pop('synth_allowed', False))
        tau = float(yaml_dict.pop('tau', 0.0))
        return MetaSectionTableOther(name, synth_allowed, tau)

    def __init__(
            self, 
            name, 
            synth_allowed=False,
            tau=0.0):
        super().__init__(MetaSection.TYPE_NAME_TABLE_OTHER, name)
        self.synth_allowed = synth_allowed
        self.tau = tau

    def copy(self):
        return MetaSectionTableOther(self.name, self.synth_allowed, self.tau)

    def to_dict(self):
        dct = super().to_dict()
        dct["synth_allowed"] = self.synth_allowed
        dct["tau"] = self.tau
        return dct

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
