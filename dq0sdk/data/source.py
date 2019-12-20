# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all dq0sdk data sources.

Implementing subclasses have to define at least read

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

from abc import ABC, abstractmethod


class Source(ABC):
    """Abstract base class for all data connector sources
    available through the SDK.

    Data sources classes provide a read method to read the data into memory or
    provide a data reader for the underlying source.
    """
    def __init__(self):
        super().__init__()
        self.data = None
        self.preprocessed_data = None

    @abstractmethod
    def read(self, force=False):
        """Read data sources

        This function should be used by child classes to read data or return
        a data handler to read streaming data.

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()

    @abstractmethod
    def preprocess(self, force=False, **kwargs):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            force (bool): True to force re-read of the data.
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()
