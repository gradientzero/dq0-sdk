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

import json
import os

from dq0sdk.cli import Model
from dq0sdk.cli.api import Client, routes


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
            print(response['error'])
            return
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
            print(response['error'])
            return None
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
            print(response['error'])
            return
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
