#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Wolfgang Gross <wg@gradient0.com>
"""

from dq0sdk.data_connector import util


def _handle_missing_data(dataset_df, mode='imputation',
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
            print('Missing value in a quantitative feature replaced with '
                  'feature ' + imputation_method_for_quant_feats.lower()
                  + ' value')

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


def train_test_split(X_df, y_ts,num_tr_instances):

    # ASSUMPTION: train instances on top, test instances at the bottom
    # TODO: Make this more robust by adding a column defining tr / test status
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