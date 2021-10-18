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

    def copy(self):
        return MetaSectionColumnMachineLearning(self.name, self.is_feature, self.is_target)

    def to_dict(self):
        dct = super().to_dict()
        dct["is_feature"] = self.is_feature
        dct["is_target"] = self.is_target
        return dct

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.is_feature != other.is_feature:
            raise Exception(f"sections with matching super precheck cannot have diverging is_feature flags {self.is_feature} <--> {other.is_feature}")
        if self.is_target != other.is_target:
            raise Exception(f"sections with matching super precheck cannot have diverging is_target flags {self.is_target} <--> {other.is_target}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
