# -*- coding: utf-8 -*-
"""20Newsgroups Data Source.

This is a data source example known from the Scikit-learn API:
https://scikit-learn.org/stable/datasets/index.html#the-20-newsgroups-text-dataset

The 20 newsgroups dataset comprises around 18000 newsgroups posts on 20 topics split
in two subsets: one for training (or development) and the other one for testing
(or for performance evaluation). The split between the train and test set is based
upon a messages posted before and after a specific date.

Copyright 2020, Gradient Zero
All rights reserved
"""

import ssl

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.source import Source
from dq0sdk.data.utils import util

import pandas as pd

from sklearn.datasets import fetch_20newsgroups


class NewsgroupsSource(Source):
    """Data Source for 20Newsgroups.

    Newsgroups posts on 20 topics from scikit-learn.
    """
    def __init__(self):
        super().__init__()

    def read(self):
        """Read the 20newsgroups data source

        Args:
            kwargs: keyword arguments

        Returns:
            data read from the data source.
        """
        tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature = \
            self._get_train_and_test_dataset()

        # util.print_dataset_info(tr_dataset_df, 'Raw training dataset')
        # util.print_dataset_info(test_dataset_df, 'Raw test dataset')

        X_train_df = tr_dataset_df.drop([target_feature], axis=1)
        X_test_df = test_dataset_df.drop([target_feature], axis=1)
        y_train_ts = tr_dataset_df[target_feature]
        y_test_ts = test_dataset_df[target_feature]

        # concatenate training and test datasets
        assert isinstance(X_train_df, pd.DataFrame)
        X_df = X_train_df.append(X_test_df)
        y_ts = y_train_ts.append(y_test_ts)

        util.print_dataset_info(X_df, 'Raw dataset')

        return X_df, y_ts

    def _get_train_and_test_dataset(self):
        """'20_Newsgroups' is a corpus of labeled documents. We extract features
        by counting word occurrences (Tfidf). However, since the dictionary
        of words is quite big, the code allow to keep only the most
        discriminative words for the classification task.

        Returns:
            train and test data sets for 20newsgroups.
        """

        # print('Fetching "20 newsgroups" dataset from remote repository')
        to_be_removed = ('headers', 'footers', 'quotes')

        # WORKAROUND to fix CERTIFICATE_VERIFY_FAILED error when trying out
        # requests-html on Mac. See:
        #   https://timonweb.com/tutorials/fixing-certificate_verify_failed-
        #   error-when-trying-requests_html-out-on-mac/
        # for details
        ssl._create_default_https_context = ssl._create_unverified_context

        # Select the labels for the classification task
        # To load all newsgroups topics: set to None
        # newsgroups_topics = ['alt.atheism', 'talk.religion.misc',
        #                     'comp.graphics', 'sci.space']
        newsgroups_topics = None

        num_top_ranked_feats_to_keep = int(
            2e4)  # set to 'all' to skip feat sel.
        if str(num_top_ranked_feats_to_keep).lower() != 'all':
            technique_for_feat_sel = 'chi-squared test'  # 'mutual information'

        params_dict = {
            'data_home': self.input_folder,
            'subset': 'train',
            'shuffle': True,
            'random_state': 42,  # for reproducible output across multiple
            # function calls
            'remove': to_be_removed,
            'categories': newsgroups_topics
        }

        tr_data = fetch_20newsgroups(**params_dict)
        params_dict['subset'] = 'test'
        test_data = fetch_20newsgroups(**params_dict)

        # print('Data fetched')
        print('Loaded "20_Newsgroups" dataset')
        print('%d training documents' % len(tr_data.filenames))
        print('%d test documents' % len(test_data.filenames))
        print('%d different classes of documents' % len(
            tr_data.target_names))

        util.pretty_print_strings_list(
            list(tr_data.target_names), 'Classes of 20-Newsgroup dataset')

        tr_data_list = tr_data.data  # list of text documents
        test_data_list = test_data.data
        y_train_np_a, y_test_np_a = tr_data.target, test_data.target

        X_train_sp_matr, X_test_sp_matr, feature_names_list = \
            preprocessing.extract_count_features_from_text_corpus(
                tr_data_list,
                test_data_list
            )

        if str(num_top_ranked_feats_to_keep).lower() != 'all':
            X_train_sp_matr, X_test_sp_matr, feature_names_list = \
                preprocessing.univariate_feature_selection(
                    num_top_ranked_feats_to_keep,
                    X_train_sp_matr,
                    y_train_np_a,
                    X_test_sp_matr,
                    technique=technique_for_feat_sel,
                    feature_names_list=feature_names_list
                )

        tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature = \
            self._build_data_structures(X_train_sp_matr, X_test_sp_matr,
                                        feature_names_list, y_train_np_a,
                                        y_test_np_a,
                                        sparse_representation=False)

        return tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature

    def _build_data_structures(self, X_train_sp_matr, X_test_sp_matr,
                               feature_names_list, y_train_np_a, y_test_np_a,
                               sparse_representation=True):
        """Data structure helper function."""
        tr_dataset_df = util.sparse_scipy_matrix_to_Pandas_df(
            X_train_sp_matr,
            sparse_representation,
            columns_names_list=feature_names_list)

        test_dataset_df = util.sparse_scipy_matrix_to_Pandas_df(
            X_test_sp_matr,
            sparse_representation,
            columns_names_list=feature_names_list)

        target_feature = 'class_label'
        tr_dataset_df[target_feature] = y_train_np_a
        test_dataset_df[target_feature] = y_test_np_a
        categorical_features_list = None
        quantitative_features_list = feature_names_list

        return tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature

    def preprocess(self, force=False, **kwargs):
        pass

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
