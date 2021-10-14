from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnPrivacyString(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_COLUMN_PRIVACY_STRING:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_COLUMN_PRIVACY_STRING} was {type_name}")
        name = yaml_dict.pop('name', None)
        cardinality = int(yaml_dict.pop('cardinality', 0))
        allowed_values = yaml_dict.pop('allowed_values', None)
        mask = yaml_dict.pop('use_auto_bounds', None)
        synthesizable = bool(yaml_dict.pop('synthesizable', cardinality != 0))
        return MetaSectionColumnPrivacyString(name, cardinality, allowed_values, mask, synthesizable)

    def __init__(
            self,
            name=None,
            cardinality=0,
            allowed_values=None,
            mask=None,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_PRIVACY_STRING, name)
        self.cardinality = cardinality
        self.allowed_values = allowed_values
        self.mask = mask
        self.synthesizable = synthesizable
