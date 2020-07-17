# -*- coding: utf-8 -*-
"""Data Source for Big Query.

This source class provides access to data from Google BigQuery as pandas dataframes.

The BigQuery adapter assumes the authentication is managed in the runtime environment!

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

import pandas_gbq


class BigQuery(SQL):
    """Data Source for BigQuery data.

    Provides function to read in BigQuery data.

    Args:
        query (:obj:`str`): SQL query.
        project_id (:obj:`str`): The BigQuery project.
    """

    def __init__(self, query, project_id):
        super().__init__(query, project_id)
        self.type = 'bigquery'

    def read(self, **kwargs):
        """Read BigQuery data sources

        Args:
            kwargs: keyword arguments

        Returns:
            BigQuery data as pandas dataframe
        """
        return pandas_gbq.read_gbq(self.query, project_id=self.connection, **kwargs)
