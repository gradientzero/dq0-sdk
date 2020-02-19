# -*- coding: utf-8 -*-
"""User Data Source.

This is a template for user defined data sources.
When training a model on a certain deta source dq0-core is looking for a
UserSource class that is to be used as the custom data source implementation.

This template class derives from Source. Actual implementations should derive
from child classes like CSVSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.source import Source

logger = logging.getLogger()


class UserSource(Source):
    """User Data Source.

    Template. Real implementations should derive from Source child classes.
    For example: UserSource(CSVSource)

    Args:
        filepath (str): Absolute path to the data file.
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
        pass

    def preprocess(self, force=False):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Preprocessed data should be stored in self.data

        Args:
            force (bool): True to force re-read of the data.
        """
        pass

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        pass
