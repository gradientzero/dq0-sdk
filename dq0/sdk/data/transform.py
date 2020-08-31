# -*- coding: utf-8 -*-
"""Data Transform class.

Copyright 2020, Gradient Zero
"""

import uuid

from abc import abstractmethod

from dq0.sdk.projects import Project


class Transform(Project):
    """Abstract base class for all transformations available through the SDK.

    Transform classes provide a execute method to transform source data

    Attributes:
        model_type (:obj:`str`): type of this model instance. Options: 'keras'.
        uuid (:obj:`str`): UUID of this model.
        data_source (:obj:`dq0.sdk.data.Source`): dict of attached data sources.

    """

    def __init__(self):
        super().__init__()
        # data source, model path and uuid will be set at runtime
        self.data_source = None
        self.uuid = uuid.uuid1()
        self.model_type = ''

    @abstractmethod
    def execute(self, dataset=None):
        """Execute transformation function

        This function can be used by child classes to prepare data 
        that dont need to be repeated for every training run.
        """
        pass
