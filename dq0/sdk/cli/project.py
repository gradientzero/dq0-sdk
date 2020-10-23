# -*- coding: utf-8 -*-
"""Project represents a user project

This class provides methods to create and manage a user project
comprising of user_model and user_source code.

Project reads and writes the .meta file in the current project directory.

Project wraps the following CLI commands:
    * dq0 project info
    * dq0 project create [NAME]
    * dq0 project deploy
    * dq0 data list
    * dq0 data attach

Copyright 2020, Gradient Zero
All rights reserved
"""

import inspect
import json
import os

from dq0.sdk.cli import Model
from dq0.sdk.cli.api import Client, routes
from dq0.sdk.cli.utils.code import (
    add_function,
    check_signature,
    replace_function,
    replace_model_parent_class,
)
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse

import yaml


class Project:
    """A user project

    Provides methods to create and manage a user project
    comprising of user_model and user_source code.

    Example:
        >>> # Create a new project
        >>> project = Project(name='some name') # doctest: +SKIP

        >>> # Load a project (cd into project dir first)
        >>> project = Project.load() # doctest: +SKIP

    Args:
        name (:obj:`str`): The name of the new project
        create (bool): True to create a new project via DQ0 CLI.
            Default is True.

    Attributes:
        name (:obj:`str`): The name of the project
        project_uuid (:obj:`str`): The universally unique identifier of
            the project
        data_source_uuid (:obj:`str`): The universally unique identifier of
            the project's currently attached data source
        version (:obj:`str`): A version number of the project.

    """

    def __init__(self, name=None, create=True):
        if name is None:
            raise ValueError('You need to set the "name" argument')
        self.name = name
        self.commit_uuid = ''
        self.datasets = []
        self.experiment_name = ''

        # create API client instance
        self.client = Client()

        if create:
            self._create_new(name)

    @staticmethod
    def load():
        """Load loads an existing project.

        Load is a static function to create a new model instance from an
        existing local project.

        It reads the .meta file of the current directory to collect all
        neccessary project information.

        Returns:
            New instance of the Project class for the loaded project

        Raises:
            FileNotFoundError: if the .meta project file was not found in
                the current directory.
        """
        # check if .meta file exists in current directory
        if not os.path.isfile('.meta'):
            raise FileNotFoundError('Could not find .meta project file '
                                    'in current directory')

        with open('.meta') as f:
            meta = yaml.load(f, Loader=yaml.FullLoader)

        project = Project(name=meta['project_name'], create=False)
        project.project_uuid = meta['project_uuid']
        project.commit_uuid = meta['commit_uuid']
        project.experiment_name = meta['experiment_name']
        project.datasets = meta['datasets']

        return project

    def _create_new(self, name):
        """Creates a new project.

        First, calls the API to create a new project with the given name.
        Then sets the UUID property read from the new .meta file.

        Note:
            This function will change to the new project directory.

        Args:
            name (:obj:`str`): The name of the new project
        """
        working_dir = os.getcwd()
        response = self.client.post(routes.project.create, data={'working_dir': working_dir, 'name': name})
        checkSDKResponse(response)
        print(response['message'])

        # change to working directory where the new project was created
        os.chdir(working_dir)

        with open('{}/.meta'.format(name)) as f:
            meta = yaml.load(f, Loader=yaml.FullLoader)
        self.project_uuid = meta['project_uuid']

        # change the working directory to the new project
        os.chdir(name)

    def info(self):
        """Info returns information about the project.

        It calls the CLI command `project info` and returns
        the results as JSON.

        Returns:
            Project info in JSON format
        """
        return self.client.get(routes.project.info, uuid=self.project_uuid)

    def get_latest_model(self):
        """Returns the currently active model of this project.

        Returns:
            The currently active model of this project.
        """
        return Model(project=self)

    def get_available_data_sources(self):
        """Returns a list of available data sources.

        The returned UUIDs can be used for the attach_data_source method.

        Returns:
            A list of available data sources.
        """
        response = self.client.get(routes.data.list)
        checkSDKResponse(response)
        return response['items']

    def get_data_info(self, data_uuid):
        """Returns info of a given data source.

        The returned dict contains information about the
        data source depending on the source's permissions set by
        the data owner.

        Args:
            data_uuid (:obj:`str`): The UUID of the requested data source

        Returns:
            The data source information in JSON format
        """
        response = self.client.get(routes.data.get, uuid=data_uuid)
        checkSDKResponse(response)
        return response

    def get_sample_data(self, data_uuid):
        """Returns sample data for a given data source.

        Sample data is provided manually and is not available
        for every data source.

        Args:
            data_uuid (:obj:`str`): The UUID of the requested data source

        Returns:
            The data source sample data
        """
        response = self.client.get(routes.data.sample, uuid=data_uuid)
        checkSDKResponse(response)
        if 'sample' in response:
            try:
                response = json.loads(response['sample'])
            except Exception:
                pass
        return response

    def attach_data_source(self, data_source_uuid, data_name):
        """Attaches a new data source to the project.

        Args:
            data_source_uuid (:obj:`str`): The UUID of the new source to attach
            data_name (:obj:`str`): The name of the new source to attach
        """
        response = self.client.post(
            routes.project.attach,
            uuid=self.project_uuid,
            data={'data_uuid': data_source_uuid, 'data_name': data_name})
        checkSDKResponse(response)
        print(response['message'])

    def _deploy(self):
        """Deploys the project to DQ0

        This is called before every train, predict, or preprocess call.

        Returns:
            The API response in JSON format
        """
        return self.client.post(routes.project.deploy, uuid=self.project_uuid)

    def update_commit_uuid(self, message):
        """Updates the latest commit uuid from the given response message.

        Args:
            message (:obj:`str`): The response message after deploy.
        """
        try:
            self.commit_uuid = message.split(' ')[-1]
        except Exception:
            raise DQ0SDKError('Could not parse new commit uuid')

    def set_connection(self, host='localhost', port=9000):
        """Updates the connection string for the API communication.

        Passes the updated info to the API handler.

        Args:
            host (:obj:`str`): The host of the DQ0 CLI API Server
            port (int): The port of the DQ0 CLI API Server
        """
        self.client.set_connection(host=host, port=port)

    def set_model_code(self,  # noqa: C901
                       setup_data=None,
                       setup_model=None,
                       preprocess=None,
                       parent_class_name=None):
        """Sets the user defined setup_model and setup_data functions.

        Saves the function code to user_model.py

        Note:
            This function will only work inside iphyton notebooks,
            otherwise the sources of the function arguments are not available.

        Args:
            setup_data (func, optional): user defined setup_data function
            setup_model (func, optional): user defined setup_model function
            preprocess (func, optional): user defined preprocess function
            parent_class_name (:obj:`str`, optional): name of the parent class for UserModel
        """
        # check args
        setup_data_code = None
        setup_model_code = None
        preprocess_code = None
        try:
            if setup_data is not None:
                setup_data_code = inspect.getsource(setup_data)
            if setup_model is not None:
                setup_model_code = inspect.getsource(setup_model)
            if preprocess is not None:
                preprocess_code = inspect.getsource(preprocess)
        except OSError:
            raise DQ0SDKError('Could not get sources. '
                              'This will only work inside iphyton notebooks.')
        if setup_data_code is None and setup_model_code is None and preprocess_code is None:
            raise ValueError('You need to either pass setup_data, '
                             'setup_model or preprocess function')

        setup_data_code = check_signature(setup_data_code, 'setup_data')
        setup_model_code = check_signature(setup_model_code, 'setup_model')
        preprocess_code = check_signature(preprocess_code, 'preprocess')
        if setup_data_code is None and setup_model_code is None and preprocess_code is None:
            return

        # replace in my_model.py
        with open('my_model.py', 'r') as f:
            lines = f.readlines()
        if setup_data_code is not None:
            lines = replace_function(lines, setup_data_code)
        if setup_model_code is not None:
            lines = replace_function(lines, setup_model_code)
        if preprocess_code is not None:
            add_preprocess = True
            try:
                '\n'.join(lines).index('def preprocess(')
                add_preprocess = False
            except ValueError:
                lines = add_function(lines, preprocess_code)
            if not add_preprocess:
                lines = replace_function(lines, preprocess_code)
        if parent_class_name is not None:
            allowed_class_names = [
                'Model',
                'NeuralNetwork',
                'NeuralNetworkClassification',
                'NeuralNetworkRegression',
                'NeuralNetworkYaml'
            ]
            if parent_class_name not in allowed_class_names:
                raise DQ0SDKError('DQ0SDK only allows one of {}'
                                  ' as parent_class_name!'.format(allowed_class_names))
            lines = replace_model_parent_class(lines, parent_class_name)
        with open('my_model.py', 'w') as f:
            f.writelines(lines)

        print('Successfully set model code.')
