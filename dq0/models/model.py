# -*- coding: utf-8 -*-
"""Model abstract base class

The Model class serves as the base class for all models.

Implementing subclasses have to define setup, fit and predict fucntions.

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
"""

from abc import ABC, abstractmethod


class Model(ABC):
    """Abstract base class for all models available through the SDK.

    Model classes provide a setup method as well as the fit and predict
    ML model functions.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def setup(self, **kwargs):
        """Setup function

        Implementing child classes can use this method to provide
        basic setup functionality.

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    @abstractmethod
    def fit(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.

        Returns:
            model: fitted model. TODO: needs discussion!
        """
        pass

    @abstractmethod
    def fit_dp(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.

        Returns:
            model: fitted model. TODO: needs discussion!
        """
        pass

    @abstractmethod
    def predict(self, **kwargs):
        """Model predict function.

        Implementing child classes will perform model scoring here.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        pass
