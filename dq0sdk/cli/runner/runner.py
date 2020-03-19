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
    * dq0 data cancel

Copyright 2020, Gradient Zero
All rights reserved
"""

import time
from abc import ABC, abstractmethod

from dq0sdk.cli.runner.state import State
from dq0sdk.errors import DQ0SDKError


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
        self.state = State()

    @abstractmethod
    def get_state(self):
        """Gets the current state of the running model or data experiment."""
        pass

    def _get_state(self, route, id):
        """Gets the current state of the running model or data experiment."""
        response = self.project.client.get(route, id=id)
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
        self.state.update(response['message'])
        return self.state.message

    def get_results(self):
        """Gets the results of the running model or data experiment."""
        if self.state.finished:
            return self.state.message
        return ''

    @abstractmethod
    def cancel(self, force=False):
        """Cancels the experiment run"""
        pass

    def _cancel(self, route, id):
        """Cancels the experiment run. Model or data."""
        response = self.project.client.post(route, id=id)
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
        print(response['message'])

    def wait_for_completion(self, verbose=False):
        """Loops until the state reflects the end of the run.

        This function is blocking in single-threaded contexts.
        """
        if verbose:
            print('Waiting for job to complete...')
        while not self.state.finished:
            time.sleep(3.0)
            # refetch model or data job state
            self.get_state()
            if verbose:
                print(self.state.message)
        if verbose:
            print('Job completed.')
            print(self.state.message)
