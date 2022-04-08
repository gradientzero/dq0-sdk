# -*- coding: utf-8 -*-
"""Data Source for SQLite.

This source class provides access to data from SQLite as pandas dataframes.

Based on sqlalchemy with standard sqlite driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class SQLite(SQL):
    """Data Source for SQLite data.

    Provides function to read in SQLite data.

    SQLite connection string: 'sqlite:///path/to/database.db'

    Args:
        connection_string (:obj:`str`): The sqlite connection string.
    """

    def __init__(self, meta_database):
        meta_connector = meta_database.connector
        if meta_connector.type_name != 'sqlite':
            raise Exception(f"type_name {meta_connector.type_name} does not match sqlite")
        uri = meta_connector.uri if isinstance(meta_connector.uri, str) else ''
        connection_string = f"sqlite:///{uri}"
        super().__init__(connection_string)
        self.type = 'sqlite'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute SQL query

        Args:
            query: SQL Query to execute
            kwargs: keyword arguments

        Returns:
            SQL ResultSet as pandas dataframe
        """
        # check query
        if query is None:
            raise ValueError('you need to pass the query')

        connection = self.get_connection()
        return pd.read_sql_query(query, connection, **kwargs)
