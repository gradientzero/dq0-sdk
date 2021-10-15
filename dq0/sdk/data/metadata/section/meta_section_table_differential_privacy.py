from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableDifferentialPrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY)
        name = yaml_dict.pop('name', None)
        budget_epsilon = float(yaml_dict.pop('budget_epsilon', 0.0))
        budget_delta = float(yaml_dict.pop('budget_delta', 0.0))
        return MetaSectionTableDifferentialPrivacy(name, budget_epsilon, budget_delta)

    def __init__(
            self,
            name,
            budget_epsilon=0.0,
            budget_delta=0.0):
        super().__init__(MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY, name)
        self.budget_epsilon = budget_epsilon
        self.budget_delta = budget_delta
