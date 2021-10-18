from dq0.sdk.data.metadata.section.meta_section_column import MetaSectionColumn, MetaSectionColumnBooleanDatetime, MetaSectionColumnFloat, MetaSectionColumnInt, MetaSectionColumnString
from dq0.sdk.data.metadata.section.meta_section_column_machine_learning import MetaSectionColumnMachineLearning
from dq0.sdk.data.metadata.section.meta_section_column_smart_noise import MetaSectionColumnSmartNoise, MetaSectionColumnSmartNoiseFloat, MetaSectionColumnSmartNoiseInt, MetaSectionColumnSmartNoiseString
from dq0.sdk.data.metadata.section.meta_section_schema_privacy import MetaSectionSchemaPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_differential_privacy import MetaSectionTableDifferentialPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_other import MetaSectionTableOther
from dq0.sdk.data.metadata.section.meta_section_table_privacy import MetaSectionTablePrivacy
from dq0.sdk.data.metadata.section.meta_section_table_smart_noise import MetaSectionTableSmartNoise


class MetaSection:
    TYPE_NAME_COLUMN = 'column'
    TYPE_NAME_COLUMN_BOOLEAN_DATETIME = 'column_boolean_datetime'
    TYPE_NAME_COLUMN_FLOAT = 'column_float'
    TYPE_NAME_COLUMN_INT = 'column_int'
    TYPE_NAME_COLUMN_MACHINE_LEARNING = 'column_machine_learning'
    TYPE_NAME_COLUMN_SMART_NOISE = 'column_smart_noise'
    TYPE_NAME_COLUMN_SMART_NOISE_FLOAT = 'column_smart_noise_float'
    TYPE_NAME_COLUMN_SMART_NOISE_INT = 'column_smart_noise_int'
    TYPE_NAME_COLUMN_SMART_NOISE_STRING = 'column_smart_noise_string'
    TYPE_NAME_COLUMN_STRING = 'column_string'
    TYPE_NAME_SCHEMA_PRIVACY = 'schema_privacy'
    TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY = 'table_differential_privacy'
    TYPE_NAME_TABLE_OTHER = 'table_other'
    TYPE_NAME_TABLE_PRIVACY = 'table_privacy'
    TYPE_NAME_TABLE_SMART_NOISE = 'table_smart_noise'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if \
                type_name == MetaSection.TYPE_NAME_COLUMN or \
                type_name == MetaSection.TYPE_NAME_COLUMN_BOOLEAN_DATETIME or \
                type_name == MetaSection.TYPE_NAME_COLUMN_FLOAT or \
                type_name == MetaSection.TYPE_NAME_COLUMN_INT or \
                type_name == MetaSection.TYPE_NAME_COLUMN_MACHINE_LEARNING or \
                type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE or \
                type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT or \
                type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_INT or \
                type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_STRING or \
                type_name == MetaSection.TYPE_NAME_COLUMN_STRING or \
                type_name == MetaSection.TYPE_NAME_SCHEMA_PRIVACY or \
                type_name == MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY or \
                type_name == MetaSection.TYPE_NAME_TABLE_OTHER or \
                type_name == MetaSection.TYPE_NAME_TABLE_PRIVACY or \
                type_name == MetaSection.TYPE_NAME_TABLE_SMART_NOISE:
            return True
        return False

    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict.pop('type_name', None)
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")
        return type_name

    @staticmethod
    def fromYamlDict(yaml_dict):
        type_name = MetaSection.verifyYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN:
            return MetaSectionColumn.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_BOOLEAN_DATETIME:
            return MetaSectionColumnBooleanDatetime.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_FLOAT:
            return MetaSectionColumnFloat.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_INT:
            return MetaSectionColumnInt.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_MACHINE_LEARNING:
            return MetaSectionColumnMachineLearning.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE:
            return MetaSectionColumnSmartNoise.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT:
            return MetaSectionColumnSmartNoiseFloat.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_INT:
            return MetaSectionColumnSmartNoiseInt.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_SMART_NOISE_STRING:
            return MetaSectionColumnSmartNoiseString.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_STRING:
            return MetaSectionColumnString.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_SCHEMA_PRIVACY:
            return MetaSectionSchemaPrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY:
            return MetaSectionTableDifferentialPrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_OTHER:
            return MetaSectionTableOther.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_PRIVACY:
            return MetaSectionTablePrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_SMART_NOISE:
            return MetaSectionTableSmartNoise.fromYamlDict(yaml_dict)
        raise Exception(f"no factory configured for type_name {type_name}")

    @staticmethod
    def fromYamlList(yaml_list):
        if yaml_list is None:
            raise Exception("yaml_list is None")
        if not isinstance(yaml_list, list):
            raise Exception("yaml_list is not a list instance")
        sections = []
        for yaml_dict in yaml_list:
            sections.append(MetaSection.fromYamlDict(yaml_dict))
        return sections    

    @staticmethod
    def merge_many(lst_a, lst_b):
        if lst_a is None:
            return lst_b
        if lst_b is None:
            return lst_a
        merged = []
        for elem_a in lst_a:
            elem_merged = elem_a.copy()
            for elem_b in lst_b:
                if elem_a.merge_precheck_with(elem_b):
                    lst_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(elem_b)
                    break
            merged.append(elem_merged)
        for elem_b in lst_b:
            for elem_a in lst_a:
                if elem_b.merge_precheck_with(elem_a):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(
            self,
            type_name,
            name):
        self.type_name = type_name
        self.name = name

    def copy(self):
        return MetaSection(self.type_name, self.name)

    def to_dict(self):
        return {
            "type_name": self.type_name,
            "name": self.name,
        }

    def merge_precheck_with(self, other):
        if other is None or self.type_name != other.type_name or self.name != other.name:
            return False
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
