# -*- coding: utf-8 -*-
"""Data Source for census adult data set - preprocssed version.

This data source reads a csv that contains the results from
`CensusSource.preprocess()`

Uses the `read()` function from the parent class `CSVSource`

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.csv import CSVSource


class CensusSourcePreprocessed(CSVSource):
    """Data Source for the preprocessed adult dataset.

    Provides function to read the preprocessed adult dataset.

    Args:
        filepath (:obj:`str`): Path to the data set csv
    """
    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = None
