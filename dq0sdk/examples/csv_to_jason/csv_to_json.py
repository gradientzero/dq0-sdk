"""Example of dp stats for CSVSource using adult.data

see histograms_dp.ipynb for plots of histograms

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Craig Lincoln <cl@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.data.csv import CSVSource


class AdultCSVSource(CSVSource):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.read_allowed = True
        self.meta_allowed = True


if __name__ == '__main__':
    # data paths.
    path = 'dq0sdk/data/adult/data/'
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.data')

    # init data sourcd
    dc = AdultCSVSource(path_train)
    stats_dict = dc.to_json(0.1)
    print(stats_dict.keys())
    print(stats_dict)
