# -*- coding: utf-8 -*-
"""Data Source for JSON files.

This source class provides access to JSON data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class JSON(Source):
    """Data Source for JSON data.

    Provides function to read in json data.

    Args:
        path (:obj:`str`): Absolute path to the JSON file.
    """

    def __init__(self, path):
        super().__init__(path)
        self.type = 'json'

    def read(self, **kwargs):
        """Read json data sources

        Args:
            kwargs: keyword arguments

        Returns:
            json data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        return pd.read_json(self.path, **kwargs)
