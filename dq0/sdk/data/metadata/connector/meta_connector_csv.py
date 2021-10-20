from dq0.sdk.data.metadata.connector.meta_connector import MetaConnector


class MetaConnectorCSV(MetaConnector):
    @staticmethod
    def fromYamlDict(yaml_dict):
        MetaConnector.verifyYamlDict(yaml_dict, MetaConnector.TYPE_NAME_CSV)
        uri = yaml_dict.pop('uri', None)
        use_original_header = bool(yaml_dict.pop('use_original_header', True))
        header_row = yaml_dict.pop('header_row', 0)
        header_columns = yaml_dict.pop('header_columns', None)
        sep = yaml_dict.pop('sep', ',')
        decimal = yaml_dict.pop('decimal', '.')
        na_values = yaml_dict.pop('na_values', None)
        index_col = yaml_dict.pop('index_col', None)
        skipinitialspace = bool(yaml_dict.pop('skipinitialspace', False))
        return MetaConnectorCSV(uri, use_original_header, header_row, header_columns, sep, decimal, na_values, index_col, skipinitialspace)

    def __init__(
            self,
            uri=None,
            use_original_header=True,
            header_row=0,
            header_columns=None,
            sep=',',
            decimal='.',
            na_values=None,
            index_col=None,
            skipinitialspace=False):
        super().__init__(MetaConnector.TYPE_NAME_CSV)
        self.uri = uri
        self.use_original_header = use_original_header
        self.header_row = header_row
        self.header_columns = header_columns
        self.sep = sep
        self.decimal = decimal
        self.na_values = na_values
        self.index_col = index_col
        self.skipinitialspace = skipinitialspace

    def copy(self):
        return MetaConnectorCSV(self.uri, self.use_original_header, self.header_row, self.header_columns, self.sep, self.decimal, self.na_values, self.index_col, self.skipinitialspace)

    def to_dict(self):
        dct = super().to_dict()
        dct["uri"] = self.uri
        dct["use_original_header"] = self.use_original_header
        dct["header_row"] = self.header_row
        dct["header_columns"] = self.header_columns
        dct["sep"] = self.sep
        dct["decimal"] = self.decimal
        dct["na_values"] = self.na_values
        dct["index_col"] = self.index_col
        dct["skipinitialspace"] = self.skipinitialspace
        return dct

    def merge_precheck_with(self, other):
        if not super.merge_precheck_with(other):
            return False
        if self.uri != other.uri:
            raise Exception(f"uri must match for merge but {self.uri if self.uri is not None else 'None'} <--> {other.uri if other.uri is not None else 'None'}")
        if self.use_original_header != other.use_original_header:
            raise Exception(f"use_original_header must match for merge but {self.use_original_header} <--> {other.use_original_header if other.use_original_header is not None else 'None'}")
        if self.header_row != other.header_row:
            raise Exception(f"header_row must match for merge but {self.header_row} <--> {other.header_row if other.header_row is not None else 'None'}")
        if self.header_columns != other.header_columns:
            raise Exception(f"header_columns must match for merge but {self.header_columns if self.header_columns is not None else 'None'} <--> {other.header_columns if other.header_columns is not None else 'None'}")
        if self.sep != other.sep:
            raise Exception(f"sep must match for merge but {self.sep} <--> {other.sep if other.sep is not None else 'None'}")
        if self.decimal != other.decimal:
            raise Exception(f"decimal must match for merge but {self.decimal} <--> {other.decimal if other.decimal is not None else 'None'}")
        if self.na_values != other.na_values:
            raise Exception(f"na_values must match for merge but {self.na_values if self.na_values is not None else 'None'} <--> {other.na_values if other.na_values is not None else 'None'}")
        if self.index_col != other.index_col:
            raise Exception(f"index_col must match for merge but {self.index_col if self.index_col is not None else 'None'} <--> {other.index_col if other.index_col is not None else 'None'}")
        if self.skipinitialspace != other.skipinitialspace:
            raise Exception(f"skipinitialspace must match for merge but {self.skipinitialspace} <--> {other.skipinitialspace if other.skipinitialspace is not None else 'None'}")
        return True

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge connectors that fail the precheck")
        return self.copy()
