from pathlib import Path

from dq0.sdk.connector.connector import Connector
from dq0.sdk.connector.connector_kind import ConnectorKind

import pandas


class CSV(Connector):
    @staticmethod
    def csv_from(meta_connector):
        if meta_connector.type_name != 'csv':
            raise ValueError(f"type_name={meta_connector.type_name} != csv")
        filepath = meta_connector.uri
        if len(filepath) == 0:
            raise ValueError("uri not specified")
        sep = meta_connector.sep if meta_connector.sep is not None else ','
        header = meta_connector.header_row if meta_connector.header_row is not None else 'infer'
        names = meta_connector.header_columns
        index_col = meta_connector.index_col
        skipinitialspace = meta_connector.skipinitialspace \
            if meta_connector.skipinitialspace is not None else False
        na_values = meta_connector.na_values
        decimal = meta_connector.decimal if meta_connector.decimal is not None else '.'
        return CSV(filepath=filepath, sep=sep, header=header, names=names, index_col=index_col,
                   skipinitialspace=skipinitialspace, na_values=na_values, decimal=decimal)

    def __init__(self, filepath, sep=',', header='infer', names=None, index_col=None,
                 skipinitialspace=False, na_values=None, decimal='.'):
        super().__init__(ConnectorKind.CSV)
        self._filepath = Path(filepath)
        if not self._filepath.is_file():
            raise ValueError(f"filepath={filepath} is not a file")
        self._sep = sep
        self._header = header
        self._names = names
        self._index_col = index_col
        self._skipinitialspace = skipinitialspace
        self._na_values = na_values
        self._decimal = decimal

    def get_filepath(self):
        return self._filepath

    def get_sep(self):
        return self._sep

    def get_header(self):
        return self._header

    def get_names(self):
        return self._names

    def get_index_col(self):
        return self._index_col

    def get_skipinitialspace(self):
        return self._skipinitialspace

    def get_na_values(self):
        return self._na_values

    def get_decimal(self):
        return self._decimal

    def to_pandas(self):
        return pandas.read_csv(filepath=self._filepath, sep=self._sep, header=self._header,
                               names=self._names, index_col=self._index_col,
                               skipinitialspace=self._skipinitialspace, na_values=self._na_values,
                               decimal=self._decimal)
