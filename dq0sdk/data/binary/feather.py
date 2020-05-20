# -*- coding: utf-8 -*-
"""Data Source for Apache Arrow Feather files.

This source class provides access to feather data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.source import Source

import pandas as pd


class Feather(Source):
    """Data Source for Apache Arrow Feather data.

    Provides function to read in feather data.

    Args:
        path (:obj:`str`): Absolute path to the feather file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'feather'

    def read(self, **kwargs):
        """Read feather data source

        Args:
            kwargs: keyword arguments.

        Returns:
            feather data as pandas dataframe
        """
        return pd.read_feather(self.path, **kwargs)
