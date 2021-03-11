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

    def __init__(self, path, feature_cols=None, target_cols=None,header=None):
        super().__init__(path)
        self.type = 'csv'
        self.feature_cols = feature_cols
        self.target_cols = target_cols
        if len(header) == 1:
            self.has_header = True

    def read(self, **kwargs):
        """Read CSV data sources

        Args:
            kwargs: keyword arguments

        Returns:
            CSV data as pandas dataframe
        """
        return pd.read_csv(self.path, **kwargs)
