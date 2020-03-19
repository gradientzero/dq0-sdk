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

import uuid
from abc import ABC, abstractmethod


class Source(ABC):
    """Abstract base class for all data connector sources
    available through the SDK.

    Data sources classes provide a read method to read the data into memory or
    provide a data reader for the underlying source.
    """
    def __init__(self, input_folder=None):
        super().__init__()
        self.uuid = uuid.uuid1()  # UUID for this data source. Will be set at runtime.
        self.name = ''
        self.data = None
        self.preprocessed_data = None
        self.read_allowed = False
        self.meta_allowed = False
        self.types_allowed = False
        self.stats_allowed = False
        self.sample_allowed = False
        self.input_folder = input_folder

    @abstractmethod
    def read(self):
        """Read data sources

        This function should be used by child classes to read data or return
        a data handler to read streaming data.

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()

    @abstractmethod
    def preprocess(self):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
