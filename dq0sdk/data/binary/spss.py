# -*- coding: utf-8 -*-
"""Data Source for SPSS files.

This source class provides access to SPSS data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.source import Source

import pandas as pd


class SPSS(Source):
    """Data Source for SAS data.

    Provides function to read in spss data.

    Args:
        path (:obj:`str`): Absolute path to the spss file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'spss'

    def read(self, **kwargs):
        """Read spss data source

        Args:
            kwargs: keyword arguments.

        Returns:
            spss data as pandas dataframe
        """
        return pd.read_spss(self.path, **kwargs)
