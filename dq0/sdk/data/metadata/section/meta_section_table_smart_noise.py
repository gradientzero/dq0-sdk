from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableSmartNoise(MetaSection):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaSection.verifyYamlDict(yaml_dict, MetaSection.TYPE_NAME_TABLE_SMART_NOISE)
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

    def __init__(
            self,
            name,
            row_privacy=False,
            rows=0,
            max_ids=1,
            sample_max_ids=True,
            use_dpsu=False,
            clamp_counts=False,
            clamp_columns=True,
            censor_dims=False):
        super().__init__(MetaSection.TYPE_NAME_TABLE_SMART_NOISE, name)
        self.row_privacy = row_privacy
        self.rows = rows
        self.max_ids = max_ids
        self.sample_max_ids = sample_max_ids
        self.use_dpsu = use_dpsu
        self.clamp_counts = clamp_counts
        self.clamp_columns = clamp_columns
        self.censor_dims = censor_dims
