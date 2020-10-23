# -*- coding: utf-8 -*-
"""State reprersents the state of a running job.

A runner can tell the job's current state, this class provides the info.

The state will be updated by the runner. It provides a finished status and current
state log information.

State ID values provided by dq0-main:
    * 0 - StateCreated
    * 1 - StatePrepared
    * 2 - StateRunning
    * 3 - StateFailed
    * 4 - StateStopped

Copyright 2020, Gradient Zero
All rights reserved
"""


class State:
    """A state for a running job (model or data)

    Provides methods to get the job's state and log message.

    Attributes:
        finished (bool): The state's finished flag.
            True if the run has finished.
        message (:obj:`str`): The last log message of the run.
        results (:obj:`dict`): The run's state once finished.

    """

    def __init__(self):
        self.finished = False
        self.message = ''
        self.run_id = ''
        self.progress = 0
        self.results = {}

    def update(self, response):
        """Updates the state representation"""
        self.message = response['job_state']
        self.results = response
        try:
            self.run_id = response['job_params'].split('=')[-1]
        except Exception:
            pass
        try:
            self.progress = int(response['job_progress'])
        except Exception:
            pass
        if self.progress == 1:
            self.finished = True
            # TODO: get Results via /runs/:run_id request
