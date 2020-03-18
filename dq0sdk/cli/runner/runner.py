# -*- coding: utf-8 -*-
"""Runner manages a running experiment.

When starting an experiment with experiment.train(), experiment.preprocess() or
model.predict() a new Runner instance is returned.

Runner can tell the job's current state, it can wait for the job to complete, or
it can (forcefully) cancel the job.

Runner wraps the following CLI commands:
    * dq0 model state
    * dq0 model cancel
    * dq0 data state
    * dq0 data state cancel

Copyright 2020, Gradient Zero
All rights reserved
"""

from abc import ABC, abstractmethod


class Runner(ABC):
    """A running experiment

    Provides methods to get job status, wait for completion or cancel job.

    Example:
        # call train
        run = experiment.train()

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
        if project is None:
            raise ValueError('You need to provide a valid project instance')
        self.project = project
        # self.state = State()

    @abstractmethod
    def get_state(self):
        """Gets the current state of the running model or data experiment."""
        pass

    @abstractmethod
    def get_results(self):
        """Gets the results of the running model or data experiment."""
        pass

    @abstractmethod
    def cancel(self, force=False):
        """Cancels the experiment run"""
        pass

    def wait_for_completion(self):
        """Loops until the state reflects the end of the run."""
        # while not self.state.finished
        pass
