from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumn(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN)
        name = yaml_dict.pop('name', None)
        data_type_name = yaml_dict.pop('data_type_name', None)
        selectable = bool(yaml_dict.pop('selectable', False))
        return MetaSectionColumn(name, data_type_name, selectable)
    
    def __init__(
            self,
            name=None,
            data_type_name=None,
            selectable=False):
        super().__init__(MetaSection.TYPE_NAME_COLUMN, name)
        self.data_type_name = data_type_name
        self.selectable = selectable


class MetaSectionColumnBooleanDatetime(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_BOOLEAN_DATETIME)
        name = yaml_dict.pop('name', None)
        synthesizable = bool(yaml_dict.pop('synthesizable', False))
        return MetaSectionColumnBooleanDatetime(name, synthesizable)

    def __init__(
            self,
            name=None,
            synthesizable=False):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_BOOLEAN_DATETIME, name)
        self.synthesizable = synthesizable


class MetaSectionColumnFloat(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_FLOAT)
        name = yaml_dict.pop('name', None)
        use_auto_bounds = bool(yaml_dict.pop('use_auto_bounds', False))
        auto_bounds_prob = float(yaml_dict.pop('auto_bounds_prob', 0.9))
        auto_lower = float(yaml_dict.pop('auto_lower', 0.0))
        auto_upper = float(yaml_dict.pop('auto_upper', 0.0))
        discrete = bool(yaml_dict.pop('discrete', False))
        min_step = float(yaml_dict.pop('min_step', 1.0))
        synthesizable = bool(yaml_dict.pop('synthesizable', True))
        return MetaSectionColumnFloat(name, use_auto_bounds, auto_bounds_prob, auto_lower, auto_upper, discrete, min_step, synthesizable)

    def __init__(
            self,
            name=None,
            use_auto_bounds=False,
            auto_bounds_prob=0.9,
            auto_lower=None,
            auto_upper=None,
            discrete=False,
            min_step=1.0,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_FLOAT, name)
        self.use_auto_bounds = use_auto_bounds
        self.auto_bounds_prob = auto_bounds_prob
        self.auto_lower = auto_lower
        self.auto_upper = auto_upper
        self.discrete = discrete
        self.min_step = min_step
        self.synthesizable = synthesizable


class MetaSectionColumnInt(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_INT)
        name = yaml_dict.pop('name', None)
        use_auto_bounds = bool(yaml_dict.pop('use_auto_bounds', False))
        auto_bounds_prob = float(yaml_dict.pop('auto_bounds_prob', 0.9))
        auto_lower = int(yaml_dict.pop('auto_lower', 0))
        auto_upper = int(yaml_dict.pop('auto_upper', 0))
        discrete = bool(yaml_dict.pop('discrete', False))
        min_step = int(yaml_dict.pop('min_step', 1))
        synthesizable = bool(yaml_dict.pop('synthesizable', True))
        return MetaSectionColumnInt(name, use_auto_bounds, auto_bounds_prob, auto_lower, auto_upper, discrete, min_step, synthesizable)

    def __init__(
            self,
            name=None,
            use_auto_bounds=False,
            auto_bounds_prob=0.9,
            auto_lower=None,
            auto_upper=None,
            discrete=False,
            min_step=1.0,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_INT, name)
        self.use_auto_bounds = use_auto_bounds
        self.auto_bounds_prob = auto_bounds_prob
        self.auto_lower = auto_lower
        self.auto_upper = auto_upper
        self.discrete = discrete
        self.min_step = min_step
        self.synthesizable = synthesizable


class MetaSectionColumnString(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_STRING)
        name = yaml_dict.pop('name', None)
        cardinality = int(yaml_dict.pop('cardinality', 0))
        allowed_values = yaml_dict.pop('allowed_values', None)
        mask = yaml_dict.pop('use_auto_bounds', None)
        synthesizable = bool(yaml_dict.pop('synthesizable', cardinality != 0))
        return MetaSectionColumnString(name, cardinality, allowed_values, mask, synthesizable)

    def __init__(
            self,
            name=None,
            allowed_values=None,
            mask=None,
            cardinality=0,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_STRING, name)
        self.allowed_values = allowed_values
        self.mask = mask
        self.cardinality = cardinality
        self.synthesizable = synthesizable
