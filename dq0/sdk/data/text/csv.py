# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source class provides access to CSV data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source
from dq0.sdk.data.metadata.meta_utils import MetaUtils

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
            table_connector = self.meta_ml.root_node.child_nodes[0].child_nodes[0].child_nodes[0].connector  # Since there is only one table as tested in data_connector
            self.use_original_header = getattr(table_connector, "use_original_header", self.use_original_header)
            self.header_row = getattr(table_connector, "header_row", self.header_row)
            self.header_columns = getattr(table_connector, "header_columns", self.header_columns)
            self.sep = getattr(table_connector, "sep", self.sep)
            self.decimal = getattr(table_connector, "decimal", self.decimal)
            self.na_values = getattr(table_connector, "na_values", self.na_values)
            self.index_col = getattr(table_connector, "index_col", self.index_col)
            self.skipinitialspace = getattr(table_connector, "skipinitialspace", self.skipinitialspace)

            feature_cols, target_cols = MetaUtils.get_feature_target_cols_from_meta(meta_ml)
            self.feature_cols = feature_cols
            self.target_cols = target_cols

            col_types = MetaUtils.get_col_types(meta_ml)
            self.col_types = col_types

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
