# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all dq0 data sources.

Implementing subclasses have to define at least read

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
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

    @abstractmethod
    def read(self):
        """Read data sources

        This function should be used by child classes to read data or return
        a data handler to read streaming data.

        Returns:
            data read from the data source.
        """
        pass
