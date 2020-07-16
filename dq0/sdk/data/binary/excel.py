# -*- coding: utf-8 -*-
"""Data Source for MS Excel files.

This source class provides access to Excel data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class Excel(Source):
    """Data Source for MS Excel data.

    Provides function to read in excel data.

    Args:
        path (:obj:`str`): Absolute path to the Excel file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'excel'

    def read(self, **kwargs):
        """Read excel data source

        Args:
            kwargs: keyword arguments.
                Should contain a 'sheet_name' argument to specify which excel sheet to load (None for all).

        Returns:
            excel data as pandas dataframe
        """
        return pd.read_excel(self.path, **kwargs)
