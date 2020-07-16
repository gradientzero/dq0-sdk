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
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The saphana connection string.
    """
    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'saphana'
        self.engine = sqlalchemy.create_engine(connection)

    def read(self, **kwargs):
        """Read saphana data source

        Args:
            kwargs: keyword arguments

        Returns:
            saphana data as pandas dataframe
        """
        connection = self.engine.connect()
        return pd.read_sql_query(self.query, connection, **kwargs)
