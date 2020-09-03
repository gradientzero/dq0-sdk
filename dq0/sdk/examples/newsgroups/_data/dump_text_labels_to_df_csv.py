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

from sklearn.datasets import fetch_20newsgroups

import numpy as np

import pandas as pd

# remove below packages
from dq0.sdk.data.preprocessing import preprocessing
from dq0.sdk.data.utils import util
from sklearn.model_selection import train_test_split


if __name__ == '__main__':
    csv_path = 'dq0/sdk/examples/newsgroups/_data/20newsgroups_text_label_df.csv'

    to_be_removed = ('headers', 'footers', 'quotes')

    # Select the labels for the classification task
    # To load all newsgroups topics: set to None
    # newsgroups_topics = ['alt.atheism', 'talk.religion.misc',
    #                     'comp.graphics', 'sci.space']
    newsgroups_topics = None

    params_dict = {
        'subset': 'train',
        'shuffle': True,
        'random_state': 42,  # for reproducible output across multiple
        # function calls
        'remove': to_be_removed,
        'categories': newsgroups_topics
    }

    train = fetch_20newsgroups(**params_dict)
    params_dict['subset'] = 'test'
    test = fetch_20newsgroups(**params_dict)
    
    X_train = train.data  # list of text documents
    X_test = test.data
    y_train_np_a, y_test_np_a = train.target, test.target

    X = X_train + X_test
    y = np.hstack([y_train_np_a, y_test_np_a])

    print(len(X))

    dataset = pd.DataFrame(X, columns = ['text'])
    dataset['y'] = y

    dataset.to_csv(csv_path,
                   index=False)
    
    # # TESTING CODE FOR USER MODEL
    # num_top_ranked_feats_to_keep = int(
    #     5e3)  # set to 'all' to skip feat sel.
    # if str(num_top_ranked_feats_to_keep).lower() != 'all':
    #     technique_for_feat_sel = 'chi-squared test'  # 'mutual information'

    # dataset = pd.read_csv(csv_path)
    # X = dataset.iloc[:,0]
    # y = dataset.iloc[:,1]
    
    # # fillna with empty strings (exist in original)
    # X.fillna("", inplace=True)

    # # Split for preprocessing
    # X_train_df, X_test_df, y_train_np_a, y_test_np_a =\
    #     train_test_split(X, y,
    #                     test_size=0.33,
    #                     random_state=42)
    
    # X_train_sp_matr, X_test_sp_matr, feature_names_list = \
    #         preprocessing.extract_count_features_from_text_corpus(
    #             X_train_df.values.tolist(),
    #             X_test_df.values.tolist()
    #         )

    # if str(num_top_ranked_feats_to_keep).lower() != 'all':
    #     X_train_sp_matr, X_test_sp_matr, feature_names_list = \
    #         preprocessing.univariate_feature_selection(
    #             num_top_ranked_feats_to_keep,
    #             X_train_sp_matr,
    #             y_train_np_a,
    #             X_test_sp_matr,
    #             technique=technique_for_feat_sel,
    #             feature_names_list=feature_names_list
    #         )

    # # tr_dataset_df, test_dataset_df, categorical_features_list, \
    # #     quantitative_features_list, target_feature = \
    # #     self._build_data_structures(X_train_sp_matr, X_test_sp_matr,
    # #                                 feature_names_list, y_train_np_a,
    # #                                 y_test_np_a,
    # #                                 sparse_representation=False)

    # """Data structure helper function."""
    # sparse_representation=False
    # X_train = util.sparse_scipy_matrix_to_Pandas_df(
    #     X_train_sp_matr,
    #     sparse_representation,
    #     columns_names_list=feature_names_list)

    # X_test = util.sparse_scipy_matrix_to_Pandas_df(
    #     X_test_sp_matr,
    #     sparse_representation,
    #     columns_names_list=feature_names_list)

    # from sklearn.preprocessing import LabelEncoder
    # label_encoder = LabelEncoder()
    # le_model = label_encoder.fit(y_train_np_a)
    # y_train_np_a = le_model.transform(y_train_np_a)
    # y_test_np_a = le_model.transform(y_test_np_a)

    # print(X_train.shape)
    # print(X_test.shape)
    # print(y_train_np_a.shape)
    # print(y_test_np_a.shape)
