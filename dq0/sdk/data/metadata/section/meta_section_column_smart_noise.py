from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnSmartNoise(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE)
        name = yaml_dict.pop('name', None)
        private_id = bool(yaml_dict.pop('private_id', False))
        return MetaSectionColumnSmartNoise(name, private_id)

    def __init__(
            self,
            name=None,
            private_id=False):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_SMART_NOISE, name)
        self.private_id = private_id

    def copy(self):
        return MetaSectionColumnSmartNoise(self.name, self.private_id)

    def to_dict(self):
        dct = super().to_dict()
        dct["private_id"] = self.private_id
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.private_id != other.private_id:
            raise Exception(f"sections with matching super precheck cannot have diverging private_ids {self.private_id} <--> {other.private_id}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


class MetaSectionColumnSmartNoiseFloat(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT)
        name = yaml_dict.pop('name', None)
        bounded = bool(yaml_dict.pop('bounded', False))
        lower = float(yaml_dict.pop('lower', 0.0))
        upper = float(yaml_dict.pop('upper', 0.0))
        return MetaSectionColumnSmartNoiseFloat(name, bounded, lower, upper)

    def __init__(
            self,
            name=None,
            bounded=False,
            lower=None,
            upper=None):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT, name)
        self.bounded = bounded
        self.lower = lower
        self.upper = upper

    def copy(self):
        return MetaSectionColumnSmartNoiseFloat(self.name, self.bounded, self.lower, self.upper)

    def to_dict(self):
        dct = super().to_dict()
        dct["bounded"] = self.bounded
        dct["lower"] = self.lower
        dct["upper"] = self.upper
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.bounded != other.bounded:
            raise Exception(f"sections with matching super precheck cannot have diverging bounded flags {self.bounded} <--> {other.bounded}")
        if self.lower != other.lower:
            raise Exception(f"sections with matching super precheck cannot have diverging lower bounds {self.lower} <--> {other.lower}")
        if self.upper != other.upper:
            raise Exception(f"sections with matching super precheck cannot have diverging upper bounds {self.upper} <--> {other.upper}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


class MetaSectionColumnSmartNoiseInt(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_INT)
        name = yaml_dict.pop('name', None)
        bounded = bool(yaml_dict.pop('bounded', False))
        lower = int(yaml_dict.pop('lower', 0))
        upper = int(yaml_dict.pop('upper', 0))
        return MetaSectionColumnSmartNoiseInt(name, bounded, lower, upper)

    def __init__(
            self,
            name=None,
            bounded=False,
            lower=None,
            upper=None):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_INT, name)
        self.bounded = bounded
        self.lower = lower
        self.upper = upper

    def copy(self):
        return MetaSectionColumnSmartNoiseInt(self.name, self.bounded, self.lower, self.upper)

    def to_dict(self):
        dct = super().to_dict()
        dct["bounded"] = self.bounded
        dct["lower"] = self.lower
        dct["upper"] = self.upper
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.bounded != other.bounded:
            raise Exception(f"sections with matching super precheck cannot have diverging bounded flags {self.bounded} <--> {other.bounded}")
        if self.lower != other.lower:
            raise Exception(f"sections with matching super precheck cannot have diverging lower bounds {self.lower} <--> {other.lower}")
        if self.upper != other.upper:
            raise Exception(f"sections with matching super precheck cannot have diverging upper bounds {self.upper} <--> {other.upper}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()


class MetaSectionColumnSmartNoiseString(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_STRING)
        name = yaml_dict.pop('name', None)
        cardinality = int(yaml_dict.pop('cardinality', 0))
        return MetaSectionColumnSmartNoiseInt(name, cardinality)

    def __init__(
            self,
            name=None,
            cardinality=0):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_STRING, name)
        self.cardinality = cardinality

    def copy(self):
        return MetaSectionColumnSmartNoiseString(self.name, self.cardinality)

    def to_dict(self):
        dct = super().to_dict()
        dct["cardinality"] = self.cardinality
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.cardinality != other.cardinality:
            raise Exception(f"sections with matching super precheck cannot have diverging cardinalities {self.cardinality} <--> {other.cardinality}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
