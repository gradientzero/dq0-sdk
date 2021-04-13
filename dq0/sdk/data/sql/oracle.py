# -*- coding: utf-8 -*-
"""Data Source for Oracle DB.

This source class provides access to data from Oracle DB as pandas dataframes.

Based on sqlalchemy with Oracle-CX driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Oracle(SQL):
    """Data Source for Oracle data.

    Provides function to read in Oracle data.

    Oracle connection string: 'oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]'

    Args:
        connection_string (:obj:`str`): The oracle connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'oracle'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute Oracle SQL query

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
