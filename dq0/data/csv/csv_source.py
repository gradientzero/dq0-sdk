# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source call provides access to CSV data as pandas dataframes.

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
"""

import os

from dq0.data.source import Source

import pandas as pd


class CSVSource(Source):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        filepath (str): Absolute path to the CSV file.
    """
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def read(self, force=False):
        """Read CSV data sources

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            CSV data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        if not force and self.data is not None:
            return self.data

        path = self.filepath
        if not os.path.exists(path) or not os.path.isfile(path):
            raise IOError('Could not read csv data.'
                          'File not found {}'.format(path))
        return pd.read_csv(path)

    def preprocess(self, force=False, **kwargs):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            force (bool): True to force re-read of the data.
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            preprocessed data
        """
        if not force and self.preprocessed_data is not None:
            return self.preprocessed_data

        self.preprocessed_data = self.data
        return self.preprocessed_data
