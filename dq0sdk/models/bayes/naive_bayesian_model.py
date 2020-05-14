# -*- coding: utf-8 -*-
"""Naive Bayesian Model class

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle

from dq0sdk.data.utils import plotting
from dq0sdk.data.utils import util
from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

from sklearn import metrics
from sklearn.naive_bayes import GaussianNB, MultinomialNB

logger = logging.getLogger()


class NaiveBayesianModel(Model):
    """Naive Bayesian model implementation.

    Simple model representing a bayesian classifier.
    """
    def __init__(self, **kwargs):
        super().__init__()

        if 'saved_model_folder' in kwargs:
            self._saved_model_folder = kwargs['saved_model_folder']
        else:
            self._saved_model_folder = './data/output'

        self._classifier_type = kwargs['classifier_type']

    def setup_data(self):
        """load train data."""
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        train_data, data = source.read()
        X_df, y_ts, num_tr_instances = source.preprocess(
            approach_for_missing_feature='imputation',
            # 'imputation', 'dropping',
            imputation_method_for_cat_feats='unknown',
            # 'unknown', 'most_common_cat'
            imputation_method_for_quant_feats='median',  # 'median', 'mean'
            features_to_drop_list=None
        )
        self.X_train = X_df
        self.y_train = y_ts

    def setup_model(self, kwargs):
        """
        Setup a Naive Bayesian classifier from sklearn.naive_bayes

        """

        if util.case_insensitive_str_comparison(self._classifier_type,
                                                'GaussianNB'):
            self._classifier = GaussianNB()

        elif util.case_insensitive_str_comparison(self._classifier_type,
                                                  'MultinomialNB'):
            self._classifier = MultinomialNB()
            if 'smoothing_prior' in kwargs:
                alpha = kwargs['smoothing_prior']
            else:
                alpha = .01
            self._classifier.set_params(alpha=alpha)

    def fit(self):
        """
        Model fit function: it learns a model from training data
        """
        X_train = self.X_train
        y_train = self.y_train

        if isinstance(y_train, np.ndarray):
            if y_train.ndim == 2:
                # make 1-dimensional array
                y_train = np.ravel(y_train)

        logger.debug('-------------------- ' + self._classifier_type + ' '
                     'classifier learning ---------------------')
        logger.debug('Percentage freq. of target labels in train dataset:')
        util.estimate_freq_of_labels(y_train)

        self._classifier.fit(X_train, y_train)

        logger.debug('Learned a ' + self._classifier_type + ' model. ')
        y_pred = self._classifier.predict(X_train)

        accuracy_score = metrics.accuracy_score(y_train, y_pred)
        logger.debug('Model accuracy on training data:', round(accuracy_score, 2))

        return accuracy_score

    def get_classes(self):
        """
        Just a wrapper for sklearn attribute classes_
        According to the documentation of scikit-learn v. 0.22:
            "classes_ :  array, shape (n_classes,)
                         class labels known to the classifier"

        """
        return self._classifier.classes_

    def predict(self, X_test):
        """
        Model predict function. Just a wrapper for sklearn predict()
        function.
        """

        y_pred = self._classifier.predict(X_test)
        return y_pred

    def predict_proba(self, X_test, top_n_proba_only=3):
        """
        Basically a wrapper for sklearn predict_proba() function.

        Args:
            X_test: test data
            top_n_proba_only: set to n to keep only the top-n class
                              probabilities. If set to None is has no
                              effect.

        Returns:
            Pandas DataFrame posterior_class_probab_df with class probabilities
        """

        assert (top_n_proba_only is None) or (top_n_proba_only >= 2)

        probs_np_a = self._classifier.predict_proba(X_test)

        probs_np_a, class_names = self._keep_top_n_class_probabilities_only(
            probs_np_a, top_n_proba_only)
        posterior_class_probab_df = pd.DataFrame(probs_np_a,
                                                 columns=class_names)

        return posterior_class_probab_df

    def _keep_top_n_class_probabilities_only(self, probs_np_a,
                                             top_n_proba_only):
        """Keep only top n class probabilities.

        Args:
            probs_np_a: numpy array with probabily classes
            top_n_proba_only: Keep only this many

        Returns:
            numpy.ndarray with top-n probabilities and class_names. If
            all the class probabilities are retained, class_names list contains
            the class names associated with the probabilities. Otherwise,
            class_list has the form ["top-1", "top-2", "top-3", ...]
        """

        num_proba = probs_np_a.shape[1]  # num. of classes of the
        # classification task
        if (top_n_proba_only is not None) and (top_n_proba_only < num_proba):
            logger.debug('Keep only the top-' + str(top_n_proba_only) + ' '
                         'probabilities')
            # minus sign to sort in descending order
            probs_np_a = - np.sort(- probs_np_a, axis=1)
            probs_np_a = probs_np_a[:, 0:top_n_proba_only]

            class_names = []
            for r in range(1, top_n_proba_only + 1):
                class_names.append('top_' + str(r))
        else:
            class_names = list(self.get_classes())

        return probs_np_a, class_names

    def evaluate(self, X_test, y_test, output_folder,
                 enable_plots=False,
                 classifier_description=''):
        """Test learnt classifier over a test set

        Args:
            X_test: test instances. pandas.DataFrame or numpy.ndarray
            y_test: learning signal. pandas.Series or numpy.ndarray
            output_folder: The output folder
            enable_plots: flag to generate a jpg file with the confusion matrix
            classifier_description: name of file containing the confusion matrix (if enabled)

        Returns:
            accuracy score over test set
        """

        logger.debug('--------------------- Testing learnt classifier '
                     '---------------------')

        if isinstance(y_test, np.ndarray):
            if y_test.ndim == 2:
                # Make 1-dimensional arrays
                y_test = np.ravel(y_test)

        y_pred_np_a = self._classifier.predict(X_test)

        logger.debug('Percentage freq. of target labels in test dataset (baseline '
                     'for classification performance):')
        util.estimate_freq_of_labels(y_test)

        accuracy_score = metrics.accuracy_score(y_test, y_pred_np_a)
        logger.debug('Model accuracy on test data:', round(accuracy_score, 2))
        logger.debug('', metrics.classification_report(y_test, y_pred_np_a))

        logger.debug('Normalized confusion matrix:')
        cm_df, _ = plotting.compute_confusion_matrix(
            y_test, y_pred_np_a, normalize='true'
        )
        logger.debug(cm_df)
        # By default, labels that appear at least once in y_test or
        # y_pred_np_a are used in sorted order in the confusion matrix.

        if enable_plots:
            plotting.plot_confusion_matrix_for_scikit_classifier(
                self._classifier,
                X_test.values if isinstance(X_test, pd.DataFrame) else X_test,
                y_test.values if isinstance(y_test, pd.Series) else y_test,
                class_names=None,
                xticks_rotation='horizontal',
                part_of_fn_describing_matrix=classifier_description,
                output_folder=output_folder
            )

        return accuracy_score

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        with open(os.path.join(self._saved_model_folder, name, version), 'wb') as f:
            pickle.dump(self._classifier, f)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        with open(os.path.join(self._saved_model_folder, name, version), 'rb') as file:
            self._classifier = pickle.load(file)
