from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnPrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_COLUMN_PRIVACY:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_COLUMN_PRIVACY} was {type_name}")
        name = yaml_dict.pop('name', None)
        private_id = bool(yaml_dict.pop('private_id', False))
        selectable = bool(yaml_dict.pop('selectable', False))
        is_feature = bool(yaml_dict.pop('is_feature', False))
        is_target = bool(yaml_dict.pop('is_target', False))
        return MetaSectionColumnPrivacy(name, private_id, selectable, is_feature, is_target)
    
    def __init__(
            self,
            name=None,
            private_id=False,
            selectable=False,
            is_feature=False,
            is_target=False):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_PRIVACY, name)
        self.private_id = private_id
        self.selectable = selectable
        self.is_feature = is_feature
        self.is_target = is_target
