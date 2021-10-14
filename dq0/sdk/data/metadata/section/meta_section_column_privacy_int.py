from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnPrivacyInt(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_COLUMN_PRIVACY_INT:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_COLUMN_PRIVACY_INT} was {type_name}")
        name = yaml_dict.pop('name', None)
        bounded = bool(yaml_dict.pop('bounded', False))
        lower = int(yaml_dict.pop('lower', 0))
        upper = int(yaml_dict.pop('upper', 0))
        use_auto_bounds = bool(yaml_dict.pop('use_auto_bounds', False))
        auto_bounds_prob = float(yaml_dict.pop('auto_bounds_prob', 0.9))
        auto_lower = int(yaml_dict.pop('auto_lower', 0))
        auto_upper = int(yaml_dict.pop('auto_upper', 0))
        discrete = bool(yaml_dict.pop('discrete', False))
        min_step = int(yaml_dict.pop('min_step', 1))
        synthesizable = bool(yaml_dict.pop('synthesizable', True))
        return MetaSectionColumnPrivacyInt(name, bounded, lower, upper, use_auto_bounds, auto_bounds_prob, auto_lower, auto_upper, discrete, min_step, synthesizable)

    def __init__(
            self,
            name=None,
            bounded=False,
            lower=None,
            upper=None,
            use_auto_bounds=False,
            auto_bounds_prob=0.9,
            auto_lower=None,
            auto_upper=None,
            discrete=False,
            min_step=1.0,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_PRIVACY_INT, name)
        self.bounded = bounded
        self.lower = lower
        self.upper = upper
        self.use_auto_bounds = use_auto_bounds
        self.auto_bounds_prob = auto_bounds_prob
        self.auto_lower = auto_lower
        self.auto_upper = auto_upper
        self.discrete = discrete
        self.min_step = min_step
