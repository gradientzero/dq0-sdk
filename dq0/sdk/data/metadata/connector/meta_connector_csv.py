from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorCSV(MetaConnector):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaConnector.verifyYamlDict(yaml_dict, MetaConnector.TYPE_NAME_CSV)
        use_original_header = bool(yaml_dict.pop('use_original_header', True))
        header_row = yaml_dict.pop('header_row', 0)
        header_columns = yaml_dict.pop('header_columns', None)
        sep = yaml_dict.pop('sep', ',')
        decimal = yaml_dict.pop('decimal', '.')
        na_values = yaml_dict.pop('na_values', None)
        index_col = yaml_dict.pop('index_col', None)
        skipinitialspace = bool(yaml_dict.pop('skipinitialspace', False))
        return MetaConnectorCSV(use_original_header, header_row, header_columns, sep, decimal, na_values, index_col, skipinitialspace)

    def __init__(
            self,
            use_original_header=True,
            header_row=0,
            header_columns=None,
            sep=',',
            decimal='.',
            na_values=None,
            index_col=None,
            skipinitialspace=False):
        super().__init__(MetaConnector.TYPE_NAME_CSV)
        self.use_original_header = use_original_header
        self.header_row = header_row
        self.header_columns = header_columns
        self.sep = sep
        self.decimal = decimal
        self.na_values = na_values
        self.index_col = index_col
        self.skipinitialspace = skipinitialspace
