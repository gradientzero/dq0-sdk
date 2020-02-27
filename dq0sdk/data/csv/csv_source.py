# -*- coding: utf-8 -*-
"""Data Source for CSV files.

This source call provides access to CSV data as pandas dataframes.

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Craig Lincoln <cl@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import logging
import os

from dq0sdk.data.source import Source
from dq0sdk.data.utils.dp_methods import _dp_stats

import pandas as pd

logger = logging.getLogger()


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

    def to_json(self, epsilon=0.1):  # noqa: C901
        """Returns a json representation of this data sources information.

        Args:
            epsilon (float): Differential Privacy epsilon value

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        length = 0
        mean = ''
        std = ''
        hist = ''
        types = ''
        content = None
        if self.read_allowed:
            try:
                content = self.read()
            except Exception as e:
                logger.fatal('Could not read content. {}'.format(e))

        if self.stats_allowed and content is not None:
            try:
                dp_mean, dp_std, dp_hist = _dp_stats(content, epsilon)
                length = int(content.size)
                mean = '{}'.format(dp_mean)
                std = '{}'.format(dp_std)
                hist = '{}'.format(dp_hist)
            except Exception as e:
                logger.warn('Could not get stats for content. {}'.format(e))

        if self.types_allowed and content is not None:
            try:
                types = '{}'.format(content.dtypes)
            except Exception as e:
                logger.warn('Could not get types for content. {}'.format(e))

        permissions = []
        if self.read_allowed:
            permissions.append('read')
        if self.meta_allowed:
            permissions.append('meta')
        if self.types_allowed:
            permissions.append('types')
        if self.stats_allowed:
            permissions.append('stats')
        if self.sample_allowed:
            permissions.append('sample')

        return {
            "name": self.name,
            "type": 'csv',
            "filepath": self.filepath,
            "length": length,
            "permissions": permissions,
            "mean": mean,
            "std": std,
            'hist': hist,
            "types": types
        }
