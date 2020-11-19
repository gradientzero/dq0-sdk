# -*- coding: utf-8 -*-
"""Query allows for the execution of db stats jobs

A query object will be created at runtime from a project instance.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.cli.api import Client, routes
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse
from dq0.sdk.cli.utils import is_valid_uuid
from dq0.sdk.cli.runner import QueryRunner
from dq0.sdk.cli.data import Data


class Query:
    """A query source wrapper

    Provides methods to run query jobs. Alternative to using the query method directly from a Data instance.
    Allows for querying multiple data sources.

    Example:
        >>>  # instantiate query
        >>>  query = Query(project) # doctest: +SKIP
        >>>
        >>>  # get datasets
        >>>  data1 = Data('data_name1')
        >>>  data2 = Data('data_name2')
        >>>
        >>>  # execute query asynchronously. Data source names must be defined as SQL aliases
        >>>  # e.g. SELECT [data_source_name_1].[table_name1].*, [data_source_name_2].[table_name2]*
        >>>  # this returns a QueryRunner instance
        >>>  run = query.for_data([data1, data2]).execute('SELECT data_name1.table1.*') # doctest: +SKIP
        >>>  # optionally, wait for completion
        >>>  run.wait_for_completion()
        >>>  # check result
        >>>  result = run.get_results() # doctest: +SKIP

    Args:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this query belongs to

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this query belongs to

    """

    def __init__(self, project=None):
        self.project = project
        self.datasets_used = []
        self.client = Client()

    def for_data(self, data):
        """
        Specifiy which datasets are used in query.
        Args:
            data (:obj:`list`) list of :obj:`dq0.sdk.cli.Data` instances included in query. Alternatively, pass a single
            :obj:`dq0.sdk.cli.Data` instance.

        Returns:
            :obj:`dq0.sdk.cli.Query` instance with set datasets
        """
        if isinstance(data, Data):
            data = [data]
        elif not isinstance(data, list):
            raise DQ0SDKError('Please provide datasets either as list of Data objects or a single Data instance')
        self.datasets_used = data
        return self

    def get_dataset_names(self):
        """Returns used dataset names as a single comma-separated string"""
        return ','.join([dataset.name for dataset in self.datasets_used])

    def execute(self, query, permissions=None, params=None):
        """Run a query on the data sources defined by this Query instance.

        Args:
            query: string containing SQL
            permissions: optional; e.g. 'households<75'
            params: optional; e.g. 'p1=123'
        Returns:
            :obj:`dq0.sdk.cli.runner.QueryRunner` instance
        """
        if not self.datasets_used:
            return DQ0SDKError('Please specify which datasets to use for query')
        response = self.client.post(
            route=routes.query.create,
            data={'query': query,
                  'datasets_used': self.get_dataset_names(),
                  'permissions': permissions,
                  'params': params
                  }
        )
        checkSDKResponse(response)
        query_uuid = response.get('query_uuid')
        if not query_uuid:
            raise DQ0SDKError('Did not receive query in CLI server response')
        return QueryRunner(self.project, query_uuid)
