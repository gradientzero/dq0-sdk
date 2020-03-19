# -*- coding: utf-8 -*-
"""Model allows for the execution of prediction jobs

A model will be created at runtime. It belongs to a project.

Calling predict through Model will return a ModelRunner instance
that can be used to further control the job

Model wraps the following CLI commands:
    * dq0 model predict

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.cli.api import routes
from dq0sdk.cli.runner import ModelRunner
from dq0sdk.errors import DQ0SDKError


class Model:
    """A model predict wrapper

    Provides methods to call model predict

    Example:
        # get the latest model
        model = project.get_latest_model()

        # check DQ0 privacy clearing
        if model.predict_allowed:

            # call predict
            run = model.predict(np.array([1, 2, 3]))

            # wait for completion
            run.wait_for_completion(verbose=True)

            # get training results
            print(run.get_results())

    Args:
        project (:obj:`dq0sdk.cli.api.Project`): The project
            this experiment belongs to
    """
    def __init__(self, project=None):
        if project is None:
            raise ValueError('You need to provide the "project" argument')
        self.project = project

    def predict(self):
        """Starts a prediction run

        It calls the CLI command `model predict` and returns
        a Runner instance to watch to job
        """
        response = self.project._deploy()
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])

        response = self.project.client.post(routes.model.predict, id=self.project.model_uuid)
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
        print(response['message'])
        return ModelRunner(self.project)
