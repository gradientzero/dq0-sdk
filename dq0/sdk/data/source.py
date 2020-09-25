# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all data sources.

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
        type (:obj:`str`): The data source's distinct type (e.g. 'csv')
        description (:obj:`str`): The data source's description
        types: json object containing column type description
        data (:obj:`pandas.DataFrame`): The loaded data
        read_allowed (bool): True if this source can be read
        meta_allowed (bool): True if this source provides meta information
        types_allowed (bool): True if this source provides data type information
        stats_allowed (bool): True if this source provides statistics
        sample_allowed (bool): True if there is sample data for this source
        path (:obj:`str`): Path to the data
        sample_path (:obj:`str`): Absolute path to the file containing sample data.
    """

    def __init__(self, path=None):
        super().__init__()
        self.uuid = uuid.uuid1()  # UUID for this data source. Will be set at runtime.
        self.name = ''
        self.description = ''
        self.type = ''
        self.data = None
        self.read_allowed = False
        self.meta_allowed = False
        self.types_allowed = False
        self.stats_allowed = False
        self.sample_allowed = False
        self.path = path
        self.sample_path = None

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

    def to_json(self):  # noqa: C901
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        permissions = []
        if self.read_allowed:
            permissions.append('read')
        if self.meta_allowed:
            permissions.append('meta')
        if self.types_allowed:
            permissions.append('types')
        if self.stats_allowed:
            permissions.append('stats')
        if self.sample_allowed:
            permissions.append('sample')

        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "filepath": self.path,
            "samplepath": self.sample_path,
            "permissions": permissions,
            "types": self.types
        }
