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

from dq0.sdk.cli.api import routes
from dq0.sdk.cli import Data
from dq0.sdk.cli.runner import DataRunner, ModelRunner
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse


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
        project (:obj:`dq0.sdk.cli.Project`): The project
            this experiment belongs to
        name (:obj:`str`): The name of the new experiment

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
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
        self.datasets_used = None

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

    def get_dataset_uuids(self, datasets=None):
        """Returns used dataset uuids as a single comma-separated string"""
        if not datasets:
            datasets = self.datasets_used

        data_uuids = []
        for dataset in datasets:
            if isinstance(dataset, Data):
                data_uuids.append(dataset.uuid)
            elif type(dataset) == str:
                data_uuids.append(dataset)

        return ','.join(data_uuids)

    def run(self, args, datasets=None):
        """Starts a training run

        It calls the CLI command `model train` and returns
        a Runner instance to watch to job

        Returns:
            A new instance of the ModelRunner class for the train run.
        """
        if not isinstance(args, dict):
            raise TypeError('args need to passed as a dict')

        response = self.project._deploy()
        checkSDKResponse(response)
        self.project.update_commit_uuid(response['message'])

        data_uuids = self.get_dataset_uuids(datasets)

        if not data_uuids or not len(data_uuids):
            raise DQ0SDKError('No datasets provided. Please choose which datasets to use for this run using the'
                              'datasets parameter or the .for_data() method')

        data = {
            'project_uuid': self.project.project_uuid,
            'commit_uuid': self.project.commit_uuid,
            'experiment_name': self.name,
            'args': args,
            'datasets': data_uuids
        }

        response = self.project.client.post(routes.runs.create, data=data)
        checkSDKResponse(response)
        print(response)
        try:
            job_uuid = response['message'].split(' ')[-1]
        except Exception:
            raise DQ0SDKError('Could not parse new commit uuid')
        return ModelRunner(self.project, job_uuid)

    def for_data(self, data):
        """
        Specifiy which datasets are used in query.
        Args:
            data (:obj:`list`) list of :obj:`dq0.sdk.cli.Data` instances included in query. Alternatively, pass a single
            :obj:`dq0.sdk.cli.Data` instance.

        Returns:
            :obj:`dq0.sdk.cli.Query` instance with set datasets
        """
        if isinstance(data, Data):
            data = [data]
        elif not isinstance(data, list):
            raise DQ0SDKError('Please provide datasets either as list of Data objects or a single Data instance')
        self.datasets_used = data
        return self

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
        print(response)
        return DataRunner(self.project)
