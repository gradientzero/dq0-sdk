# -*- coding: utf-8 -*-
"""Data Source for HDF5 PyTables files.

This source class provides access to hdf5 data as pandas dataframes.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

import pandas as pd


class HDF5(Source):
    """Data Source for HDF5 PyTables data.

    Provides function to read in hdf5 data.

    Args:
        path (:obj:`str`): Absolute path to the hdf5 file.
    """

    def __init__(self, path):
        super().__init__(path)
        self.type = 'hdf5'

    def read(self, **kwargs):
        """Read hdf5 data source

        Args:
            kwargs: keyword arguments.
                Can contain a 'key' argument to specify a group within the pytable.

        Returns:
            hdf5 data as pandas dataframe
        """
        return pd.read_hdf(self.path, **kwargs)
