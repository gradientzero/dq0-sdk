# -*- coding: utf-8 -*-
"""State reprersents the state of a running job.

A runner can tell the job's current state, this class provides the info.

The state will be updated by the runner. It provides a finished status and current
state log information.

Copyright 2020, Gradient Zero
All rights reserved
"""


class State:
    """A state for a running job (experiment or model)

    Provides methods to get the job state and log message.
    """
    def __init__(self):
        self.finished = False
        self.message = ''

    def update(self, new_state):
        """Updates the state representation"""
        self.message = new_state
        try:
            new_state.lower().index('state: finished')
            self.finished = True
        except ValueError:
            pass
