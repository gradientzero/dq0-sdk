# -*- coding: utf-8 -*-
"""Data Source for Big Query.

This source class provides access to data from Google BigQuery as pandas dataframes.

The BigQuery adapter assumes the authentication is managed in the runtime environment!

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.sql.sql import SQL

try:
    from google.cloud import bigquery
    big_query_available = True
except ImportError:
    big_query_available = False


class BigQuery(SQL):
    """Data Source for BigQuery data.

    Provides function to read in BigQuery data.

    Args:
        connection_string (:obj:`str`): The BigQuery project.
    """

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.type = 'bigquery'

    def execute(self, query, **kwargs):
        """Execute SQL query

        Args:
            query: SQL Query to execute
            kwargs: keyword arguments

        Returns:
            SQL ResultSet as pandas dataframe
        """
        # check query
        if query is None:
            raise ValueError('you need to pass a query parameter')

        # Construct a BigQuery client object.
        if not big_query_available:
            raise ImportError('big_query dependencies must be installed first')

        self.client = bigquery.Client()

        # make an API request
        query_job = self.client.query(query)

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
