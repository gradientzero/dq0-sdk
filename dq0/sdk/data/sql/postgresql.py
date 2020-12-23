# -*- coding: utf-8 -*-
"""Data Source for PostgreSQL.

This source class provides access to data from PostgreSQL as pandas dataframes.

Based on sqlalchemy with psycopg2 driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class PostgreSQL(SQL):
    """Data Source for PostgreSQL data.

    Provides function to read in PostgreSQL data.

    PostgreSQL connection string: 'postgresql+psycopg2://user:password@/dbname'

    Args:
        connection_string (:obj:`str`): The postgresql connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'postgresql'
        try:
            connection_string.index('postgresql+psycopg2://')
        except ValueError:
            connection_string = 'postgresql+psycopg2://{}'.format(connection_string)
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute the Postgres query

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
