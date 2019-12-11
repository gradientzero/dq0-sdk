# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all dq0sdk data sources.

Implementing subclasses have to define at least read

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
"""

from dq0sdk.data.source import Source
import pandas as pd
import os


class CSVSource(Source):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        filepath (str): Absolute path to the CSV file.
    """
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def read(self):
        """Read CSV data sources

        Returns:
            CSV data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        path = self.filepath
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not read csv data.'
                          'File not found {}'.format(path))
        return pd.read_csv(path)
