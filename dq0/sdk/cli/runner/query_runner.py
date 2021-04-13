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
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse


class QueryRunner(Runner):
    """A running query

    Provides methods to get job status, wait for completion or cancel job.

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
        return self._get_state(routes.job.state, self.query_uuid)

    def _get_state(self, route, uuid):
        """Gets the current state of the running model or data experiment.

        Helper function called by both DataRunner.get_state() and
        ModelRunner.get_state() with the appropiate route.

        Args:
            route (:obj:`str`): The API route for either data or model state
            uuid (int): The UUID of the project or data source for the API call

        Returns:
            The state in JSON format
        """
        response = self.project.client.get(route, uuid=uuid)
        checkSDKResponse(response)
        self.state.update(response)
        print(self.state.state)
        return self.state.state

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
        self.get_state()
        if not self.state.finished:
            return 'Query still running'
        if self.state.error:
            return self.state.error
        if len(self.state.job_uuid) < 1:
            raise DQ0SDKError('could net get run details, job_uuid not set')
        response = self.project.client.get(routes.artifacts.download, data={'run_uuid': self.state.job_uuid,
                                                                            'artifact_path': 'results.csv'})
        checkSDKResponse(response)
        result = response.get('data_string')
        if result:
            self.state.set_results(result)
            return result
        return response
