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

from dq0.sdk.cli.runner.state import State
from dq0.sdk.errors import checkSDKResponse


class Runner(ABC):
    """A running experiment

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

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this runner belongs to
        state (:obj:`dq0.sdk.cli.runner.State`) The runner's state

    """
    def __init__(self, project):
        if project is None:
            raise ValueError('You need to provide a valid project instance')
        self.project = project
        self.state = State()

    @abstractmethod
    def get_state(self):
        """Gets the current state of the running model or data experiment.

        Returns:
            The state in JSON format
        """
        pass

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
        return self.state.results

    def get_results(self):
        """Gets the results of the running model or data experiment.

        Returns:
            The final state in JSON format or an empty dict if the run
            has not finished yet.
        """
        if self.state.finished:
            return self.state.results
        return {}

    @abstractmethod
    def cancel(self, force=False):
        """Cancels the experiment run"""
        pass

    def _cancel(self, route, uuid):
        """Cancels the experiment run. Model or data.

        Args:
            force (bool, optional): Set to true to force the job to be
                interrupted. Default is false where the job gracefully
                gets signalled to halt.
        """
        response = self.project.client.post(route, uuid=uuid)
        checkSDKResponse(response)
        print(response['message'])

    def wait_for_completion(self, verbose=False):
        """Loops until the state reflects the end of the run.

        This function is blocking.

        Args:
            verbose (bool, optional): Set to true to see periodic state outputs.
                Default is false
        """
        if verbose:
            print('Waiting for job to complete...')
        while not self.state.finished:
            time.sleep(5.0)
            # refetch model or data job state
            self.get_state()
            if verbose:
                print(self.state.message)
        if verbose:
            print('Job completed.')
            print(self.state.message)
