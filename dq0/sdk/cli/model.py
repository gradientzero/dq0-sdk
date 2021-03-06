# -*- coding: utf-8 -*-
"""Model allows for the execution of prediction jobs

A model will be created at runtime. It belongs to a project.

Calling predict through Model will return a ModelRunner instance
that can be used to further control the job

Model wraps the following CLI commands:
    * dq0 model predict

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.cli.api import routes
from dq0.sdk.cli.runner import ModelRunner
from dq0.sdk.errors import checkSDKResponse

import numpy as np


class Model:
    """A model predict wrapper

    Provides methods to call model predict

    Example:
        >>> # get the latest model
        >>> model = project.get_latest_model() # doctest: +SKIP
        >>>
        >>> # check DQ0 privacy clearing
        >>> if model.predict_allowed: # doctest: +SKIP
        >>>
        >>>    # call predict
        >>>    run = model.predict(np.array([1, 2, 3])) # doctest: +SKIP
        >>>
        >>>    # wait for completion
        >>>    run.wait_for_completion(verbose=True) # doctest: +SKIP
        >>>
        >>>    # get training results
        >>>    print(run.get_results()) # doctest: +SKIP

    Args:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this experiment belongs to

    Attributes:
        project (:obj:`dq0.sdk.cli.Project`): The project
            this experiment belongs to
        predict_allowed (bool): True if the model was checked by DQ0
            and flagged as safe. Note that this attribute is here for
            convenience. The actual allowance check is done by dq0-main.

    """

    def __init__(self, project=None):
        if project is None:
            raise ValueError('You need to provide the "project" argument')
        self.project = project
        self.predict_allowed = False

        # TODO: get model info and set predict allowed
        self.predict_allowed = True

    def predict(self, test_data):
        """Starts a prediction run

        It calls the CLI command `model predict` and returns
        a Runner instance to watch to job

        Args:
            test_data (:obj:`numpy.array`) data to perform prediction for

        Returns:
            New instance of the ModelRunner class representing the prediction run.
        """
        if test_data is None or not isinstance(test_data, np.ndarray):
            raise ValueError('test_data not in np.array format')
        response = self.project._deploy()
        checkSDKResponse(response)

        # save predict data
        np.save('predict_data.npy', test_data)
        data = {'input_path': os.path.abspath('predict_data.npy')}

        response = self.project.client.post(
            routes.model.predict, id=self.project.model_uuid, data=data)
        checkSDKResponse(response)
        print(response['message'])
        return ModelRunner(self.project)
