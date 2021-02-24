# -*- coding: utf-8 -*-
"""Data Source for Amazon Redshift.

This source class provides access to Amazon Redshift data as pandas dataframes.

Based on sqlalchemy with sqlalchemy-redshift (psycopg2) driver extension: https://github.com/SAP/sqlalchemy-hana

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class Redshift(SQL):
    """Data Source for Amazon Redshift data.

    Provides function to read in Amazon Redshift data.

    Amazon Redshift connection string: 'redshift+psycopg2://username@host.amazonaws.com:5439/database'

    Args:
        connection_string (:obj:`str`): The redshift connection string.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'redshift'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute Redshift SQL query

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
