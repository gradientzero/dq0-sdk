from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTablePrivacy(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        if yaml_dict is None:
            raise Exception("yaml_dict is None")
        if not isinstance(yaml_dict, dict):
            raise Exception("yaml_dict is not a dict instance")
        type_name = yaml_dict['type_name'] if 'type_name' in yaml_dict else None
        if not MetaSection.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        if type_name != MetaSection.TYPE_NAME_TABLE_PRIVACY:
            raise Exception(f"type_name must be {MetaSection.TYPE_NAME_TABLE_PRIVACY} was {type_name}")
        name = yaml_dict.pop('name', None)
        privacy_level = int(yaml_dict.pop('privacy_level', 2))
        rows = int(yaml_dict.pop('rows', 0))
        synth_allowed = bool(yaml_dict.pop('synth_allowed', False))
        row_privacy = bool(yaml_dict.pop('row_privacy', False))
        max_ids = int(yaml_dict.pop('max_ids', 1))
        sample_max_ids = bool(yaml_dict.pop('sample_max_ids', True))
        use_dpsu = bool(yaml_dict.pop('use_dpsu', False))
        clamp_counts = bool(yaml_dict.pop('clamp_counts', False))
        clamp_columns = bool(yaml_dict.pop('clamp_columns', True))
        censor_dims = bool(yaml_dict.pop('censor_dims', False))
        tau = float(yaml_dict.pop('tau', 0.0))
        return MetaSectionTablePrivacy(name, privacy_level, rows, synth_allowed, row_privacy, max_ids, sample_max_ids, use_dpsu, clamp_counts, clamp_columns, censor_dims, tau)

    def __init__(
            self, 
            name, 
            privacy_level=2,
            rows=0,
            synth_allowed=False,
            row_privacy=False,
            max_ids=1,
            sample_max_ids=True,
            use_dpsu=False,
            clamp_counts=False,
            clamp_columns=True,
            censor_dims=False,
            tau=0.0):
        super().__init__(MetaSection.TYPE_NAME_TABLE_PRIVACY, name)
        self.privacy_level = privacy_level
        self.rows = rows
        self.synth_allowed = synth_allowed
        self.row_privacy = row_privacy
        self.max_ids = max_ids
        self.sample_max_ids = sample_max_ids
        self.use_dpsu = use_dpsu
        self.clamp_counts = clamp_counts
        self.clamp_columns = clamp_columns
        self.censor_dims = censor_dims
        self.tau = tau
