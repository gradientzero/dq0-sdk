# -*- coding: utf-8 -*-
"""Data Source for Big Query.

This source class provides access to data from Google BigQuery as pandas dataframes.

The BigQuery adapter assumes the authentication is managed in the runtime environment!

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

from google.cloud import bigquery

import pandas as pd


class BigQuery(SQL):
    """Data Source for BigQuery data.

    Provides function to read in BigQuery data.

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): The BigQuery project.
    """

    def __init__(self, query, connection):
        super().__init__(query, connection)
        self.type = 'bigquery'

    def execute(self, query=None, **kwargs):
        """Execute SQL query

        Args:
            query: SQL Query to execute
            kwargs: keyword arguments

        Returns:
            SQL ResultSet as pandas dataframe
        """
        # Construct a BigQuery client object.
        self.client = bigquery.Client()

        # make an API request
        query_job = self.client.query(self.query)

        # waits for query to complete
        query_job.result()

        # get the destination table for the query results
        destination = query_job.destination

        # Get the schema (and other properties) for the destination table.
        destination = self.client.get_table(destination)

        # details: https://github.com/googleapis/python-bigquery/blob/35627d145a41d57768f19d4392ef235928e00f72/google/cloud/bigquery/client.py
        rows = self.client.list_rows(
            destination,
            selected_fields=None,
            max_results=None,
            page_token=None,
            start_index=None,
            page_size=None,
        )

        # either create temporary table or return result set as dataframe
        df = rows.to_dataframe(create_bqstorage_client=False)

        # return pandas dataframe
        return df
