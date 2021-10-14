from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableDifferentialPrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY} was {type_name}")
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
