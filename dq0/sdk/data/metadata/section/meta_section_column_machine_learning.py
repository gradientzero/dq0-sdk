from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionColumnMachineLearning(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_COLUMN_MACHINE_LEARNING)
        name = yaml_dict.pop('name', None)
        is_feature = bool(yaml_dict.pop('is_feature', False))
        is_target = bool(yaml_dict.pop('is_target', False))
        return MetaSectionColumnMachineLearning(name, is_feature, is_target)
    
    def __init__(
            self,
            name=None,
            is_feature=False,
            is_target=False):
        super().__init__(MetaSection.TYPE_NAME_COLUMN_MACHINE_LEARNING, name)
        self.is_feature = is_feature
        self.is_target = is_target
