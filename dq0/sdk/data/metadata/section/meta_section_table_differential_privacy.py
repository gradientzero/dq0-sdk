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

    def copy(self):
        return MetaSectionTableDifferentialPrivacy(self.name, self.budget_epsilon, self.budget_delta)

    def to_dict(self):
        dct = super().to_dict()
        dct["budget_epsilon"] = self.budget_epsilon
        dct["budget_delta"] = self.budget_delta
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.budget_epsilon != other.budget_epsilon:
            raise Exception(f"sections with matching super precheck cannot have diverging budget_epsilons {self.budget_epsilon} <--> {other.budget_epsilon}")
        if self.budget_delta != other.budget_delta:
            raise Exception(f"sections with matching super precheck cannot have diverging budget_deltas {self.budget_delta} <--> {other.budget_delta}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
