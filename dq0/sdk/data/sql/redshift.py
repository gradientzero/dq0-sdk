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
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The redshift connection string.
    """

    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'redshift'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read redshift data source

        Args:
            kwargs: keyword arguments

        Returns:
            redshift data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
