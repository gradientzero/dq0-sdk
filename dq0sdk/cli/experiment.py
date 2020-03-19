# -*- coding: utf-8 -*-
"""Experiment allows for the execution of training and preprocessing jobs

An experiment will be created at runtime. It has a project and a name.

Calling train or preprocess through the experiment will return
a Runner instance that can be used to further control the job

Experiment wraps the following CLI commands:
    * dq0 model train
    * dq0 data preprocess

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.cli.api import routes
from dq0sdk.cli.runner import DataRunner, ModelRunner
from dq0sdk.errors import DQ0SDKError


class Experiment:
    """An experiment

    Provides methods to train models and preprocess datasets.

    Example:
        # Create an experiment
        experiment = Experiment(project=project, name='experiment_1')

        # call train
        run = experiment.train()

        # call preprocess
        run = experiment.preprocess()

    Args:
        project (:obj:`dq0sdk.cli.api.Project`): The project
            this experiment belongs to
        name (str): The name of the new experiment
    """
    def __init__(self, project=None, name=None):
        if project is None:
            raise ValueError('You need to provide the "project" argument')
        if name is None:
            raise ValueError('You need to set the "name" argument')
        self.project = project
        self.name = name

    def get_last_model_run(self):
        """Returns the latest ModelRunner.

        Can be used to cancel zombie jobs for example.
        """
        return ModelRunner(self.project)

    def get_last_data_run(self):
        """Returns the latest DataRunner.

        Can be used to cancel zombie jobs for example.
        """
        return DataRunner(self.project)

    def train(self):
        """Starts a training run

        It calls the CLI command `model train` and returns
        a Runner instance to watch to job
        """
        response = self.project._deploy()
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])

        response = self.project.client.post(routes.model.train, id=self.project.model_uuid)
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
        print(response['message'])
        return ModelRunner(self.project)

    def preprocess(self):
        """Starts a preprocessing run

        It calls the CLI command `data preprocess` and returns
        a Runner instance to watch to job
        """
        response = self.project._deploy()
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])

        response = self.project.post(routes.data.preprocess, id=self.project.data_source_uuid)
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
        print(response['message'])
        return DataRunner(self.project)
