from dq0.sdk.data.metadata.meta_node_type import MetaNodeType
from dq0.sdk.data.metadata.section.meta_section_column import MetaSectionColumn, MetaSectionColumnBooleanDatetime, MetaSectionColumnFloat, MetaSectionColumnInt, MetaSectionColumnString
from dq0.sdk.data.metadata.section.meta_section_column_machine_learning import MetaSectionColumnMachineLearning
from dq0.sdk.data.metadata.section.meta_section_column_smart_noise import MetaSectionColumnSmartNoise, MetaSectionColumnSmartNoiseFloat, MetaSectionColumnSmartNoiseInt, MetaSectionColumnSmartNoiseString
from dq0.sdk.data.metadata.section.meta_section_dataset_tags import MetaSectionDatasetTags
from dq0.sdk.data.metadata.section.meta_section_schema_privacy import MetaSectionSchemaPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_differential_privacy import MetaSectionTableDifferentialPrivacy
from dq0.sdk.data.metadata.section.meta_section_table_other import MetaSectionTableOther
from dq0.sdk.data.metadata.section.meta_section_table_privacy import MetaSectionTablePrivacy
from dq0.sdk.data.metadata.section.meta_section_table_smart_noise import MetaSectionTableSmartNoise
from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType


class MetaSectionFactory:
    @staticmethod
    def verifyYamlDict(yaml_dict, expected_type_name=None):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSectionType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if expected_type_name is not None and type_name != expected_type_name:
            raise Exception(f"type_name must be {expected_type_name} was {type_name}")

    @staticmethod
    def metaSectionColumnBooleanDatetimeFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME)
        name = yaml_dict.pop('name', None)
        synthesizable = bool(yaml_dict.pop('synthesizable', False))
        return MetaSectionColumnBooleanDatetime(name, synthesizable)

    @staticmethod
    def metaSectionColumnFloatFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_FLOAT)
        name = yaml_dict.pop('name', None)
        use_auto_bounds = bool(yaml_dict.pop('use_auto_bounds', False))
        auto_bounds_prob = float(yaml_dict.pop('auto_bounds_prob', 0.9))
        auto_lower = float(yaml_dict.pop('auto_lower', 0.0))
        auto_upper = float(yaml_dict.pop('auto_upper', 0.0))
        discrete = bool(yaml_dict.pop('discrete', False))
        min_step = float(yaml_dict.pop('min_step', 1.0))
        synthesizable = bool(yaml_dict.pop('synthesizable', True))
        return MetaSectionColumnFloat(name, use_auto_bounds, auto_bounds_prob, auto_lower, auto_upper, discrete, min_step, synthesizable)

    @staticmethod
    def metaSectionColumnIntFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_INT)
        name = yaml_dict.pop('name', None)
        use_auto_bounds = bool(yaml_dict.pop('use_auto_bounds', False))
        auto_bounds_prob = float(yaml_dict.pop('auto_bounds_prob', 0.9))
        auto_lower = int(yaml_dict.pop('auto_lower', 0))
        auto_upper = int(yaml_dict.pop('auto_upper', 0))
        discrete = bool(yaml_dict.pop('discrete', False))
        min_step = int(yaml_dict.pop('min_step', 1))
        synthesizable = bool(yaml_dict.pop('synthesizable', True))
        return MetaSectionColumnInt(name, use_auto_bounds, auto_bounds_prob, auto_lower, auto_upper, discrete, min_step, synthesizable)


    @staticmethod
    def metaSectionColumnMachineLearningFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING)
        name = yaml_dict.pop('name', None)
        is_feature = bool(yaml_dict.pop('is_feature', False))
        is_target = bool(yaml_dict.pop('is_target', False))
        return MetaSectionColumnMachineLearning(name, is_feature, is_target)

    @staticmethod
    def metaSectionColumnSmartNoiseFloatFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT)
        name = yaml_dict.pop('name', None)
        bounded = bool(yaml_dict.pop('bounded', False))
        lower = float(yaml_dict.pop('lower', 0.0))
        upper = float(yaml_dict.pop('upper', 0.0))
        return MetaSectionColumnSmartNoiseFloat(name, bounded, lower, upper)

    @staticmethod
    def metaSectionColumnSmartNoiseIntromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_INT)
        name = yaml_dict.pop('name', None)
        bounded = bool(yaml_dict.pop('bounded', False))
        lower = int(yaml_dict.pop('lower', 0))
        upper = int(yaml_dict.pop('upper', 0))
        return MetaSectionColumnSmartNoiseInt(name, bounded, lower, upper)

    @staticmethod
    def metaSectionColumnSmartNoiseIntFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_STRING)
        name = yaml_dict.pop('name', None)
        cardinality = int(yaml_dict.pop('cardinality', 0))
        return MetaSectionColumnSmartNoiseInt(name, cardinality)

    @staticmethod
    def metaSectionColumnSmartNoiseFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE)
        name = yaml_dict.pop('name', None)
        private_id = bool(yaml_dict.pop('private_id', False))
        return MetaSectionColumnSmartNoise(name, private_id)

    @staticmethod
    def metaSectionColumnStringFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN_STRING)
        name = yaml_dict.pop('name', None)
        allowed_values = yaml_dict.pop('allowed_values', None)
        mask = yaml_dict.pop('mask', None)
        cardinality = int(yaml_dict.pop('cardinality', 0))
        synthesizable = bool(yaml_dict.pop('synthesizable', cardinality != 0))
        return MetaSectionColumnString(name, allowed_values, mask, cardinality, synthesizable)

    @staticmethod
    def metaSectionColumnFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_COLUMN)
        name = yaml_dict.pop('name', None)
        data_type_name = yaml_dict.pop('data_type_name', None)
        selectable = bool(yaml_dict.pop('selectable', False))
        return MetaSectionColumn(name, data_type_name, selectable)

    @staticmethod
    def metaSectionDatasetTagsFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_DATASET_TAGS)
        name = yaml_dict.pop('name', None)
        tags  = yaml_dict.pop('tags', None)
        return MetaSectionDatasetTags(name, tags)

    @staticmethod
    def metaSectionSchemaPrivacyFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_SCHEMA_PRIVACY)
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        return MetaSectionSchemaPrivacy(name, privacy_level)

    @staticmethod
    def metaSectionTableDifferentialPrivacyFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY)
        name = yaml_dict.pop('name', None)
        budget_epsilon = float(yaml_dict.pop('budget_epsilon', 0.0))
        budget_delta = float(yaml_dict.pop('budget_delta', 0.0))
        return MetaSectionTableDifferentialPrivacy(name, budget_epsilon, budget_delta)

    @staticmethod
    def metaSectionTableOtherFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_TABLE_OTHER)
        name = yaml_dict.pop('name', None)
        synth_allowed = bool(yaml_dict.pop('synth_allowed', False))
        tau = float(yaml_dict.pop('tau', 0.0))
        return MetaSectionTableOther(name, synth_allowed, tau)

    @staticmethod
    def metaSectionTablePrivacyFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_TABLE_PRIVACY)
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        privacy_column = yaml_dict.pop('privacy_column', None)
        return MetaSectionTablePrivacy(name, privacy_level, privacy_column)

    @staticmethod
    def metaSectionTableSmartNoiseFromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict, MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE)
        name = yaml_dict.pop('name', None)
        row_privacy = bool(yaml_dict.pop('row_privacy', False))
        rows = int(yaml_dict.pop('rows', 0))
        max_ids = int(yaml_dict.pop('max_ids', 1))
        sample_max_ids = bool(yaml_dict.pop('sample_max_ids', True))
        use_dpsu = bool(yaml_dict.pop('use_dpsu', False))
        clamp_counts = bool(yaml_dict.pop('clamp_counts', False))
        clamp_columns = bool(yaml_dict.pop('clamp_columns', True))
        censor_dims = bool(yaml_dict.pop('censor_dims', False))
        return MetaSectionTableSmartNoise(name, row_privacy, rows, max_ids, sample_max_ids, use_dpsu, clamp_counts, clamp_columns, censor_dims)

    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSectionFactory.verifyYamlDict(yaml_dict)
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME:
            return MetaSectionFactory.metaSectionColumnBooleanDatetimeFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_FLOAT:
            return MetaSectionFactory.metaSectionColumnFloatFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_INT:
            return MetaSectionFactory.metaSectionColumnIntFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING:
            return MetaSectionFactory.metaSectionColumnMachineLearningFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT:
            return MetaSectionFactory.metaSectionColumnSmartNoiseFloatFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_INT:
            return MetaSectionFactory.metaSectionColumnSmartNoiseIntromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_STRING:
            return MetaSectionFactory.metaSectionColumnSmartNoiseIntFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE:
            return MetaSectionFactory.metaSectionColumnSmartNoiseFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN_STRING:
            return MetaSectionFactory.metaSectionColumnStringFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_COLUMN:
            return MetaSectionFactory.metaSectionColumnFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_DATASET_TAGS:
            return MetaSectionFactory.metaSectionDatasetTagsFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_SCHEMA_PRIVACY:
            return MetaSectionFactory.metaSectionSchemaPrivacyFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY:
            return MetaSectionFactory.metaSectionTableDifferentialPrivacyFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_TABLE_OTHER:
            return MetaSectionFactory.metaSectionTableOtherFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_TABLE_PRIVACY:
            return MetaSectionFactory.metaSectionTablePrivacyFromYamlDict(yaml_dict)
        if type_name == MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE:
            return MetaSectionFactory.metaSectionTableSmartNoiseFromYamlDict(yaml_dict)
        raise Exception(f"no factory configured for type_name {type_name}")

    @staticmethod
    def fromYamlList(yaml_list):
        if yaml_list is None:
            raise Exception("yaml_list is None")
        if not isinstance(yaml_list, list):
            raise Exception("yaml_list is not a list instance")
        sections = []
        for yaml_dict in yaml_list:
            sections.append(MetaSectionFactory.fromYamlDict(yaml_dict))
        return sections    

    @staticmethod
    def generateMissingDefaultSections(node_type_name, existing_sections=[]):
        existing_section_type_names = []
        for existing_section in existing_sections:
            existing_section_type_names.append(existing_section.type_name)
        missing_default_sections = []
        if node_type_name == MetaNodeType.TYPE_NAME_DATASET:
            if MetaSectionType.TYPE_NAME_DATASET_TAGS not in existing_section_type_names:
                missing_default_sections.append(MetaSectionDatasetTags("default dataset tags section"))
        elif node_type_name == MetaNodeType.TYPE_NAME_SCHEMA:
            if MetaSectionType.TYPE_NAME_SCHEMA_PRIVACY not in existing_section_type_names:
                missing_default_sections.append(MetaSectionSchemaPrivacy("default schema privacy section"))
        elif node_type_name == MetaNodeType.TYPE_NAME_TABLE:
            if MetaSectionType.TYPE_NAME_TABLE_DIFFERENTIAL_PRIVACY not in existing_section_type_names:
                missing_default_sections.append(MetaSectionTableDifferentialPrivacy("default table differential privacy section"))
            if MetaSectionType.TYPE_NAME_TABLE_OTHER not in existing_section_type_names:
                missing_default_sections.append(MetaSectionTableOther("default table other section"))
            if MetaSectionType.TYPE_NAME_TABLE_PRIVACY not in existing_section_type_names:
                missing_default_sections.append(MetaSectionTablePrivacy("default table privacy section"))
            if MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE not in existing_section_type_names:
                missing_default_sections.append(MetaSectionTableSmartNoise("default table smart noise section"))
        elif node_type_name == MetaNodeType.TYPE_NAME_COLUMN:
            column_section = None
            for existing_section in existing_sections:
                if existing_section.type_name == MetaSectionType.TYPE_NAME_COLUMN:
                    column_section = existing_section
                    break
            if column_section is None:
                raise Exception(f"nodes of type {node_type_name} must always have an existing section of type {MetaSectionType.TYPE_NAME_COLUMN}")
            if column_section.data_type_name is None:
                raise Exception(f"nodes of type {node_type_name} must always have data_type_name set in a section of type {MetaSectionType.TYPE_NAME_COLUMN}")
            if column_section.data_type_name in ['boolean', 'datetime'] and  MetaSectionType.TYPE_NAME_COLUMN_BOOLEAN_DATETIME not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnBooleanDatetime("default column boolean datetime section"))
            if column_section.data_type_name == 'float' and MetaSectionType.TYPE_NAME_COLUMN_FLOAT not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnFloat("default column float section"))
            if column_section.data_type_name == 'int' and MetaSectionType.TYPE_NAME_COLUMN_INT not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnInt("default column int section"))
            if column_section.data_type_name == 'string' and MetaSectionType.TYPE_NAME_COLUMN_STRING not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnString("default column string section"))
            if MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnSmartNoise("default column smart noise section"))
            if column_section.data_type_name == 'float' and MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_FLOAT not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnSmartNoiseFloat("default column smart noise float section"))
            if column_section.data_type_name == 'int' and MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_INT not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnSmartNoiseInt("default column smart noise int section"))
            if column_section.data_type_name == 'string' and MetaSectionType.TYPE_NAME_COLUMN_SMART_NOISE_STRING not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnSmartNoiseString("default column smart noise string section"))
            if MetaSectionType.TYPE_NAME_COLUMN_MACHINE_LEARNING not in existing_section_type_names:
                missing_default_sections.append(MetaSectionColumnMachineLearning("default column machine learning section"))
        return missing_default_sections
