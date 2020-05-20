# -*- coding: utf-8 -*-
"""Data Source for MSSQL.

This source class provides access to data from MSSQL as pandas dataframes.

Based on sqlalchemy with pyodbc driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class MSSQL(SQL):
    """Data Source for MSSQL data.

    Provides function to read in MSSQL data.

    MSSQL connection string: 'mssql+pyodbc://<username>:<password>@<dsnname>'

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The mssql connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'mssql'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read mssql data source

        Args:
            kwargs: keyword arguments

        Returns:
            mssql data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
