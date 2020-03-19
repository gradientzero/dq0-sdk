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
from dq0sdk.errors import DQ0SDKError


class Project:
    """A user project

    Provides methods to create and manage a user project
    comprising of user_model and user_source code.

    Example:
        # Create a new project
        project = Project(name='some name')

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
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
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
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
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
        if 'error' in response and response['error'] != "":
            raise DQ0SDKError(response['error'])
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

        Args:
            setup_data (func): user defined setup_data function
            setup_model (func): user defined setup_model function
            parent_class_name (str): name of the parent class for UserModel
        """
        # check args
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

        # check method signatures
        def _check_signature(code, name):
            if code is None:
                return None
            wrong_signature_error = 'Wrong function signature. '\
                                    'Should start with "def {}():" '\
                                    'or "def {}(self). '\
                                    '(Static function will be changed to '\
                                    'member function automatically.)"'\
                                    .format(name, name)
            try:
                def_start_index = code.index('def {}('.format(name))
                if def_start_index != 0:
                    raise DQ0SDKError('{}. {}'.format(name, wrong_signature_error))
                def_end_index = code.index(':')
                code = code.replace(code[:def_end_index], 'def {}(self)'.format(name))
            except ValueError:
                raise DQ0SDKError('{}. {}'.format(name, wrong_signature_error))
            return code

        setup_data_code = _check_signature(setup_data_code, 'setup_data')
        setup_model_code = _check_signature(setup_model_code, 'setup_model')
        if setup_data_code is None and setup_model_code is None:
            return

        # replace functions
        def _replace_function(lines, code):
            search = code[:code.index(':')]
            new_lines = []
            code_lines = code.split('\n')
            code_lines_index = 1  # skip signature
            in_function = False
            indent = -1
            for line in lines:
                if indent == -1:
                    try:
                        indent = line.index(search)
                        # if search was not found ValueError is thrown.
                        space_char = '\t' if line[:1] == '\t' else ' '
                        in_function = True
                        # use original function signature
                        new_lines.append(line)
                    except ValueError:
                        pass
                elif in_function:
                    len_indent = len(line) - len(line.lstrip())
                    if len(line) > 1 and len_indent == indent:
                        in_function = False
                    else:
                        # replace function
                        if code_lines_index < len(code_lines):
                            code_line = code_lines[code_lines_index]
                            num_code_spaces = len(code_line) - len(code_line.lstrip())
                            if space_char == '\t':
                                if code_line[:1] == ' ':
                                    num_code_spaces = int(num_code_spaces / 4)
                                num_code_spaces = num_code_spaces + 1
                            else:
                                num_code_spaces = num_code_spaces + 4
                            code_spaces = space_char.join(['' for i in range(num_code_spaces + 1)])
                            new_lines.append(code_spaces + code_line.lstrip() + '\n')
                            code_lines_index = code_lines_index + 1
                if not in_function:
                    # keep other code
                    new_lines.append(line)
            if len(new_lines) == 0 or code_lines_index == 1:
                raise DQ0SDKError('Function to replace not found in user_model.py')
            return new_lines

        def _replace_parent_class(lines, parent_class_name):
            new_lines = []
            for line in lines:
                try:
                    index = line.index('from dq0sdk.models')
                    if index == 0:
                        line = 'from dq0sdk.models.tf.neural_network import NeuralNetwork\n'
                except ValueError:
                    pass
                try:
                    line.index('class UserModel(')
                    line = 'class UserModel(NeuralNetwork):\n'
                except ValueError:
                    pass
                new_lines.append(line)
            return new_lines

        # replace in user_model.py
        with open('models/user_model.py', 'r') as f:
            lines = f.readlines()
        if setup_data_code is not None:
            lines = _replace_function(lines, setup_data_code)
        if setup_model_code is not None:
            lines = _replace_function(lines, setup_model_code)
        if parent_class_name is not None:
            if parent_class_name != 'NeuralNetwork':
                raise DQ0SDKError('Current version only allows "NeuralNetwork"'
                                  ' as parent_class_name!')
            lines = _replace_parent_class(lines, parent_class_name)
        with open('models/user_model.py', 'w') as f:
            f.writelines(lines)
