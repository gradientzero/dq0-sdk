# -*- coding: utf-8 -*-
"""Data Source for Apache ORC files.

This source class provides access to orc data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class ORC(Source):
    """Data Source for Apache ORC data.

    Provides function to read in orc data.

    Args:
        path (:obj:`str`): Absolute path to the orc file.
    """

    def __init__(self, path):
        super().__init__(path)
        self.type = 'orc'

    def read(self, **kwargs):
        """Read orc data source

        Args:
            kwargs: keyword arguments.
                May contain columns to define columsn to read.

        Returns:
            orc data as pandas dataframe
        """
        return pd.read_orc(self.path, **kwargs)
