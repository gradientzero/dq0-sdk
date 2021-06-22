# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source class provides access to CSV data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

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
        if meta_ml is not None:
            table = self.meta_ml.get_all_tables()[0]  # Since there is only one table as tested in data_connector
            self.use_original_header = getattr(table, "use_original_header", self.use_original_header)
            self.header_row = getattr(table, "header_row", self.header_row)
            self.header_columns = getattr(table, "header_columns", self.header_columns)

            feature_cols, target_cols = self.meta_ml.get_feature_target_cols()
            self.feature_cols = feature_cols
            self.target_cols = target_cols

            col_types = self.meta_ml.get_col_types()
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

        if not self.use_original_header:  # covers MutliIndex column names
            if isinstance(self.header_row, list) and len(self.header_row) > 1:
                header = 0
                skiprows = skiprows + self.header_row

        try:
            return pd.read_csv(self.path, header=header, names=names, skiprows=skiprows, **kwargs)
        except Exception:
            print(
                'Failed to load CSV with use_original_header {}, '
                'header_row {}, header_columns {} and kwargs {}'.format(
                    self.use_original_header, self. header_row,
                    self.header_columns, kwargs))
