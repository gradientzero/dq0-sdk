# -*- coding: utf-8 -*-
"""Data Source for dq0 demo files.

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

from dq0sdk.data.csv.csv_source import CSVSource

logger = logging.getLogger()


class UserSource(CSVSource):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        filepath (str): Absolute path to the CSV file.
    """
    def __init__(self, filepath):
        super().__init__(filepath)
        self.filepath = filepath
        self.data = None
 