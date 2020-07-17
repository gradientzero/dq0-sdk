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
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The oracle connection string.
    """

    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'oracle'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read oracle data source

        Args:
            kwargs: keyword arguments

        Returns:
            oracle data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
