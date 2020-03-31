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
        >>> # call preprocess
        >>> run = experiment.preprocess() # doctest: +SKIP
        >>>
        >>> # get status
        >>> print(run.get_state()) # doctest: +SKIP
        >>>
        >>> # wait for completion
        >>> run.wait_for_completion(verbose=True) # doctest: +SKIP
        >>>
        >>> # or cancel
        >>> run.cancel() # doctest: +SKIP

    Args:
        project (:obj:`dq0sdk.cli.Project`): The project
            this runner belongs to

    """
    def __init__(self, project):
        super().__init__(project)

    def get_state(self):
        """Gets the current state of the running data experiment.

        Returns:
            The state in JSON format
        """
        return super()._get_state(routes.data.state, self.project.data_source_uuid)

    def cancel(self, force=False):
        """Cancels the data run.

        Args:
            force (bool, optional): Set to true to force the job to be
                interrupted. Default is false where the job gracefully
                gets signalled to halt.
        """
        super()._cancel(routes.data.cancel, self.project.data_source_uuid)
