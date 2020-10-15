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

import numpy as np

import pandas as pd

from sklearn.datasets import fetch_20newsgroups


def _dump_text_and_labels_to_csv(
        csv_path='dq0/sdk/examples/newsgroups/_data/20newsgroups_text_label_df.csv'
):

    train, test = _fetch_data()

    dataset = _make_df(train, test)

    dataset.to_csv(csv_path, index=False)


def _fetch_data():

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

    return train, test


def _make_df(train, test):

    X_train = train.data  # list of text documents
    X_test = test.data
    y_train_np_a, y_test_np_a = train.target, test.target

    X = X_train + X_test
    y = np.hstack([y_train_np_a, y_test_np_a])

    dataset = pd.DataFrame(X, columns=['text'])
    dataset['label'] = y

    return dataset


if __name__ == '__main__':

    _dump_text_and_labels_to_csv()
