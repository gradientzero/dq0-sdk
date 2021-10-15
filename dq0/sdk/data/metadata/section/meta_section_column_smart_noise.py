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
