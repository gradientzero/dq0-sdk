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

import os

from dq0sdk.cli.api import Client


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

        if create:
            # create project
            # TODO: call API
            pass

        # create API client instance
        self.client = Client()

    def load():
        """Load loads an existing project.

        Load is a static function to create a new model instance from an
        existing local project.

        It reads the .meta file of the current directory to collect all
        neccessary project information.
        """
        # check if .meta file exists in current directory
        if not os.path.isfile('.meta'):
            raise FileNotFoundError('Could not find .meta project file'
                                    'in current directory')

        meta = {}  # TODO
        project = Project(name=meta.UUID, create=False)
        return project

    def info(self):
        """Info returns information about the project.

        It calls the CLI command `project info` and returns
        the results as JSON.
        """
        pass

    def set_connection(self, host='localhost', port=9000):
        """Updates the connection string for the API communication.

        Passes the updated info to the API handler.

        Args:
            host (str): The host of the DQ0 CLI API Server
            port (int): The port of the DQ0 CLI API Server
        """
        self.client.set_connection(host=host, port=port)
