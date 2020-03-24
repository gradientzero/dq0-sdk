# -*- coding: utf-8 -*-
"""Project represents a user project

This class provides methods to create and manage a user project
comprising of user_model and user_source code.

Project reads and writes the .meta file in the current project directory.

Project wraps the following CLI commands:
    * dq0 project info
    * dq0 project create --name [NAME]
    * dq0 project deploy
    * dq0 data list
    * dq0 data attach

Copyright 2020, Gradient Zero
All rights reserved
"""

import inspect
import json
import os

from dq0sdk.cli import Model
from dq0sdk.cli.api import Client, routes
from dq0sdk.cli.utils.code import (
    check_signature,
    replace_data_parent_class,
    replace_function,
    replace_model_parent_class,
)
from dq0sdk.errors import DQ0SDKError, checkSDKResponse


class Project:
    """A user project

    Provides methods to create and manage a user project
    comprising of user_model and user_source code.

    Example:
        >>> # Create a new project
        >>> project = Project(name='some name')

        >>> # Load a project (cd into project dir first)
        >>> project = Project.load()

    Args:
        name (str): The name of the new project
    """
    def __init__(self, name=None, create=True):
        if name is None:
            raise ValueError('You need to set the "name" argument')
        self.name = name
        self.model_uuid = ''
        self.data_source_uuid = ''
        self.version = '1'

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
        """
        # check if .meta file exists in current directory
        if not os.path.isfile('.meta'):
            raise FileNotFoundError('Could not find .meta project file '
                                    'in current directory')

        with open('.meta') as f:
            meta = json.load(f)

        project = Project(name=meta['name'], create=False)
        project.model_uuid = meta['id']
        project.data_source_uuid = meta['data_source_uuid']
        project.version = meta['version']

        return project

    def _create_new(self, name):
        """Creates a new project.

        First, calls the API to creat a new project with the given name.
        Then sets the UUID property read from the new .meta file.

        Args:
            name (str): The name of the new project
        """
        response = self.client.post(routes.project.create, data={'name': name})
        checkSDKResponse(response)
        print(response['message'])

        with open('{}/.meta'.format(name)) as f:
            meta = json.load(f)
        self.model_uuid = meta['id']

        # change the working directory to the new project
        os.chdir(name)

    def info(self):
        """Info returns information about the project.

        It calls the CLI command `project info` and returns
        the results as JSON.
        """
        return self.client.get(routes.project.info, id=self.model_uuid)

    def get_latest_model(self):
        """Returns the currently active model of this project.

        Current implementation returns the project as is. Model management TBD.
        """
        return Model(project=self)

    def get_available_data_sources(self):
        """Returns a list of available data sources.

        The returned UUIDs can be used for the attach_data_source method.
        """
        response = self.client.get(routes.data.list)
        checkSDKResponse(response)
        return response['results']

    def attach_data_source(self, data_source_uuid):
        """Attaches a new data source to the project.

        Args:
            data_source (str) The UUID of the new source to attach
        """
        response = self.client.post(
            routes.data.attach,
            id=self.model_uuid,
            data={'data_source_uuid': data_source_uuid})
        checkSDKResponse(response)
        print(response['message'])

    def _deploy(self):
        """Deploys the project to DQ0

        This is called before every train, predict, or preprocess call.
        """
        return self.client.post(routes.project.deploy, id=self.model_uuid)

    def set_connection(self, host='localhost', port=9000):
        """Updates the connection string for the API communication.

        Passes the updated info to the API handler.

        Args:
            host (str): The host of the DQ0 CLI API Server
            port (int): The port of the DQ0 CLI API Server
        """
        self.client.set_connection(host=host, port=port)

    def set_model_code(self, setup_data=None, setup_model=None, parent_class_name=None):  # noqa: C901
        """Sets the user defined setup_model and setup_data functions.

        Saves the function code to user_model.py

        Note: This function will only work inside iphyton notebooks,
        otherwise the sources of the function arguments are not available.

        Args:
            setup_data (func): user defined setup_data function
            setup_model (func): user defined setup_model function
            parent_class_name (str): name of the parent class for UserModel
        """
        # check args
        setup_data_code = None
        setup_model_code = None
        try:
            if setup_data is not None:
                setup_data_code = inspect.getsource(setup_data)
            if setup_model is not None:
                setup_model_code = inspect.getsource(setup_model)
        except OSError:
            raise DQ0SDKError('Could not get sources. '
                              'This will only work inside iphyton notebooks.')
        if setup_data_code is None and setup_model_code is None:
            raise ValueError('You need to either pass setup_data '
                             'or setup_model function')

        setup_data_code = check_signature(setup_data_code, 'setup_data')
        setup_model_code = check_signature(setup_model_code, 'setup_model')
        if setup_data_code is None and setup_model_code is None:
            return

        # replace in user_model.py
        with open('models/user_model.py', 'r') as f:
            lines = f.readlines()
        if setup_data_code is not None:
            lines = replace_function(lines, setup_data_code)
        if setup_model_code is not None:
            lines = replace_function(lines, setup_model_code)
        if parent_class_name is not None:
            if parent_class_name != 'NeuralNetwork':
                raise DQ0SDKError('Current version only allows "NeuralNetwork"'
                                  ' as parent_class_name!')
            lines = replace_model_parent_class(lines, parent_class_name)
        with open('models/user_model.py', 'w') as f:
            f.writelines(lines)

    def set_data_code(self, preprocess=None, parent_class_name=None):  # noqa: C901
        """Sets the user defined preprocess function.

        Saves the function code to user_source.py

        Note: This function will only work inside iphyton notebooks,
        otherwise the sources of the function arguments are not available.

        Args:
            preprocess (func): user defined preprocess function
            parent_class_name (str): name of the parent class for UserSource
        """
        # check args
        if preprocess is None:
            raise ValueError('You need to pass preprocess function')
        try:
            preprocess_code = inspect.getsource(preprocess)
        except OSError:
            raise DQ0SDKError('Could not get sources. '
                              'This will only work inside iphyton notebooks.')

        preprocess_code = check_signature(preprocess_code, 'preprocess')
        if preprocess_code is None:
            return

        # replace in user_source.py
        with open('data/user_source.py', 'r') as f:
            lines = f.readlines()
        lines = replace_function(lines, preprocess_code)
        if parent_class_name is not None:
            if parent_class_name != 'CSVSource':
                raise DQ0SDKError('Current version only allows "CSVSource"'
                                  ' as parent_class_name!')
            lines = replace_data_parent_class(lines, parent_class_name)
        with open('data/user_source.py', 'w') as f:
            f.writelines(lines)
