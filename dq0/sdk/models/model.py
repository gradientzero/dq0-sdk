# -*- coding: utf-8 -*-
"""Model abstract base class

The Model class serves as the base class for all models.

Implementing subclasses have to define setup_data and setup_model functions.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import uuid
from abc import abstractmethod

from dq0.sdk.projects import Project

logger = logging.getLogger()


class Model(Project):
    """Abstract base class for all models available through the SDK.

    Model classes provide a setup method as well as the fit and predict
    ML model functions.

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
    def setup_data(self):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.
        """
        pass

    @abstractmethod
    def setup_model(self):
        """Setup model function

        Implementing child classes can use this method to define the model.
        """
        pass

    def fit(self):
        """Train model on a dataset passed as input.
        """
        pass

    @abstractmethod
    def save(self, path):
        """Saves the model.

        Implementing child classes should use this function to save the
        model in binary format on local storage.

        Args:
            path (:obj:`str`): The model path
        """
        pass

    @abstractmethod
    def load(self, path):
        """Loads the model.

        Implementing child classes should use this function to load the
        model from local storage.

        Args:
            path (:obj:`str`): The model path
        """
        pass

    @abstractmethod
    def get_clone(self):
        """
        Generates a new model with the same parameters, if they are not fit on
        the training data.

        Generates a deep copy of the model without actually
        copying any attached dataset. It yields a new model with the same
        parameters that has not been fit on any data. Parameters fit to
        the training data like, e.g., model weights, are re-initialized in the
        clone.

        Returns:
            deep copy of model

        """

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        pass

    @abstractmethod
    def to_string(self):
        """Print model type.

        Implementing child classes should use this function to print the
        model_type.
        """
    pass
