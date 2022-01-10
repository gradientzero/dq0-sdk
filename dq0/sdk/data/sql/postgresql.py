# -*- coding: utf-8 -*-
"""Data Source for PostgreSQL.

This source class provides access to data from PostgreSQL as pandas dataframes.

Based on sqlalchemy with psycopg2 driver.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas as pd

import sqlalchemy


class PostgreSQL(SQL):
    """Data Source for PostgreSQL data.

    Provides function to read in PostgreSQL data.

    PostgreSQL connection string: 'postgresql+psycopg2://user:password@/dbname'

    Args:
        connection_string (:obj:`str`): The postgresql connection string.
    """

    def __init__(self, meta_database):
        database = meta_database.data().name if isinstance(meta_database.data().name, str) else ''
        meta_connector = meta_database.connector()
        if meta_connector.type_name != 'postrgresql':
            raise Exception(f"type_name {meta_connector.type_name} does not match postgresql")
        host = meta_connector.host if isinstance(meta_connector.host, str) else ''
        password = meta_connector.password if isinstance(meta_connector.password, str) else ''
        port = f"{meta_connector.port}" if isinstance(meta_connector.port, int) else ''
        username = meta_connector.username if isinstance(meta_connector.username, str) else ''
        if len(username) == 0:
            password = ''
        if len(host) == 0:
            raise Exception("host not provided")
        password_sep = ':' if 0 < len(password) else ''
        user_sep = '@' if 0 < len(username) else ''
        port_sep = ':' if 0 < len(port) else ''
        database_sep = '/' if 0 < len(database) else ''
        connection_string = f"postgresql+psycopg2://{username}{password_sep}{password}{user_sep}{host}{port_sep}{port}{database_sep}{database}"
        super().__init__(connection_string)
        self.type = 'postgresql'
        self.engine = sqlalchemy.create_engine(connection_string)

    def execute(self, query, **kwargs):
        """Execute the Postgres query

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
