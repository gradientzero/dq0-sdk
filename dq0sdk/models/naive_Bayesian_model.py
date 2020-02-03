# -*- coding: utf-8 -*-
"""Naive Bayesian Model class

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>

Copyright 2019, Gradient Zero
"""

import os
import pickle

import diffprivlib.models as dp

from dq0sdk.data.utils import plotting
from dq0sdk.data.utils import util
from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

from sklearn import metrics
from sklearn.naive_bayes import GaussianNB, MultinomialNB


class NaiveBayesianModel(Model):

    def __init__(self, **kwargs):

        super().__init__()

        if 'saved_model_folder' in kwargs:
            self._saved_model_folder = kwargs['saved_model_folder']
        else:
            self._saved_model_folder = './data/output'
        self._classifier_type = kwargs['classifier_type']

        if 'DP_enabled' in kwargs:
            self.DP_enabled = kwargs['DP_enabled']
        else:
            self.DP_enabled = False

        if util.case_insensitive_str_comparison(self._classifier_type,
                                                'GaussianNB'):

            if not self.DP_enabled:
                self._classifier = GaussianNB()
            else:
                self._classifier_type = 'DP-' + self._classifier_type
                self.DP_epsilon = kwargs['DP_epsilon']
                self._classifier = dp.GaussianNB(
                    epsilon=self.DP_epsilon,
                    bounds=kwargs['features_bounds']
                )

        elif util.case_insensitive_str_comparison(self._classifier_type,
                                                  'MultinomialNB'):
            if not self.DP_enabled:
                self._classifier = MultinomialNB()
            else:
                self._classifier_type = 'DP-' + self._classifier_type
                self.DP_epsilon = kwargs['DP_epsilon']
                raise RuntimeError('DP-version of MultinomialNB not yet '
                                   'available!')

            if 'smoothing_prior' in kwargs:
                alpha = kwargs['smoothing_prior']
            else:
                alpha = .01
            self._classifier.set_params(alpha=alpha)

    def setup_data(self, **kwargs):
        # to inherit from abstract base class
        pass

    def setup_model(self, **kwargs):
        # to inherit from abstract base class
        pass

    def prepare(self, **kwargs):
        # to inherit from abstract base class
        pass

    def fit(self, **kwargs):
        """
        Model fit function: it learns a model from training data
        """

        X_train_df = kwargs['X_train_df']
        y_train_ts = kwargs['y_train_ts']

        print('\n\n-------------------- ' + self._classifier_type + ' '
              'classifier learning ---------------------')
        if self.DP_enabled:
            print('DP epsilon set to', self.DP_epsilon)
        print('\nPercentage freq. of target labels in train dataset:')
        print(y_train_ts.value_counts(normalize=True) * 100)

        self._classifier.fit(X_train_df, y_train_ts)

        print('\nLearned a ' + self._classifier_type + ' model. ')
        y_pred = self._classifier.predict(X_train_df)

        accuracy_score = metrics.accuracy_score(y_train_ts, y_pred)
        print('\nModel accuracy on training data:', round(accuracy_score, 2))

    def fit_dp(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
        """
        raise RuntimeError('to fit a model with dp, crate an instance '
                           'of this class enabling DP and call the fit method')
        pass

    def get_classes(self):
        """
        Just a wrapper for sklearn attribute classes_
        According to the documentation of scikit-learn v. 0.22:
            "classes_ :  array, shape (n_classes,)
                         class labels known to the classifier"

        """
        return self._classifier.classes_

    def predict(self, X_test, **kwargs):
        """
        Model predict function. Just a wrapper for sklearn predict()
        function.
        """

        y_pred = self._classifier.predict(X_test)
        return y_pred

    def predict_proba(self, X_test, top_n_proba_only=3):
        """
        Basically a wrapper for sklearn predict_proba() function.
        :param X_test:
        :param top_n_proba_only: set to n to keep only the top-n class
                                 probabilities. If set to None is has no
                                 effect.
        :return: Pandas DataFrame posterior_class_probab_df with class
                 probabilities
        """

        assert (top_n_proba_only is None) or (top_n_proba_only >= 2)

        probs_np_a = self._classifier.predict_proba(X_test)

        # print(type(probs_np_a))
        probs_np_a, class_names = self._keep_top_n_class_probabilities_only(
            probs_np_a, top_n_proba_only)
        posterior_class_probab_df = pd.DataFrame(probs_np_a,
                                                 columns=class_names)

        return posterior_class_probab_df  # probs_np_a

    def _keep_top_n_class_probabilities_only(self, probs_np_a,
                                             top_n_proba_only):
        """

        :param probs_np_a:
        :param top_n_proba_only:
        :return: numpy.ndarray with top-n probabilities and class_names. If
        all the class probabilities are retained, class_names list contains
        the class names associated with the probabilities. Otherwise,
        class_list has the form ["top-1", "top-2", "top-3", ...]
        """

        num_proba = probs_np_a.shape[1]  # num. of classes of the
        # classification task
        if (top_n_proba_only is not None) and (top_n_proba_only < num_proba):
            print("\nKeep only the top-" + str(top_n_proba_only) + " "
                  "probabilities")
            # minus sign to sort in descending order
            probs_np_a = - np.sort(- probs_np_a, axis=1)
            probs_np_a = probs_np_a[:, 0:top_n_proba_only]

            class_names = []
            for r in range(1, top_n_proba_only + 1):
                class_names.append("top_" + str(r))
        else:
            class_names = list(self.get_classes())

        return probs_np_a, class_names

    def evaluate(self, X_test_df, y_test_ts, output_folder,
                 enable_plots=False,
                 classifier_description=''
                 ):
        """
        Test learnt classifier over a test set
        :param X_test_df: test instances
        :param y_test_ts: learning signal
        :param output_folder:
        :param enable_plots: flag to generate a jpg file with the confusion
                             matrix
        :param classifier_description: name of file containing the confusion
                                       matrix (if enabled)
        :return: accuracy score over test set
        """

        print('\n\n--------------------- Testing learnt classifier '
              '---------------------')

        y_pred_np_a = self._classifier.predict(X_test_df)

        print(
            '\nPercentage freq. of target labels in test dataset (baseline '
            'for classification performance):')
        print(y_test_ts.value_counts(normalize=True) * 100)

        accuracy_score = metrics.accuracy_score(y_test_ts, y_pred_np_a)
        print('\nModel accuracy on test data:', round(accuracy_score, 2))
        print('\n', metrics.classification_report(y_test_ts, y_pred_np_a))

        # print('\nConfusion matrix:')
        # print(metrics.confusion_matrix(y_test_ts, y_pred_np_a))
        #
        # By default, labels that appear at least once in y_test_ts or
        # y_pred_np_a are used in sorted order in the confusion matrix.

        if enable_plots:
            plotting.plot_confusion_matrix_for_scikit_classifier(
                self._classifier,
                X_test_df.values,
                y_test_ts.values,
                class_names=None,
                xticks_rotation='horizontal',
                part_of_fn_describing_matrix=classifier_description,
                output_folder=output_folder
            )

        return accuracy_score

    def save(self, name='model', version=None):
        """Saves the model in binary format on local storage.

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """

        if version is not None:
            name += '_v' + str(version)
        name += '.pickle'

        with open(os.path.join(self._saved_model_folder, name), 'wb') as f:
            pickle.dump(self._classifier, f)

    def load(self, name, version):
        """Loads the model from local storage.

        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """

        if version is not None:
            name += '_v' + str(version)
        name += '.pickle'

        with open(os.path.join(self._saved_model_folder, name), 'rb') as file:
            self._classifier = pickle.load(file)
