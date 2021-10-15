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
