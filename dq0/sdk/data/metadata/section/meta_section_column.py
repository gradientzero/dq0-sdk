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

    def copy(self):
        return MetaSectionColumn(self.name, self.data_type_name, self.selectable)

    def to_dict(self):
        dct = super().to_dict()
        dct["data_type_name"] = self.data_type_name
        dct["selectable"] = self.selectable
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.data_type_name != other.data_type_name:
            raise Exception(f"sections with matching super precheck cannot have diverging data_type_names {self.data_type_name} <--> {other.data_type_name}")
        if self.selectable != other.selectable:
            raise Exception(f"sections with matching super precheck cannot have diverging selectable flags {self.selectable} <--> {other.selectable}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


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

    def copy(self):
        return MetaSectionColumnBooleanDatetime(self.name, self.synthesizable)

    def to_dict(self):
        dct = super().to_dict()
        dct["synthesizable"] = self.synthesizable
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.synthesizable != other.synthesizable:
            raise Exception(f"sections with matching super precheck cannot have diverging synthesizable flags {self.synthesizable} <--> {other.synthesizable}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


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

    def copy(self):
        return MetaSectionColumnFloat(self.name, self.use_auto_bounds, self.auto_bounds_prob, self.auto_lower, self.auto_upper, self.discrete, self.min_step, self.synthesizable)

    def to_dict(self):
        dct = super().to_dict()
        dct["use_auto_bounds"] = self.use_auto_bounds
        dct["auto_bounds_prob"] = self.auto_bounds_prob
        dct["auto_lower"] = self.auto_lower
        dct["auto_upper"] = self.auto_upper
        dct["discrete"] = self.discrete
        dct["min_step"] = self.min_step
        dct["synthesizable"] = self.synthesizable
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.use_auto_bounds != other.use_auto_bounds:
            raise Exception(f"sections with matching super precheck cannot have diverging use_auto_bounds flags {self.use_auto_bounds} <--> {other.use_auto_bounds}")
        if self.auto_bounds_prob != other.auto_bounds_prob:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_bounds_probs {self.auto_bounds_prob} <--> {other.auto_bounds_prob}")
        if self.auto_lower != other.auto_lower:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_lower bounds {self.auto_lower} <--> {other.auto_lower}")
        if self.auto_upper != other.auto_upper:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_upper bounds {self.auto_upper} <--> {other.auto_upper}")
        if self.discrete != other.discrete:
            raise Exception(f"sections with matching super precheck cannot have diverging discrete flags {self.discrete} <--> {other.discrete}")
        if self.min_step != other.min_step:
            raise Exception(f"sections with matching super precheck cannot have diverging min_steps {self.min_step} <--> {other.min_step}")
        if self.synthesizable != other.synthesizable:
            raise Exception(f"sections with matching super precheck cannot have diverging synthesizable flags {self.synthesizable} <--> {other.synthesizable}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


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

    def copy(self):
        return MetaSectionColumnInt(self.name, self.use_auto_bounds, self.auto_bounds_prob, self.auto_lower, self.auto_upper, self.discrete, self.min_step, self.synthesizable)

    def to_dict(self):
        dct = super().to_dict()
        dct["use_auto_bounds"] = self.use_auto_bounds
        dct["auto_bounds_prob"] = self.auto_bounds_prob
        dct["auto_lower"] = self.auto_lower
        dct["auto_upper"] = self.auto_upper
        dct["discrete"] = self.discrete
        dct["min_step"] = self.min_step
        dct["synthesizable"] = self.synthesizable
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.use_auto_bounds != other.use_auto_bounds:
            raise Exception(f"sections with matching super precheck cannot have diverging use_auto_bounds flags {self.use_auto_bounds} <--> {other.use_auto_bounds}")
        if self.auto_bounds_prob != other.auto_bounds_prob:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_bounds_probs {self.auto_bounds_prob} <--> {other.auto_bounds_prob}")
        if self.auto_lower != other.auto_lower:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_lower bounds {self.auto_lower} <--> {other.auto_lower}")
        if self.auto_upper != other.auto_upper:
            raise Exception(f"sections with matching super precheck cannot have diverging auto_upper bounds {self.auto_upper} <--> {other.auto_upper}")
        if self.discrete != other.discrete:
            raise Exception(f"sections with matching super precheck cannot have diverging discrete flags {self.discrete} <--> {other.discrete}")
        if self.min_step != other.min_step:
            raise Exception(f"sections with matching super precheck cannot have diverging min_steps {self.min_step} <--> {other.min_step}")
        if self.synthesizable != other.synthesizable:
            raise Exception(f"sections with matching super precheck cannot have diverging synthesizable flags {self.synthesizable} <--> {other.synthesizable}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


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

    def copy(self):
        return MetaSectionColumnString(self.name, self.allowed_values, self.mask, self.cardinality, self.synthesizable)

    def to_dict(self):
        dct = super().to_dict()
        dct["allowed_values"] = self.allowed_values
        dct["mask"] = self.mask
        dct["cardinality"] = self.cardinality
        dct["synthesizable"] = self.synthesizable
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.allowed_values != other.allowed_values:
            raise Exception(f"sections with matching super precheck cannot have diverging allowed_values {self.allowed_values} <--> {other.allowed_values}")
        if self.mask != other.mask:
            raise Exception(f"sections with matching super precheck cannot have diverging masks {self.mask} <--> {other.mask}")
        if self.cardinality != other.cardinality:
            raise Exception(f"sections with matching super precheck cannot have diverging cardinalities {self.cardinality} <--> {other.cardinality}")
        if self.synthesizable != other.synthesizable:
            raise Exception(f"sections with matching super precheck cannot have diverging synthesizable flags {self.synthesizable} <--> {other.synthesizable}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
