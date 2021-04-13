# -*- coding: utf-8 -*-
"""Project abstract base class

The Project class serves as the base class for all models and data jobs.

Copyright 2020, Gradient Zero
All rights reserved
"""

from abc import ABC


class Project(ABC):
    """Abstract base class for all all models and data jobs.

    Project classes provide a attach_data_source function that is used to
    assign a selected data source to a project (to be used by model or data jobs).

    Attributes:
        data_source (:obj:`dq0.sdk.data.Source`): attached data source.
    """

    def __init__(self, data_source=None):
        super().__init__()
        self.data_source = None
        self.data_sources = None
        if data_source is not None:
            self.attach_data_source(data_source)

    def attach_data_source(self, data_source):
        """Attach a data source to the project.

        This function needs to be called at least once. All data
        operations will use one of the attached data sources.

        Args:
            data_source (:obj:`dq0.sdk.data.Source`): The new data source to attach
        """
        self.data_source = data_source
        if self.data_sources is None:
            self.data_sources = []
        self.data_sources.append(data_source)

    def detach_data_source(self, data_source):
        """Detaches a data source from the project.

        Args:
            data_source (:obj:`dq0.sdk.data.Source`): The data source to remove
        """
        try:
            if self.data_sources is not None:
                self.data_sources.remove(data_source)
        except ValueError:
            pass
        if self.data_sources is None or len(self.data_sources) < 1:
            self.data_source = None
