# -*- coding: utf-8 -*-
"""Data Source for Apache Drill.

This source class provides access to data reveived via Apache Drill as pandas dataframes.

Based on sqlalchemy with drill driver extension: https://github.com/JohnOmernik/sqlalchemy-drill

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Drill(SQL):
    """Data Source for Apache Drill data.

    Provides function to read in drill data.

    Drill connection string: 'drill+sadrill://<username>:<password>@<host>:<port>/<storage_plugin>?use_ssl=True'

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The drill connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'drill'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read drill data source

        Args:
            kwargs: keyword arguments

        Returns:
            drill data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
