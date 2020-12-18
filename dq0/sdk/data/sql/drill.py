# -*- coding: utf-8 -*-
"""Data Source for Apache Drill.

This source class provides access to data reveived via Apache Drill as pandas dataframes.

Based on sqlalchemy with drill driver extension: https://github.com/JohnOmernik/sqlalchemy-drill

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Drill(SQL):
    """Data Source for Apache Drill data.

    Provides function to read in drill data.

    Drill connection string: 'drill+sadrill://<username>:<password>@<host>:<port>/<storage_plugin>?use_ssl=True'

    Args:
        connection_string (:obj:`str`): The drill connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'drill'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute drill query

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
