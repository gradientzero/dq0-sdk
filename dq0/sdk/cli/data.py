# -*- coding: utf-8 -*-
"""Data allows for the execution of db stats jobs

A data object will be created at runtime from a project instance.

Copyright 2020, Gradient Zero
All rights reserved
"""


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

    """

    def __init__(self, project=None):
        if project is None:
            raise ValueError('You need to provide the "project" argument')
        self.project = project

    def mean(self, cols=None, query=None):
        """Gets the differential private mean value of the given columns

        Args:
            cols: list of columns in the dataset to include. None for all available columns.
            query: optional additional query to run against the dataset before calculating the mean.

        Returns:
            New instance of the ModelRunner class representing the prediction run.
        """
        # TODO
        pass
