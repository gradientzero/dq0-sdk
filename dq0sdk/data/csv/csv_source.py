# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source class provides access to CSV data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os

from dq0sdk.data.source import Source

import pandas as pd

logger = logging.getLogger()


class CSVSource(Source):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        path (:obj:`str`): Absolute path to the CSV file.
    """
    def __init__(self, path):
        super().__init__(path)

    def read(self, **kwargs):
        """Read CSV data sources

        Args:
            kwargs: keyword arguments

        Returns:
            CSV data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        path = self.path
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not read csv data.'
                          'File not found {}'.format(path))
        return pd.read_csv(path, **kwargs)
