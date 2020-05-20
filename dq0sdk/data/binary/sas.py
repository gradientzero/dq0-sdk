# -*- coding: utf-8 -*-
"""Data Source for SAS files.

This source class provides access to SAS data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.source import Source

import pandas as pd


class SAS(Source):
    """Data Source for SAS data.

    Provides function to read in SAS data.

    Args:
        path (:obj:`str`): Absolute path to the SAS file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'sas'

    def read(self, **kwargs):
        """Read sas data source

        Args:
            kwargs: keyword arguments.

        Returns:
            sas data as pandas dataframe
        """
        return pd.read_sas(self.path, **kwargs)
