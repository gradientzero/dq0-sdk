# -*- coding: utf-8 -*-
"""Data Runner manages a running data experiment.

When starting an experiment with experiment.preprocess()
a new DataRunner instance is returned.

Runner can tell the job's current state, it can wait for the job to complete, or
it can (forcefully) cancel the job.

DataRunner wraps the following CLI commands:
    * dq0 data state
    * dq0 data cancel

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.cli.api import routes
from dq0sdk.cli.runner.runner import Runner


class DataRunner(Runner):
    """A running data experiment

    Provides methods to get job status, wait for completion or cancel job.

    Example:
        # call preprocess
        run = experiment.preprocess()

        # get status
        print(run.get_state())

        # wait for completion
        run.wait_for_completion(verbose=True)

        # or cancel
        run.cancel()

    Args:
        project (:obj:`dq0sdk.cli.api.Project`): The project
            this runner belongs to
    """
    def __init__(self, project):
        super().__init__(project)

    def get_state(self):
        """Gets the current state of the running data experiment."""
        return super()._get_state(routes.data.state, self.project.data_source_uuid)

    def cancel(self, force=False):
        """Cancels the experiment run"""
        return super()._cancel(routes.data.cancel, self.project.data_source_uuid)