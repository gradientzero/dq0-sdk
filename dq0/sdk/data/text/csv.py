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

    def __init__(self, path, use_original_header=None, header_row=None,
                 header_columns=None, feature_cols=None, target_cols=None,
                 col_types=None):
        super().__init__(path)
        self.type = 'csv'
        self.feature_cols = feature_cols
        self.target_cols = target_cols
        self.use_original_header = use_original_header
        self.header_row = header_row
        self.header_columns = header_columns
        self.col_types = col_types
        # if header is not None:
        #     if len(header) == 1:
        #         self.has_header = True

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
        except:
            print('Failed to load CSV with use_original_header {}, '
            'header_row {}, header_columns {} and kwargs {}'.format(
                self.use_original_header, self. header_row,
                self.header_columns, kwargs))

