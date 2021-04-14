# -*- coding: utf-8 -*-
"""Query allows for the execution of db stats jobs

A query object will be created at runtime from a project instance.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.cli import Project
from dq0.sdk.cli.api import Client, routes
from dq0.sdk.cli.data import Data
from dq0.sdk.cli.runner import QueryRunner
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse


class Query:
    """A query source wrapper

    Provides methods to run query jobs. A query always needs to be run in a project context.
    Alternative to using the query method directly from a Data instance.
    Allows for querying multiple data sources.

    Args:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this query belongs to

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this query belongs to

    """

    def __init__(self, project):
        if project is None or not isinstance(project, Project):
            raise DQ0SDKError('Please provide a valid project: object of type dq0.sdk.cli.project.Project')
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

    def execute(self, query, epsilon=1.0, tau=0.0, private_column='', permissions=None, params=None):
        """Run a query on the data sources defined by this Query instance.

        Args:
            query: string containing SQL
            epsilon: float; Epsilon value for differential private query. Default: 1.0
            tau: float; Tau threshold value for private query. Default: 0.0
            private_column: string; Private column for this query. Leave empty or omit for default value from metadata.
            permissions: optional; e.g. 'households<75'
            params: optional; e.g. 'p1=123'
        Returns:
            :obj:`dq0.sdk.cli.runner.QueryRunner` instance
        """
        if not self.datasets_used:
            raise DQ0SDKError('Please specify which datasets to use for query')
        response = self.client.post(
            route=routes.query.create,
            data={'query': query,
                  'datasets': self.get_dataset_names(),
                  'epsilon': epsilon,
                  'tau': tau,
                  'private_column': private_column,
                  'permissions': permissions,
                  'params': params,
                  'project_uuid': self.project.project_uuid
                  }
        )
        checkSDKResponse(response)
        query_uuid = response.get('job_uuid')
        if not query_uuid:
            raise DQ0SDKError('Did not receive job UUID in CLI server response')
        return QueryRunner(self.project, query_uuid)