# -*- coding: utf-8 -*-
"""Data Source for MySQL.

This source class provides access to data from MySQL as pandas dataframes.

Based on sqlalchemy with mysqlconnector driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class MySQL(SQL):
    """Data Source for MySQL data.

    Provides function to read in MySQL data.

    MySQL connection string: 'mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>'

    Args:
        connection_string (:obj:`str`): The mysql connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'mysql'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute MYSQL query

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
