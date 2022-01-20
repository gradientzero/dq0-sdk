# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.sdk.data.metadata.structure.utils.dummy_utils import DummyUtils
from dq0.sdk.data.text.csv import CSV
from dq0.sdk.data.utils import plotting, util


def preprocess_dataset(data_source):

    column_names_list = [
        'lastname',
        'firstname',
        'age',
        'workclass',
        'fnlwgt',
        'education',
        'education-num',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'capital-gain',
        'capital-loss',
        'hours-per-week',
        'native-country',
        'income'
    ]

    # read the data via the attached input data source
    dataset = data_source.read(
        names=column_names_list,
        sep=',',
        skiprows=1,
        index_col=None,
        skipinitialspace=True,
        na_values={
            'capital-gain': 99999,
            'capital-loss': 99999,
            'hours-per-week': 99,
            'workclass': '?',
            'native-country': '?',
            'occupation': '?'}
    )

    # drop unused columns
    dataset.drop(['lastname', 'firstname'], axis=1, inplace=True)
    column_names_list.remove('lastname')
    column_names_list.remove('firstname')

    return dataset


def eda(dataset, output_folder):
    """
    Perform exploratory data analysis over the input dataset

    Args:
        dataset (pandas.DataFrame): dataset to be investigated

    """

    print('\nExploratory data analysis (EDA)\n')

    util.print_details_about_df_columns(dataset)
    print('\n')

    categorical_feature_types = ['object', 'category']

    df_cat = dataset.select_dtypes(include=categorical_feature_types)
    for feature in df_cat.columns:
        plotting.visualize_categorical_distribution(df_cat[feature],
                                                    output_folder)

    df_quant = dataset.select_dtypes(exclude=categorical_feature_types)
    for feature in df_quant.columns:
        plotting.visualize_continuous_distribution(df_quant[feature],
                                                   output_folder)

    print('\nEDA run successfully!\n')


def visualize_filtered_data(series, conditions, output_folder):
    """

    Args:
        series (pandas.Series): data
        conditions (tuple): (lb, ub)
        output_folder (str): path to output folder

    """

    # boolean filters
    filter_lb = series >= conditions[0]
    filter_ub = series <= conditions[1]

    # filtering data on basis of filters
    series_filt = series.loc[filter_lb & filter_ub]

    if series_filt.dtype == 'object':
        plotting.visualize_categorical_distribution(
            series_filt, output_folder, fn_suffix='_filtered'
        )
    else:
        plotting.visualize_continuous_distribution(
            series_filt, output_folder,
            binning=10, fn_suffix='_filtered',
            graph_title='distribution of ' + series.name + ' in '
                        '[' + str(conditions[0]) + ',' + str(
                            conditions[1]) + ']'
        )


if __name__ == '__main__':

    # set seed of random number generator to ensure reproducibility of results
    # util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '_data/adult_with_rand_names.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    data_source = CSV(DummyUtils.dummy_meta_database_for_csv(filepath=filepath))

    dataset = preprocess_dataset(data_source)

    output_folder = './output/eda/'
    util.empty_folder(output_folder)

    eda(dataset, output_folder)

    cols = ['age']
    conditions = [(30, 50)]  # list of conditions, one tuple per column
    for counter, feature in enumerate(cols):
        visualize_filtered_data(dataset[feature], conditions[counter],
                                output_folder)
