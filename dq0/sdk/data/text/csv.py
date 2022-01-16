# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source class provides access to CSV data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.metadata.utils.utils import Utils as MetaUtils
from dq0.sdk.data.source import Source

import pandas as pd


class CSV(Source):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        path (:obj:`str`): Absolute path to the CSV file.
    """

    def __init__(self, meta_database):
        meta_connector = meta_database.connector
        if meta_connector.type_name != 'csv':
            raise Exception(f"type_name {meta_connector.type_name} does not match csv")
        uri = meta_connector.uri if isinstance(meta_connector.uri, str) else ''
        super().__init__(uri)

        self.type = 'csv'

        use_original_header = meta_connector.use_original_header
        self.use_original_header = True if use_original_header is None else use_original_header

        header_row = meta_connector.header_row
        self.header_row = 0 if header_row is None else header_row  # default assumes single header row

        self.header_columns = meta_connector.header_columns

        sep = meta_connector.sep
        self.sep = ',' if sep is None else sep

        decimal = meta_connector.decimal
        self.decimal = '.' if decimal is None else decimal

        self.na_values = meta_connector.na_values

        self.index_col = meta_connector.index_col

        skipinitialspace = meta_connector.skipinitialspace
        self.skipinitialspace = False if skipinitialspace is None else skipinitialspace

        if len(meta_database) != 0 and len(meta_database.schema()) != 0:
            meta_table = meta_database.schema().table()
            self.feature_cols, self.target_cols = MetaUtils.get_feature_target_cols(meta_table=meta_table)
            self.col_types = MetaUtils.get_col_types(meta_table=meta_table)

    def read(self, **kwargs):
        """Read CSV data sources

        Args:
            kwargs: keyword arguments

        Returns:
            CSV data as pandas dataframe
        """

        if kwargs is not None:  # prioritize kwargs over metadata
            header = kwargs.pop("header", self.header_row)
            names = kwargs.pop("names", self.header_columns)
            skiprows = kwargs.pop("skiprows", [])
            sep = kwargs.pop("sep", self.sep)
            decimal = kwargs.pop("decimal", self.decimal)
            na_values = kwargs.pop("na_values", self.na_values)  # consider combining these
            index_col = kwargs.pop("index_col", self.index_col)
            skipinitialspace = kwargs.pop("skipinitialspace", self.skipinitialspace)

        if not self.use_original_header:  # covers MutliIndex column names
            if isinstance(self.header_row, list) and len(self.header_row) > 1:
                header = 0
                skiprows = skiprows + self.header_row
            elif names is not None:
                header = None

        try:
            return pd.read_csv(self.path, header=header, names=names,
                               skiprows=skiprows, sep=sep, decimal=decimal,
                               na_values=na_values, index_col=index_col,
                               skipinitialspace=skipinitialspace, **kwargs)
        except Exception as e:
            print(
                'Failed to load CSV using use_original_header {}, '
                'header {}, names {}, skiprows {}, sep {}, decimal {}, '
                'na_values {} and kwargs {} due to {}'.format(
                    self.use_original_header, header, names, skiprows,
                    sep, decimal, na_values, kwargs, e))
