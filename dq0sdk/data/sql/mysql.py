# -*- coding: utf-8 -*-
"""Data Source for MySQL.

This source class provides access to data from MySQL as pandas dataframes.

Based on sqlalchemy with mysqlconnector driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class MySQL(SQL):
    """Data Source for MySQL data.

    Provides function to read in MySQL data.

    MySQL connection string: 'mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>'

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The mysql connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'mysql'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read mysql data sources

        Args:
            kwargs: keyword arguments

        Returns:
            mysql data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
