# -*- coding: utf-8 -*-
"""Data Source for SAP Hana.

This source class provides access to SAP Hana data as pandas dataframes.

Based on sqlalchemy with sqlalchemy-hana driver extension: https://github.com/SAP/sqlalchemy-hana

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class SAPHana(SQL):
    """Data Source for SAP Hana data.

    Provides function to read in Snowflake data.

    SAP Hana connection string: 'hana://<user>:<password>@<host>:<port>/'

    Args:
        connection_string (:obj:`str`): The saphana connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'saphana'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute SAP SQL query

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
