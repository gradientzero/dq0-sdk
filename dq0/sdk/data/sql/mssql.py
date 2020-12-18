# -*- coding: utf-8 -*-
"""Data Source for MSSQL.

This source class provides access to data from MSSQL as pandas dataframes.

Based on sqlalchemy with pyodbc driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class MSSQL(SQL):
    """Data Source for MSSQL data.

    Provides function to read in MSSQL data.

    MSSQL connection string: 'mssql+pyodbc://<username>:<password>@<dsnname>'

    Args:
        connection_string (:obj:`str`): The mssql connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'mssql'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute MSSQL query

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
