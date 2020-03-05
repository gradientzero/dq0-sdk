# -*- coding: utf-8 -*-
"""
Adult dataset example for cli.
data source example

Example:
    ./dq0 model create demo
    cd demo
    copy user_source.py to demo/data
    copy user_model.py to demo/model
    ../dq0 data list
    ../dq0 model attach --id <dataset id or uuid>
    ../dq0 model deploy
    ../dq0 model train
    ../dq0 model state
    ../dq0 model predict --input-path </path/to/numpy.npy>
    ../dq0 model state

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
