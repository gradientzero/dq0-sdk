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
        connection_string (:obj:`str`): General purpose SQL data source connection string.
        engine: the used sqlalchemy engine
        engine_connection: the active sql connection
        type: the datasource type

    Args:
        connection (:obj:`str`): General purpose SQL data source connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.query = None
        self.connection_string = connection_string
        self.engine = None
        self.connection = None
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

    def get_connection(self):
        """Returns the active sql connection.

        Initiates the connection if not already done.

        Returns:
            Active sql connection. Throws error if engine is not set.
        """
        if self.connection is not None:
            return self.connection

        if self.engine is None:
            raise ValueError('could not find valid engine')

        self.connection = self.engine.connect()
        return self.connection

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
