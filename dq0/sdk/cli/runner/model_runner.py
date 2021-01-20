# -*- coding: utf-8 -*-
"""Model Runner manages a running model experiment.

When starting an experiment with experiment.train() or model.predict()
a new ModelRunner instance is returned.

Runner can tell the job's current state, it can wait for the job to complete, or
it can (forcefully) cancel the job.

ModelRunner wraps the following CLI commands:
    * dq0 model state
    * dq0 model cancel

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.cli.api import routes
from dq0.sdk.cli.model import Model
from dq0.sdk.cli.runner.runner import Runner


class ModelRunner(Runner):
    """A running model experiment

    Provides methods to get job status, wait for completion or cancel job.

    Example:
        >>> # call train
        >>> run = experiment.train() # doctest: +SKIP
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
        project (:obj:`dq0.sdk.cli.Project`): The project
            this runner belongs to

    """

    def __init__(self, project, job_uuid):
        super().__init__(project)
        self.job_uuid = job_uuid

    def get_state(self):
        """Gets the current state of the running model experiment.

        Returns:
            The state in JSON format
        """
        return super()._get_state(routes.job.state, self.job_uuid)

    def cancel(self, force=False):
        """Cancels the experiment run.

        Args:
            force (bool, optional): Set to true to force the job to be
                interrupted. Default is false where the job gracefully
                gets signalled to halt.
        """
        return super()._cancel(routes.job.cancel, self.job_uuid)

    def get_model(self):
        """Returns a model instance for the given run.

        Returns:
            The model instance
        """
        return Model(project=self.project, run_id=self.state.job_uuid)
