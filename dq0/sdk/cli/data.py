# -*- coding: utf-8 -*-
"""Data allows for the execution of db stats jobs

A data object will be created at runtime from a project instance.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.cli.api import Client, routes
from dq0.sdk.cli.runner import QueryRunner
from dq0.sdk.cli.utils import is_valid_uuid
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse


class Data:
    """A data source wrapper

    Provides an interface for inspecting/interacting with data sources as well as query methods

    Args:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this data source belongs to

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this data source belongs to
        uuid (:obj:str): UUID of data source
        name (:obj:str): Name of data source
        type (:obj:str): Type of data source

    """

    def __init__(self, source, project=None):
        if source is None:
            raise ValueError('You need to provide the "source" argument. Can be either string (UUID/Name) or dict')
        self.source = source
        self.project = project
        self.where_clause = None
        self.client = Client()
        if isinstance(self.source, str):
            data = self._load_dataset()
        elif isinstance(self.source, dict):
            data = self.source
        else:
            raise ValueError("Please provide either UUID/Name of dataset or a dictionary of it")
        self.uuid = data.pop('data_uuid')
        self.name = data.pop('data_name', None)
        self.type = data.pop('data_type', None)
        self.description = data.pop('data_description', None)
        self.permissions = data.pop('data_permissions', None)
        self.privacy_masks = data.pop('privacy_masks', None)
        self.privacy_budget = data.pop('privacy_budget', None)
        self.privacy_thresholds = data.pop('privacy_thresholds', None)
        self.location = None
        self.size = 0
        # extract other dataset props
        self.__dict__.update(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def get_available_data_sources():
        """Returns a list of available data sources.

        The returned Data instances can be used for the attach_data_source method.

        Returns:
            A list of available data sources.
        """
        client = Client()
        response = client.get(routes.data.list)
        checkSDKResponse(response)
        return [Data(d) for d in response['items']]

    @staticmethod
    def get_data_info(data=None, data_uuid=None):
        """Returns info of a given data source.

        The returned dict contains information about the
        data source depending on the source's permissions set by
        the data owner.

        Args:
            data (:obj:`dq0.sdk.cli.Data`): Data instance of the requested data source
            data_uuid (:obj:`str`): optional; The UUID of the requested data source

        Returns:
            The data source information in JSON format
        """
        client = Client()
        if data and isinstance(data, Data):
            response = client.get(routes.data.get, uuid=data.uuid)
        elif data_uuid:
            response = client.get(routes.data.get, uuid=data_uuid)
        else:
            raise ValueError('Missing required parameter: data (Data instance) or data_uuid')
        checkSDKResponse(response)
        return response

    def as_dict(self):
        """Returns data source representation as dictionary"""
        return {
            'data_uuid': self.uuid,
            'data_name': self.name,
            'data_type': self.type,
            'description': self.description,
            'permissions': self.permissions,
            'privacy_masks': self.privacy_masks,
            'privacy_budget': self.privacy_budget,
            'privacy_thresholds': self.privacy_thresholds,
            'location': self.location,
            'size': self.size,
        }

    def refresh(self):
        """Reloads data source information from database. Useful when instantiating from incomplete dictionaries or when
        the data has changed"""
        if self.uuid:
            response = self.client.get(routes.data.info, uuid=self.uuid)
            checkSDKResponse(response)
            self.uuid = response.pop('data_uuid')
            self.name = response.pop('data_name')
            self.type = response.pop('data_type')
            self.description = response.pop('data_description')
            self.permissions = response.pop('data_permissions')
            self.privacy_masks = response.pop('privacy_masks', None)
            self.privacy_budget = response.pop('privacy_budget', None)
            self.privacy_thresholds = response.pop('privacy_thresholds', None)
            self.location = None
            self.size = 0
            # extract other dataset props
            self.__dict__.update(response)

    def _load_dataset(self):
        if is_valid_uuid(self.source):
            response = self.client.get(routes.data.info, uuid=self.source)
            checkSDKResponse(response)
            return response
        else:  # get dataset from data list if only data name provided
            response = self.client.get(routes.data.list)
            checkSDKResponse(response)
            items = response.get('items')
            if items:
                for data in items:
                    if data.get('data_name') == self.source:
                        return data
            raise DQ0SDKError(f'Dataset {self.source} not found. Please provide a valid UUID or name. Available '
                              f'datasets can be found by running the Data.get_available_data_sources() method')

    def where(self, *args):
        """Where filter. TBD."""
        self.where_clause = args
        return self

    def all(self, *args):
        """All reset filter."""
        self.where_clause = None
        return self

    def mean(self, cols=None):
        """Gets the differential private mean value of the given columns

        Args:
            cols: list of columns in the dataset to include. None for all available columns
        """
        # TODO
        pass

    def distribution(self, cols=None):
        """Gets the differential private mean value of the given columns

        Args:
            cols: list of columns in the dataset to include. None for all available columns
        """
        import os
        import time
        from IPython.display import Image

        time.sleep(2.5)

        path = os.environ['DQ0_DISTRI']
        if self.where_clause is not None:
            path = os.environ['DQ0_DISTRI_F']
        pil_img = Image(filename=path)

        display(pil_img)  # noqa: F821

    def query(self, query, epsilon=1.0, tau=0.0, private_column='', permissions=None, params=None, project=None):
        """Run a query on this Data instance.

        Args:
            query: string containing SQL
            permissions: optional; e.g. 'households<75'
            params: optional; e.g. 'p1=123'
            epsilon: float; Epsilon value for differential private query. Default: 1.0
            tau: float; Tau threshold value for private query. Default: 0.0
            private_column: string; Private column for this query. Leave empty or omit for default value from metadata.
            project:`dq0.sdk.cli.project.Project` instance.
        Returns:
            :obj:`dq0.sdk.cli.runner.QueryRunner` instance
        """
        if self.project is None and project is None:
            raise DQ0SDKError('queries need to be executed in a project context, and no project was assigned. '
                              'you can pass the project parameter to set the project context for this query.')

        if project is None:
            project = self.project

        response = self.client.post(
            route=routes.query.create,
            data={'query': query,
                  'datasets_used': self.name,
                  'permissions': permissions,
                  'epsilon': epsilon,
                  'tau': tau,
                  'private_column': private_column,
                  'params': params,
                  'project_uuid': project.uuid
                  }
        )
        checkSDKResponse(response)
        query_uuid = response.get('job_uuid')
        if not query_uuid:
            raise DQ0SDKError('Did not receive job UUID in CLI server response')
        return QueryRunner(project, query_uuid)
