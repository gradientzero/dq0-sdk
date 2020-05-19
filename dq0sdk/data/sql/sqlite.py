# -*- coding: utf-8 -*-
"""Data Source for SQLite.

This source class provides access to data from SQLite as pandas dataframes.

Based on sqlalchemy with standard sqlite driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class SQLite(SQL):
    """Data Source for SQLite data.

    Provides function to read in SQLite data.

    SQLite connection string: 'sqlite:///path/to/database.db'

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The sqlite connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'sqlite'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read sqlite data sources

        Args:
            kwargs: keyword arguments

        Returns:
            sqlite data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
