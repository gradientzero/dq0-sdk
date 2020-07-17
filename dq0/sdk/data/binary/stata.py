# -*- coding: utf-8 -*-
"""Data Source for Stata files.

This source class provides access to stata data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class Stata(Source):
    """Data Source for stata data.

    Provides function to read in stata data.

    Args:
        path (:obj:`str`): Absolute path to the stata file.
    """

    def __init__(self, path):
        super().__init__(path)
        self.type = 'stata'

    def read(self, **kwargs):
        """Read stata data source

        Args:
            kwargs: keyword arguments.

        Returns:
            stata data as pandas dataframe
        """
        return pd.read_stata(self.path, **kwargs)
