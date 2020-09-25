# -*- coding: utf-8 -*-
"""20Newsgroups Data Source.

This is a data source example known from the Scikit-learn API:
https://scikit-learn.org/stable/datasets/index.html#the-20-newsgroups-text-dataset

The 20 newsgroups dataset comprises around 18000 newsgroups posts on 20 topics
split in two subsets: one for training (or development) and the other one
for testing (or for performance evaluation). The split between the train and
test set is based upon a messages posted before and after a specific date.

Copyright 2020, Gradient Zero
All rights reserved
"""

from pathlib import Path

from dq0.sdk.data.preprocessing import preprocessing
from dq0.sdk.data.utils import util
from dq0.sdk.examples.newsgroups._data.dump_text_labels_to_df_csv import \
    _dump_text_and_labels_to_csv

import pandas as pd

from sklearn.model_selection import train_test_split


def _generate_preprocessed_dataset(X, y):

    # fillna with empty strings (exist in original)
    X.fillna("", inplace=True)

    # Split for preprocessing
    # If the input is sparse, the output will be a scipy.sparse.csr_matrix.
    # Otherwise, output type is the same as the input type.
    X_train_df, X_test_df, y_train_se, y_test_se = \
        train_test_split(X, y, test_size=0.1)

    X_train_sp_matr, X_test_sp_matr, feature_names_list = \
        preprocessing.extract_count_features_from_text_corpus(
            X_train_df.values.tolist(),
            X_test_df.values.tolist()
        )

    # Set the number of features for feature extraction
    #
    # WARNING!!! when setting num_top_ranked_feats_to_keep to 20k,
    # DP fitting takes more than an hour
    #
    num_top_ranked_feats_to_keep = int(5e3)  # set to 'all' to skip feat sel.
    if str(num_top_ranked_feats_to_keep).lower() != 'all':
        technique_for_feat_sel = 'chi-squared test'  # 'mutual information'

    if str(num_top_ranked_feats_to_keep).lower() != 'all':
        X_train_sp_matr, X_test_sp_matr, feature_names_list = \
            preprocessing.univariate_feature_selection(
                num_top_ranked_feats_to_keep,
                X_train_sp_matr,
                y_train_se,
                X_test_sp_matr,
                technique=technique_for_feat_sel,
                feature_names_list=feature_names_list
            )

    sparse_representation = False
    X_train_df = util.sparse_scipy_matrix_to_Pandas_df(
        X_train_sp_matr,
        sparse_representation,
        columns_names_list=feature_names_list)

    X_test_df = util.sparse_scipy_matrix_to_Pandas_df(
        X_test_sp_matr,
        sparse_representation,
        columns_names_list=feature_names_list)

    X = pd.concat([X_train_df, X_test_df], ignore_index=True)
    y = pd.concat([y_train_se, y_test_se], ignore_index=True)
    y.name = 'label'
    df = pd.concat([X, y], axis=1)

    print('\nGenerated dataset for 20Newsgroups:')
    print('\tfeature matrix shape:', X.shape)
    print('\tclass-labels vector shape:', y.shape)
    print('\tnum classes:', y.nunique())
    print('\tShape of DataFrame saved in file:', df.shape)

    return df


if __name__ == '__main__':

    # fetch raw text data
    raw_data_csv = '../dq0-sdk/dq0/sdk/examples/newsgroups/_data' \
                   '/20newsgroups_text_label_df.csv'

    if not Path(raw_data_csv).is_file():
        # file does not exists
        _dump_text_and_labels_to_csv(raw_data_csv)

    dataset = pd.read_csv(raw_data_csv)

    df = _generate_preprocessed_dataset(dataset.iloc[:, 0], dataset.iloc[:, 1])

    df.to_csv(
        '../dq0-sdk/dq0/sdk/examples/newsgroups/_data/preprocessed_dataset'
        '.csv', index=False
    )

    # preprocessed_dataset.csv size is 366MB, so it is not kept in the
    # repository.
