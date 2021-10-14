from dq0.sdk.data.metadata.section.meta_section_schema_privacy import MetaSectionSchemaPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_differential_privacy import MetaSectionTableDifferentialPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_privacy import MetaSectionTablePrivacy
from dq0.sdk.data.metadata.section.meta_section_column_privacy import MetaSectionColumnPrivacy
from dq0.sdk.data.metadata.section.meta_section_column_privacy_float import MetaSectionColumnPrivacyFloat
from dq0.sdk.data.metadata.section.meta_section_column_privacy_int import MetaSectionColumnPrivacyInt
from dq0.sdk.data.metadata.section.meta_section_column_privacy_other import MetaSectionColumnPrivacyOther
from dq0.sdk.data.metadata.section.meta_section_column_privacy_string import MetaSectionColumnPrivacyString


class MetaSection:
    TYPE_NAME_SCHEMA_PRIVACY = 'schema_privacy'
    TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY = 'table_differential_privacy'
    TYPE_NAME_TABLE_PRIVACY = 'table_privacy'
    TYPE_NAME_COLUMN_PRIVACY = 'column_privacy'
    TYPE_NAME_COLUMN_PRIVACY_OTHER = 'column_privacy_other'
    TYPE_NAME_COLUMN_PRIVACY_INT = 'column_privacy_int'
    TYPE_NAME_COLUMN_PRIVACY_FLOAT = 'column_privacy_float'
    TYPE_NAME_COLUMN_PRIVACY_STRING = 'column_privacy_string'

    @staticmethod
    def isValidTypeName(type_name):
        if type_name is None:
            return False
        if type_name == MetaSection.TYPE_NAME_SCHEMA_PRIVACY or type_name == MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY or type_name == MetaSection.TYPE_NAME_TABLE_PRIVACY or type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY or type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_OTHER or type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_INT or type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_FLOAT or type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_STRING:
            return True
        return False

    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict.pop('type_name', None)
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name == MetaSection.TYPE_NAME_SCHEMA_PRIVACY:
            return MetaSectionSchemaPrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY:
            return MetaSectionTableDifferentialPrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_TABLE_PRIVACY:
            return MetaSectionTablePrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY:
            return MetaSectionColumnPrivacy.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_OTHER:
            return MetaSectionColumnPrivacyOther.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_INT:
            return MetaSectionColumnPrivacyInt.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_FLOAT:
            return MetaSectionColumnPrivacyFloat.fromYamlDict(yaml_dict)
        if type_name == MetaSection.TYPE_NAME_COLUMN_PRIVACY_STRING:
            return MetaSectionColumnPrivacyString.fromYamlDict(yaml_dict)
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

    def __init__(
            self,
            type_name,
            name):
        self.type_name = type_name
        self.name = name
