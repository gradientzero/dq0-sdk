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

    def __init__(self, source, project=None):
        if source is None:
            raise ValueError('You need to provide the "source" argument')
        self.source = source
        self.project = project
        self.where_clause = None

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
