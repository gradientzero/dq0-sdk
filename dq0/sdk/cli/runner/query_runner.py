# -*- coding: utf-8 -*-
"""Query Runner manages a running queries.

When starting an query with Data.query() or Query.execute()
a new QueryRunner instance is returned.

Runner can tell the job's current state, it can wait for the job to complete, or
it can (forcefully) cancel the job.

QueryRunner wraps the following CLI commands:
    * dq0 query state
    * dq0 query cancel

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.cli.api import routes
from dq0.sdk.cli.runner.runner import Runner
from dq0.sdk.errors import checkSDKResponse


class QueryRunner(Runner):
    """A running query

    Provides methods to get job status, wait for completion or cancel job.

    Example:
        >>> # run query directly from a dataset
        >>> run = data.query('SELECT * FROM db') # doctest: +SKIP
        >>> # or over a query instance, allowing for queries across multiple data sources
        >>> query = Query(project)
        >>> run = query.for_data([data, data2]).execute('SELECT a.* FROM data.table a')
        >>>
        >>> # get status
        >>> print(res.get_state()) # doctest: +SKIP
        >>>
        >>> # wait for completion
        >>> run.wait_for_completion(verbose=True) # doctest: +SKIP
        >>>
        >>> # or cancel
        >>> run.cancel() # doctest: +SKIP

    Args:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this runner belongs to

    """

    def __init__(self, project, query_uuid):
        super().__init__(project)
        self.query_uuid = query_uuid

    def get_state(self):
        """Gets the current state of the running query.

        Returns:
            The state in JSON format
        """
        return super()._get_state(routes.job.state, self.query_uuid)

    def cancel(self, force=False):
        """Cancels the running query.

        Args:
            force (bool, optional): Set to true to force the job to be
                interrupted. Default is false where the job gracefully
                gets signalled to halt.
        """
        super()._cancel(routes.query.cancel, self.project.query_uuid)

    def _get_run_results(self):
        """Helper function to get query details after the job is completed"""
        response = self.project.client.get(routes.query.info, uuid=self.query_uuid)
        checkSDKResponse(response)
        self.state.set_results(response)
