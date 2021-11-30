# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source class provides access to CSV data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source
from dq0.sdk.data.metadata.utils import Utils as MetaUtils

import pandas as pd


class CSV(Source):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        path (:obj:`str`): Absolute path to the CSV file.
    """

    def __init__(self, path, meta_ml=None):
        super().__init__(path)
        self.type = 'csv'
        self.meta_ml = meta_ml

        self.use_original_header = True
        self.header_row = 0  # default assumes single header row
        self.header_columns = None
        self.sep = ','
        self.decimal = '.'
        self.na_values = None
        self.index_col = None
        self.skipinitialspace = False
        if meta_ml is not None:
            table_connector = self.meta_ml.node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(key='connector')  # Since there is only one table as tested in data_connector
            self.use_original_header = table_connector.get_attribute(key='use_original_header', default=self.use_original_header) if table_connector is not None else self.use_original_header
            self.header_row = table_connector.get_attribute(key='header_row', default=self.header_row) if table_connector is not None else self.header_row
            self.header_columns = MetaUtils.get_header_columns_from_meta(metadata=meta_ml)
            self.sep = table_connector.get_attribute(key='sep', default=self.sep) if table_connector is not None else self.sep
            self.decimal = table_connector.get_attribute(key='decimal', default=self.decimal) if table_connector is not None else self.decimal
            tmp_na_values = table_connector.get_attribute(key='na_values') if table_connector is not None else None
            self.na_values = tmp_na_values.to_dict() if tmp_na_values is not None else self.na_values
            self.index_col = table_connector.get_attribute(key='index_col', default=self.index_col) if table_connector is not None else self.index_col
            self.skipinitialspace = table_connector.get_attribute(key='skipinitialspace', default=self.skipinitialspace) if table_connector is not None else self.skipinitialspace
            self.feature_cols, self.target_cols = MetaUtils.get_feature_target_cols_from_meta(metadata=meta_ml)
            self.col_types = MetaUtils.get_col_types(metadata=meta_ml)

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
        except Exception:
            print(
                'Failed to load CSV using use_original_header {}, '
                'header {}, names {}, skiprows {}, sep {}, decimal {}, '
                'na_values {} and kwargs {}'.format(
                    self.use_original_header, header, names, skiprows,
                    sep, decimal, na_values, kwargs))
