# -*- coding: utf-8 -*-
"""Data Source for Snowflake.

This source class provides access to data reveived Snowflake as pandas dataframes.

Based on sqlalchemy with snowflake-sqlalchemy driver extension: https://github.com/snowflakedb/snowflake-sqlalchemy

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Snowflake(SQL):
    """Data Source for Snowflake data.

    Provides function to read in Snowflake data.

    Snowflake connection string: 'snowflake://<user>:<password>@<account>/'

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The snowflake connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'snowflake'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read snowflake data source

        Args:
            kwargs: keyword arguments

        Returns:
            snowflake data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
