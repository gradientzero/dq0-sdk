from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType
from dq0.sdk.data.metadata.section.meta_section import MetaSection


class MetaSectionTableSmartNoise(MetaSection):
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
        super().__init__(MetaSectionType.TYPE_NAME_TABLE_SMART_NOISE, name)
        self.row_privacy = row_privacy
        self.rows = rows
        self.max_ids = max_ids
        self.sample_max_ids = sample_max_ids
        self.use_dpsu = use_dpsu
        self.clamp_counts = clamp_counts
        self.clamp_columns = clamp_columns
        self.censor_dims = censor_dims

    def copy(self):
        return MetaSectionTableSmartNoise(self.name, self.row_privacy, self.rows, self.max_ids, self.sample_max_ids, self.use_dpsu, self.clamp_counts, self.clamp_columns, self.censor_dims)

    def to_dict(self):
        super_dct = super().to_dict()
        dct = {k: v for k, v in [
            ('row_privacy', self.row_privacy),
            ('rows', self.rows),
            ('max_ids', self.max_ids),
            ('sample_max_ids', self.sample_max_ids),
            ('use_dpsu', self.use_dpsu),
            ('clamp_counts', self.clamp_counts),
            ('clamp_columns', self.clamp_columns),
            ('censor_dims', self.censor_dims),
            ] if v is not None}
        return {**super_dct, **dct}

    def merge_precheck_with(self, other):
        if not super().merge_precheck_with(other):
            return False
        if self.row_privacy != other.row_privacy:
            raise Exception(f"sections with matching super precheck cannot have diverging row_privacy flags {self.row_privacy} <--> {other.row_privacy}")
        if self.rows != other.rows:
            raise Exception(f"sections with matching super precheck cannot have diverging rows {self.rows} <--> {other.rows}")
        if self.max_ids != other.max_ids:
            raise Exception(f"sections with matching super precheck cannot have diverging max_ids {self.max_ids} <--> {other.max_ids}")
        if self.sample_max_ids != other.sample_max_ids:
            raise Exception(f"sections with matching super precheck cannot have diverging sample_max_ids flags {self.sample_max_ids} <--> {other.sample_max_ids}")
        if self.use_dpsu != other.use_dpsu:
            raise Exception(f"sections with matching super precheck cannot have diverging use_dpsu flags {self.use_dpsu} <--> {other.use_dpsu}")
        if self.clamp_counts != other.clamp_counts:
            raise Exception(f"sections with matching super precheck cannot have diverging clamp_counts flags {self.clamp_counts} <--> {other.clamp_counts}")
        if self.clamp_columns != other.clamp_columns:
            raise Exception(f"sections with matching super precheck cannot have diverging clamp_columns flags {self.clamp_columns} <--> {other.clamp_columns}")
        if self.censor_dims != other.censor_dims:
            raise Exception(f"sections with matching super precheck cannot have diverging censor_dims flags {self.censor_dims} <--> {other.censor_dims}")
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
