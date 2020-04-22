# -*- coding: utf-8 -*-
"""Model abstract base class

The Model class serves as the base class for all models.

Implementing subclasses have to define setup_data and setup_model functions.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import uuid
from abc import ABC, abstractmethod

logger = logging.getLogger()


class Model(ABC):
    """Abstract base class for all models available through the SDK.

    Model classes provide a setup method as well as the fit and predict
    ML model functions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.

    Attributes:
        model_type (:obj:`str`): type of this model instance. Options: 'keras'.
        model_path (:obj:`str`): path of model (save / load)
        uuid (:obj:`str`): UUID of this model.
        data_source (:obj:`dq0sdk.data.Source`): dict of attached data sources.

    """
    def __init__(self, model_path):
        super().__init__()
        # data source, model path and uuid will be set at runtime
        self.data_source = None
        self.model_path = model_path
        self.uuid = uuid.uuid1()
        self.model_type = ''

    def attach_data_source(self, data_source):
        """Add a data source to the model.

        This function needs to be called at least once. All data
        operations will use one of the attached data sources.

        Args:
            data_source (:obj:`dq0sdk.data.Source`): The new data source to add
        """
        self.data_source = data_source

    @abstractmethod
    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    @abstractmethod
    def setup_model(self, **kwargs):
        """Setup model function

        Implementing child classes can use this method to define the
        Keras model.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    @abstractmethod
    def fit(self, **kwargs):
        """

        Train model on a dataset passed as input.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """

    @abstractmethod
    def save(self):
        """Saves the model.

        Implementing child classes should use this function to save the
        model in binary format on local storage.

        The implemented child class version will be final (non-derivable).
        """
        pass

    @abstractmethod
    def load(self):
        """Loads the model.

        Implementing child classes should use this function to load the
        model from local storage.

        The implemented child class version will be final (non-derivable).
        """
        pass
