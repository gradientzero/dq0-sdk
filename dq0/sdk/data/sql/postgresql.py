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
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The postgresql connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'postgresql'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read postgresql data source

        Args:
            kwargs: keyword arguments

        Returns:
            postgresql data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
