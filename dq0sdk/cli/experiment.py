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
from dq0sdk.errors import checkSDKResponse


class Experiment:
    """An experiment

    Provides methods to train models and preprocess datasets.

    Note:
        There can be only one epxeriment for model and data each
        per project version. If you want to run mulitple experiments for one
        model in parallel use different project versions.

    Example:
        >>> # Create an experiment. Then call train and preprocess
        >>> experiment = Experiment(project=project, name='experiment_1') # doctest: +SKIP
        >>> run = experiment.train() # doctest: +SKIP
        >>> run = experiment.preprocess() # doctest: +SKIP

    Args:
        project (:obj:`dq0sdk.cli.Project`): The project
            this experiment belongs to
        name (:obj:`str`): The name of the new experiment

    Attributes:
        project (:obj:`dq0sdk.cli.Project`): The project
            this experiment belongs to
        name (:obj:`str`): The of the experiment

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

        Returns:
            A new instance of the ModelRunner class for the project.
        """
        return ModelRunner(self.project)

    def get_last_data_run(self):
        """Returns the latest DataRunner.

        Can be used to cancel zombie jobs for example.

        Returns:
            A new instance of the DataRunner class for the project.
        """
        return DataRunner(self.project)

    def train(self):
        """Starts a training run

        It calls the CLI command `model train` and returns
        a Runner instance to watch to job

        Returns:
            A new instance of the ModelRunner class for the train run.
        """
        response = self.project._deploy()
        checkSDKResponse(response)

        response = self.project.client.post(routes.model.train, uuid=self.project.project_uuid)
        checkSDKResponse(response)
        print(response['message'])
        return ModelRunner(self.project)

    def preprocess(self):
        """Starts a preprocessing run

        It calls the CLI command `data preprocess` and returns
        a Runner instance to watch to job.

        Returns:
            A new instance of the DataRunner class for the preprocess run.
        """
        response = self.project._deploy()
        checkSDKResponse(response)

        response = self.project.post(routes.data.preprocess, id=self.project.data_source_uuid)
        checkSDKResponse(response)
        print(response['message'])
        return DataRunner(self.project)
