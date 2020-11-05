# -*- coding: utf-8 -*-
"""Data Source base class for SQL-based data sources.

Copyright 2020, Gradient Zero
All rights reserved
"""
from abc import abstractmethod

from dq0.sdk.data.source import Source


class SQL(Source):
    """Data Source base class for SQL data.

    Attributes:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): General purpose SQL data source connection string.

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): General purpose SQL data source connection string.
    """

    def __init__(self, query, connection):
        super().__init__('')
        self.query = query
        self.connection = connection
        self.engine = None
        self.type = 'sql'

    @abstractmethod
    def execute(self, query=None, **kwargs):
        """Execute SQL query

        This function should be used by child classes to execeute SQL queries

        Args:
            query: SQL Query to execute
            kwargs: keyword arguments

        Returns:
            SQL ResultSet as pandas dataframe
        """
        raise NotImplementedError()

    def read(self, **kwargs):
        """Runs overriden 'execute' method with query parameter

        Args:
            kwargs: keyword arguments

        Returns:
            CSV data as pandas dataframe
        """
        self.execute(query=self.query, **kwargs)

    def to_json(self):  # noqa: C901
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        json = super().to_json()
        json["query"] = self.query

        return json
