# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all dq0sdk data sources.

Implementing subclasses have to define at least read

Copyright 2020, Gradient Zero
All rights reserved
"""

import uuid
from abc import ABC, abstractmethod


class Source(ABC):
    """Abstract base class for all data connector sources
    available through the SDK.

    Data sources classes provide a read method to read the data into memory or
    provide a data reader for the underlying source.

    Args:
        path (:obj:`str`, optional): Path to the data

    Attributes:
        uuid (:obj:`str`): The universally unique identifier of the data source.
        name (:obj:`str`): The data source's name
        description (:obj:`str`): The data source's description
        data (:obj:`pandas.DataFrame`): The loaded data
        read_allowed (bool): True if this source can be read
        meta_allowed (bool): True if this source provides meta information
        types_allowed (bool): True if this source provides data type information
        stats_allowed (bool): True if this source provides statistics
        sample_allowed (bool): True if there is sample data for this source
        path (:obj:`str`): Path to the data

    """
    def __init__(self, path=None):
        super().__init__()
        self.uuid = uuid.uuid1()  # UUID for this data source. Will be set at runtime.
        self.name = ''
        self.description = ''
        self.data = None
        self.read_allowed = False
        self.meta_allowed = False
        self.types_allowed = False
        self.stats_allowed = False
        self.sample_allowed = False
        self.path = path

    @abstractmethod
    def read(self, **kwargs):
        """Read data sources

        This function should be used by child classes to read data or return
        a data handler to read streaming data.

        Args:
            kwargs: keyword arguments

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_json(self, epsilon=0.1):
        """Returns a json representation of this data sources information.

        Args:
            epsilon (float): Differential Privacy epsilon value. When called
                inside the quarantine (from dq0-main) this value will always
                be set to 0.1

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
