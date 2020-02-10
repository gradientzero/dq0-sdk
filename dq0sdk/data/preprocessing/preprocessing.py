# -*- coding: utf-8 -*-
"""
Collection of functions for preprocessing datasets, including data-scrubbing,
extraction of count features from corpora of documents, missing-data
handling, etc.

:Authors:
    Paolo Campigotto <pc@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
Copyright 2019, Gradient Zero
"""

import sys
from time import time

from dq0sdk.data.utils import util

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif


def handle_missing_data(dataset_df, mode='imputation',
                        imputation_method_for_cat_feats='unknown',
                        imputation_method_for_quant_feats='median',
                        categorical_features_list=None,
                        quantitative_features_list=None):

    if mode.lower() == 'imputation':

        if categorical_features_list is not None:

            if imputation_method_for_cat_feats.lower() == 'unknown':
                dataset_df[categorical_features_list] = dataset_df[
                    categorical_features_list].fillna('Unknown')
                print('Missing values in categorical features replaced with '
                      '"unknown" keyword')
            elif imputation_method_for_cat_feats.lower() == 'most_common_cat':
                # for each column, get value counts in decreasing order
                # and take the index (value) of most common category
                dataset_df[categorical_features_list] =\
                    dataset_df[categorical_features_list].apply(
                        lambda feat: feat.fillna(feat.value_counts().index[0]))
                print('Missing values in a categorical feature replaced '
                      'with feature most-common category')

        if quantitative_features_list is not None:

            if imputation_method_for_quant_feats.lower() == 'median':
                per_feature_imputation_value_ts = \
                    dataset_df[quantitative_features_list].median(axis=0)
            elif imputation_method_for_quant_feats.lower() == 'mean':
                per_feature_imputation_value_ts = \
                    dataset_df[quantitative_features_list].mean(axis=0)

            dataset_df[quantitative_features_list] = dataset_df[
                quantitative_features_list].fillna(
                per_feature_imputation_value_ts, axis=0)
            print(
                'Missing values in quantitat. feature replaced with feature'
                ' ' + imputation_method_for_quant_feats.lower() + ' value'
            )

    elif mode.lower() == 'dropping':

        dataset_df = _drop_instances_with_missing_values(dataset_df)
        print('Instances with missing values dropped')

    return dataset_df


def _drop_instances_with_missing_values(dataset_df):

    print('\nMissing values per feature:')
    print(util.missing_values_table(dataset_df))

    # drop rows with any missing value
    dataset_df.dropna(axis=0, how='any', inplace=True)
    # make index start from 0
    dataset_df.reset_index(drop=True, inplace=True)
    return dataset_df


def train_test_split(X_df, y_ts, num_tr_instances):
    #
    # ASSUMPTION: train instances on top, test instances at the bottom
    #
    # TODO  Make this more robust by adding a column defining tr / test status
    #       and split based on it rather than on above assumption

    # recover original split
    X_train_df = X_df.iloc[:num_tr_instances, :]
    X_test_df = X_df.iloc[num_tr_instances:, :]
    y_train_ts = y_ts.iloc[:num_tr_instances]
    y_test_ts = y_ts.iloc[num_tr_instances:]

    # make the index start from 0
    X_test_df.reset_index(drop=True, inplace=True)
    y_test_ts.reset_index(drop=True, inplace=True)

    return X_train_df, X_test_df, y_train_ts, y_test_ts


def extract_count_features_from_text_corpus(tr_data_list, test_data_list):
    """

    :param tr_data_list: list of text documents
    :param test_data_list: list of text documents
    :return: sparse Scipy matrices with the extracted features
    """

    print(
        '\nExtracting count features from the training documents using a '
        'sparse vectorizer. Tfidf features extracted.')
    sys.stdout.flush()
    t0 = time()
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')
    X_train_sp_matr = vectorizer.fit_transform(tr_data_list)
    util.print_human_readable_elapsed_time_value(
        elapsed_cpu_time_sec=time() - t0,
        s_tmp='Done in')
    print('n_samples: %d, n_features: %d' % X_train_sp_matr.shape)
    print()
    feature_names_list = vectorizer.get_feature_names()

    print(
        'Extracting count features from the test documents using the same '
        'vectorizer. Tfidf features extracted.')
    t0 = time()
    X_test_sp_matr = vectorizer.transform(test_data_list)
    util.print_human_readable_elapsed_time_value(
        elapsed_cpu_time_sec=time() - t0,
        s_tmp='Done in')
    print('n_samples: %d, n_features: %d' % X_train_sp_matr.shape)
    print()

    return X_train_sp_matr, X_test_sp_matr, feature_names_list


def univariate_feature_selection(num_top_ranked_feats_to_keep, X_train,
                                 y_train, X_test, technique,
                                 feature_names_list=None, verbose=False):

    print('\nUnivariate feature-selection: keep only the top',
          num_top_ranked_feats_to_keep, 'features '
                                        'ranked by ' + technique + '.')

    # reshape a 1-D array into a 2-D column array
    # y_train = y_train.reshape(y_train.shape[0], 1)

    if util.case_insensitive_str_comparison(technique, 'chi-squared test'):
        #
        # CHECK how Scikit handles multiple stat. tests. Bonferroni adjustment?
        #
        selector = SelectKBest(chi2, k=num_top_ranked_feats_to_keep)
    elif util.case_insensitive_str_comparison(technique,
                                              'mutual information'):
        selector = SelectKBest(mutual_info_classif,
                               k=num_top_ranked_feats_to_keep)

    X_train = selector.fit_transform(X_train, y_train)
    X_test = selector.transform(X_test)

    selected_feats_list = None
    if feature_names_list is not None:
        selected_feats_list = [feature_names_list[i] for i in
                               selector.get_support(indices=True)]

    if (selected_feats_list is not None) and verbose:
        util.pretty_print_strings_list(selected_feats_list, 'They are')

    return X_train, X_test, selected_feats_list


def scale_pixels(X_np_a, max_pixel_intensity):
    """
    Scale pixel values to be in [0, 1] to help gradient-descent optimization.
    :param X_np_a: Matrix of pixel intensities
    :param max_pixel_intensity: normalization constant set by user
    :return: matrix of scaled intensities of the pixels
    """

    print('\nScale pixel values to be in [0, 1] to help gradient-descent opt.')
    print('\tMax_pixel_intensity_detected:', X_np_a.max())
    print('\tNormalization constant used:', max_pixel_intensity)

    # convert from integers to floats
    X_np_a = X_np_a.astype('float32')
    # normalize to range 0-1
    X_np_a = X_np_a / max_pixel_intensity

    return X_np_a
