# -*- coding: utf-8 -*-
"""Example of dp stats for CSVSource using adult.data

Example:
    >>> ../dq0 data list # doctest: +SKIP
    >>> ../dq0 data info --uuid <UUID-OF-SOURCE> # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.data.csv import CSVSource


class AdultCSVSource(CSVSource):
    """User defined data source for Census dataset."""
    def __init__(self, filepath):
        super().__init__(filepath)
        self.read_allowed = True
        self.meta_allowed = True
        self.stats_allowed = True
        self.types_allowed = True


if __name__ == '__main__':
    # data paths.
    path = 'dq0sdk/examples/census/data/'
    path_train = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../../',
        path,
        'adult_whole_processed.csv')

    # init data source
    dc = AdultCSVSource(path_train)

    # get data info
    stats_dict = dc.to_json()
    print(stats_dict.keys())
    print(stats_dict)
