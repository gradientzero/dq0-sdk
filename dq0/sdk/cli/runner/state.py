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
        progress (float): Progress.
    """

    def __init__(self):
        self.finished = False
        self.message = ''
        self.job_uuid = ''
        self.state = ''
        self.progress = 0
        self.results = None
        self.error = ''
        self.params = ''
        self._run_status = ''

    def update(self, response):
        """Updates the state representation"""
        self.message = response['job_state']
        try:
            self.job_uuid = response.get('job_uuid')
            self.state = response.get('job_state')
            self.progress = int(response.get('job_progress', 0))
            self.params = response.get('run_params')
            self._run_status = response.get('run_status')
            self.error = response.get('job_errors')

        except Exception as e:
            pass
        if self.progress == 1 or self.message == 'error' or self.message == 'finished':
            self.finished = True

    def set_results(self, results):
        """Update parsed run results"""
        self.results = results
