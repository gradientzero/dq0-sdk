# -*- coding: utf-8 -*-
"""Naive Bayesian Model class

Copyright 2020, Gradient Zero
All rights reserved
"""

import copy
import logging
import os
import pickle

from dq0.sdk.data.utils import util
from dq0.sdk.models.model import Model

import numpy as np

import sklearn
from sklearn.calibration import CalibratedClassifierCV

logger = logging.getLogger()


class NaiveBayesianModel(Model):
    """Naive Bayesian classifier implementation.

    Simple model representing a Bayesian classifier.
    """

    def __init__(self):
        super().__init__()

        # to instantiate the suitable model checker from dq0-core.dq0.util
        self.model_type = 'NaiveBayesianClassifier'

        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.metrics = None

        # calibrate posterior probabilities of the fitted model
        self.calibrate_posterior_probabilities = True
        self.calibration_method = 'isotonic'

    def to_string(self):
        print('\nModel type is: ', self.model_type)

    def save(self, path):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            path (str): The model path
        """

        # create target directory and all intermediate directories if not
        # existing
        file_path_dirs = os.path.dirname(path)
        if not os.path.exists(file_path_dirs):
            os.makedirs(file_path_dirs)

        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path):
        """Loads the model.

        Load the model from local storage.

        Args:
            path (str): The model path
        """
        with open(path, 'rb') as file:
            self.model = pickle.load(file)

    def get_clone(self, trained=False):
        """
        Generates a new model with the same parameters, if they are not fit on
        the training data.

        Generates a deep copy of the model without actually
        copying any attached dataset. It yields a new model with the same
        parameters that has not been fit on any data. Parameters fit to
        the training data like, e.g., model weights, are re-initialized in the
        clone.

        Args:
            trained: if `True`, maintains current state including trained model
                weights, etc. Otherwise, returns an unfitted model with the
                same initialization params.

        Returns:
            deep copy of model

        """

        if trained:
            new_scikit_model = copy.deepcopy(self.model)
        else:
            # Clone does a deep copy of the model without actually copying
            # attached data. It yields a new model with the same parameters
            # that has not been fit on any data.
            new_scikit_model = sklearn.base.clone(self.model)
            # keep class labels if they have been specified
            try:
                new_scikit_model.classes_ = self.model.classes_
            except AttributeError:
                pass

        # performance boosting: do not (deep) copy any data that will be
        # discarded immediately after deep copying
        tmp_storage = {'model': self.model, 'X_train': self.X_train,
                       'y_train': self.y_train, 'X_test': self.X_test,
                       'y_test': self.y_test}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.data_source = None

        # model clone
        # new_model = self.__class__()
        new_model = copy.deepcopy(self)
        new_model.model = new_scikit_model

        # recover attributes temporarily removed for efficient deep copying
        for key, value in tmp_storage.items():
            self.__setattr__(key, value)

        return new_model

    def fit(self):
        """
        Model fit function learning a model from training data
        """

        if self.model is None:
            logger.fatal('No Scikit-learn model provided!')

        # Check for valid model setup
        if not hasattr(self, 'X_train'):
            raise ValueError('Missing argument in model: X_train')
        if not hasattr(self, 'y_train'):
            raise ValueError('Missing argument in model: y_train')

        if isinstance(self.y_train, np.ndarray):
            if self.y_train.ndim == 2:
                # make 1-dimensional array
                self.y_train = np.ravel(self.y_train)

        if hasattr(self, '_classifier_type'):
            print('\n' + self._classifier_type + ' classifier learning...')
        else:
            print('\nClassifier learning...')

        print('\nPercentage frequency of target labels in the training '
              'dataset:')
        util.estimate_freq_of_labels(self.y_train)

        if self.calibrate_posterior_probabilities:
            self.model = CalibratedClassifierCV(
                self.model, cv=5, method=self.calibration_method
            )

        self.model.fit(self.X_train, self.y_train)

        self._print_fit_log()

    def _print_fit_log(self):

        if hasattr(self, '_classifier_type'):
            partial_str = ' ' + self._classifier_type
        else:
            partial_str = ''

        if not self.calibrate_posterior_probabilities:
            calibration_descr = ''
        else:
            if self.calibration_method == 'sigmoid':
                calibration_method_descr = 'logistic regression'
            elif self.calibration_method == 'isotonic':
                calibration_method_descr = 'isotonic regression'

            calibration_descr = ' Calibrated its posterior probabilities ' \
                                'by using ' + calibration_method_descr + '.'

        print('\nLearned a' + partial_str + ' model from',
              self.X_train.shape[0], 'examples.' + calibration_descr)

    def evaluate(self, test_data=True):
        """Model evaluate implementation.

        Args:
            test_data (bool): False to use train data instead of test
                Default is True.
        """
        if self.model is None:
            logger.fatal('No Scikit-learn model provided!')

        # Check for valid model setup
        if not test_data and not hasattr(self, 'X_train'):
            logger.fatal('Missing argument in model: X_train')
            return
        if not test_data and not hasattr(self, 'y_train'):
            logger.fatal('Missing argument in model: y_train')
            return
        if test_data and not hasattr(self, 'X_test'):
            logger.fatal('Missing argument in model: X_test')
            return
        if test_data and not hasattr(self, 'y_test'):
            logger.fatal('Missing argument in model: y_test')
            return

        X = self.X_test if test_data else self.X_train
        y = self.y_test if test_data else self.y_train

        if isinstance(y, np.ndarray):
            if y.ndim == 2:
                # Make 1-dimensional arrays
                y = np.ravel(y)

        y_pred_np_a = self.model.predict(X)

        # accuracy = sklearn.metrics.accuracy_score(y, y_pred_np_a)
        #
        # evaluation_res = {'accuracy': accuracy}
        # util.print_evaluation_res(
        #     evaluation_res,
        #     'test' if test_data else 'training'
        # )

        self.metrics = util.instantiate_metrics_from_name(self.metrics)
        evaluation_res = util.compute_metrics_scores(y, y_pred_np_a,
                                                     self.metrics)
        util.print_evaluation_res(
            evaluation_res,
            'test' if test_data else 'training'
        )

        return evaluation_res
