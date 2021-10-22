from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumn(MetaSection):
    def __init__(
            self,
            name=None,
            data_type_name=None,
            selectable=False):
        super().__init__(MetaSectionType.TYPE_NAME_COLUMN, name)
        self.data_type_name = data_type_name
        self.selectable = selectable

    def copy(self):
        return MetaSectionColumn(self.name, self.data_type_name, self.selectable)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('data_type_name', self.data_type_name),
            ('selectable', self.selectable),
            ] if v is not None}
        return {**super_dct, **dct}

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
    def __init__(
            self,
            name=None,
            synthesizable=False):
        super().__init__(MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME, name)
        self.synthesizable = synthesizable

    def copy(self):
        return MetaSectionColumnBooleanDatetime(self.name, self.synthesizable)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('synthesizable', self.synthesizable),
            ] if v is not None}
        return {**super_dct, **dct}        

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
        super().__init__(MetaSectionType.TYPE_NAME_COLUMN_FLOAT, name)
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
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('use_auto_bounds', self.use_auto_bounds),
            ('auto_bounds_prob', self.auto_bounds_prob),
            ('auto_lower', self.auto_lower),
            ('auto_upper', self.auto_upper),
            ('discrete', self.discrete),
            ('min_step', self.min_step),
            ('synthesizable', self.synthesizable),
            ] if v is not None}
        return {**super_dct, **dct}

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
    def __init__(
            self,
            name=None,
            use_auto_bounds=False,
            auto_bounds_prob=0.9,
            auto_lower=None,
            auto_upper=None,
            discrete=False,
            min_step=1,
            synthesizable=True):
        super().__init__(MetaSectionType.TYPE_NAME_COLUMN_INT, name)
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
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('use_auto_bounds', self.use_auto_bounds),
            ('auto_bounds_prob', self.auto_bounds_prob),
            ('auto_lower', self.auto_lower),
            ('auto_upper', self.auto_upper),
            ('discrete', self.discrete),
            ('min_step', self.min_step),
            ('synthesizable', self.synthesizable),
            ] if v is not None}
        return {**super_dct, **dct}

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
    def __init__(
            self,
            name=None,
            allowed_values=None,
            mask=None,
            cardinality=0,
            synthesizable=True):
        super().__init__(MetaSectionType.TYPE_NAME_COLUMN_STRING, name)
        self.allowed_values = allowed_values
        self.mask = mask
        self.cardinality = cardinality
        self.synthesizable = synthesizable

    def copy(self):
        return MetaSectionColumnString(self.name, self.allowed_values, self.mask, self.cardinality, self.synthesizable)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('allowed_values', self.allowed_values),
            ('mask', self.mask),
            ('cardinality', self.cardinality),
            ('synthesizable', self.synthesizable),
            ] if v is not None}
        return {**super_dct, **dct}

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
