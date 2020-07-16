# -*- coding: utf-8 -*-
"""Data Source for Apache Parquet files.

This source class provides access to parquet data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class Parquet(Source):
    """Data Source for Apache Parquet data.

    Provides function to read in parquet data.

    Args:
        path (:obj:`str`): Absolute path to the parquet file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'parquet'

    def read(self, **kwargs):
        """Read parquet data source

        Args:
            kwargs: keyword arguments.
                May contain 'engine' to define whether to use pyarrow or fastparquet.
                May contain columns to define columsn to read.

        Returns:
            parquet data as pandas dataframe
        """
        return pd.read_parquet(self.path, **kwargs)
