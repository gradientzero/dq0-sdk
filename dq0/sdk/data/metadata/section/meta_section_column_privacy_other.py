from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnPrivacyOther(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_COLUMN_PRIVACY_OTHER:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_COLUMN_PRIVACY_OTHER} was {type_name}")
        name = yaml_dict.pop('name', None)
        synthesizable = bool(yaml_dict.pop('synthesizable', False))
        return MetaSectionColumnPrivacyOther(name, synthesizable)

    def __init__(
            self,
            name=None,
            synthesizable=True):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_PRIVACY_OTHER, name)
        self.synthesizable = synthesizable
