# -*- coding: utf-8 -*-
"""Data Source for Snowflake.

This source class provides access to data reveived Snowflake as pandas dataframes.

Based on sqlalchemy with snowflake-sqlalchemy driver extension: https://github.com/snowflakedb/snowflake-sqlalchemy

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Snowflake(SQL):
    """Data Source for Snowflake data.

    Provides function to read in Snowflake data.

    Snowflake connection string: 'snowflake://<user>:<password>@<account>/'

    Args:
        connection_string (:obj:`str`): The snowflake connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'snowflake'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute Snowflake query

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
