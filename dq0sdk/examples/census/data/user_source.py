# -*- coding: utf-8 -*-
"""
Adult dataset example for cli.
data source example

Example:
    >>> ./dq0 project create --name demo # doctest: +SKIP
    >>> cd demo # doctest: +SKIP
    >>> copy user_source.py to demo/data/ # doctest: +SKIP
    >>> copy user_model.py to demo/model/ # doctest: +SKIP
    >>> ../dq0 data list # doctest: +SKIP
    >>> ../dq0 model attach --id <dataset id> # doctest: +SKIP
    >>> ../dq0 project deploy # doctest: +SKIP
    >>> ../dq0 model train # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP
    >>> ../dq0 model predict --input-path </path/to/numpy.npy> # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.csv.csv_source import CSVSource

logger = logging.getLogger()


class UserSource(CSVSource):
    """Data Source for CSV data.

    Provides function to read in csv data.

    Args:
        filepath (:obj:`str`): Absolute path to the CSV file.
    """
    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = None
