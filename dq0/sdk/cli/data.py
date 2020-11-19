# -*- coding: utf-8 -*-
"""Data allows for the execution of db stats jobs

A data object will be created at runtime from a project instance.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.cli.api import Client, routes
from dq0.sdk.errors import DQ0SDKError, checkSDKResponse
from dq0.sdk.cli.utils import is_valid_uuid
from dq0.sdk.cli.runner import QueryRunner


class Data:
    """A data source wrapper

    Provides methods to call data info jobs

    Example:
        >>> # get data source
        >>> data = project.get_available_data_sources()[0] # doctest: +SKIP
        >>>
        >>>  # call dp mean
        >>>  result = data.mean(cols=['age']) # doctest: +SKIP
        >>>
        >>>  # call with where clause
        >>>  result = data.mean(cols=['age'], query="where age > 30 and age < 40") # doctest: +SKIP

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
        self.name = data.pop('data_name')
        self.type = data.pop('data_type')
        # extract other dataset props
        self.__dict__.update(data)

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
                              f'datasets can be found by running the Project.get_available_data_sources() method')

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

    def query(self, query, permissions=None, params=None):
        """Run a query on this Data instance.

        Args:
            query: string containing SQL
            permissions: optional; e.g. 'households<75'
            params: optional; e.g. 'p1=123'
        Returns:
            :obj:`dq0.sdk.cli.runner.QueryRunner` instance
        """
        response = self.client.post(
            route=routes.query.create,
            data={'query': query,
                  'datasets_used': self.name,
                  'permissions': permissions,
                  'params': params
                  }
        )
        checkSDKResponse(response)
        query_uuid = response.get('query_uuid')
        if not query_uuid:
            raise DQ0SDKError('Did not receive query in CLI server response')
        return QueryRunner(self.project, query_uuid)

