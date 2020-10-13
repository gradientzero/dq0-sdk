# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os
import warnings

import dq0.sdk
from dq0.privacy_checker.results_visualizer import plot_bars, select_bar_colors
from dq0.sdk.data.utils import plotting, util

from matplotlib import pyplot as plt

import numpy as np


def visualize_categorical_distributions(df_cat):
    """



    Args:
        df_cat:

    """

    for feature in df_cat.columns:

        counts_se = df_cat[feature].value_counts(normalize=True)
        bar_heights = counts_se.values
        bar_labels = counts_se.index.values.tolist()
        bar_colors = select_bar_colors(bar_heights)

        if len(bar_heights) > 5:
            x_labels_rotation_degr = 90
        else:
            x_labels_rotation_degr = 45

        plot_bars(
            bar_heights=bar_heights,
            bar_labels=bar_labels,
            bar_colors=bar_colors,
            tick_label_length_threshold_for_rotation=4,
            x_labels_rotation_degr=x_labels_rotation_degr,
            y_lim=(0, 1),
            y_label='proportion',
            color_transparency_level=.8,
            show_bar_heights=True,
            threshold=None,
            graph_title='distribution of ' + feature,
            file_with_fig=output_folder + feature + '.png'
        )


def visualize_continuous_distributions(df_quant):
    """



    Args:
        df_quant:

    """

    for feature in df_quant.columns:

        vals = df_quant[feature].values
        bool_mask = np.isnan(vals)
        num_nans = sum(bool_mask)
        if num_nans > 0:
            wrn_str = 'feature ' + feature + ' has ' + str(num_nans) +\
                      ' NaN values ignored when computing the histogram!'
            warnings.warn(wrn_str)

        # drop Nan values. Otherwise the range parameter of the histogram is
        # not finite.
        vals = vals[np.logical_not(bool_mask)]

        binning = 10  # 'auto'
        bin_heights, bin_edges = np.histogram(vals, bins=binning, density=False)

        # normalize s.t. the sum of heights is one
        bin_heights = bin_heights / bin_heights.sum()

        plot_hist(bin_edges, bin_heights,
                  x_label=feature,
                  y_label='proportion',
                  y_lim=(0, 1),
                  color_transparency_level=.8,
                  graph_title='distribution of ' + feature,
                  file_with_fig=output_folder + feature + '.png')


def plot_hist(bin_edges, bin_heights, **kwargs):
    """
    Plot a histogram. By default, the bins are coloured based on their heights.
    Coloring is based on a diverging colormap where highest bins are given
    reddish colors, while lower bins are given bluish colors.

    Args:
        bar_heights (list): heights of the bars.
        **kwargs:

    Returns:

    """

    width_factor = kwargs.get('width_factor', 1.0)  # decrease to avoid
    # overlapping edges
    bar_colors = kwargs.get('bar_colors', None)
    x_label = kwargs.get('x_label', None)
    y_label = kwargs.get('y_label', None)
    x_lim = kwargs.get('x_lim', None)
    y_lim = kwargs.get('y_lim', None)
    log_y_scale = kwargs.get('log_y_scale', False)
    graph_title = kwargs.get('graph_title', None)
    remove_grid = kwargs.get('remove_grid', True)
    file_with_fig = kwargs.get('file_with_fig', None)
    # set opacity. If set to None, colors are NOT transparent at all.
    color_transparency_level = kwargs.get('color_transparency_level', .4)

    if bar_colors is None:
        bar_colors = select_bar_colors(bin_heights)

    linewidth, markersize, figsize, fontsize, dpi = \
        plotting.get_param_configuration_for_publication_quality_plot()

    bin_width = width_factor * (bin_edges[1] - bin_edges[0])
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    plt.style.use('seaborn-darkgrid')
    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=figsize)
    ax = fig.gca()

    plt.bar(
        bin_centers, bin_heights, align='center',
        width=bin_width,
        color=bar_colors,
        alpha=color_transparency_level
        # linewidth=linewidth,
        # linestyle='-',
    )

    if x_lim is not None:
        ax.set_xlim(x_lim)

    if y_lim is not None:
        ax.set_ylim(y_lim)

    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=fontsize['axes_label'])
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=fontsize['axes_label'])
    if log_y_scale:
        plt.yscale('log')

    # plt.tick_params(axis='both', which='major', labelsize=fontsize[
    #     'major_axes_tick:'])
    # plt.tick_params(axis='both', which='minor', labelsize=fontsize[
    #     'minor_axes_tick:'])

    if remove_grid:
        plt.grid(None)  # remove grid

    if graph_title is not None:
        plt.title(graph_title, fontsize=fontsize['legend'])

    # clean up whitespace padding
    plt.tight_layout()

    if file_with_fig is not None:
        fig.savefig(file_with_fig, dpi=dpi)
    else:
        plt.show()

    # do not leave fig in RAM...
    plt.close(fig)
    # return fig


if __name__ == '__main__':

    print('\nExploratory data analysis for the "Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    # util.initialize_rnd_numbers_generators_state()

    output_folder = './output/eda/'
    util.empty_folder(output_folder)

    # path to input
    path = '../_data/adult_with_rand_names.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    data_source = dq0.sdk.data.text.CSV(filepath)

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

    # define target feature
    # target_feature = 'income'

    util.print_details_about_df_columns(dataset)

    categorical_feature_types = ['object', 'category']

    df_cat = dataset.select_dtypes(include=categorical_feature_types)
    visualize_categorical_distributions(df_cat)

    df_quant = dataset.select_dtypes(exclude=categorical_feature_types)
    visualize_continuous_distributions(df_quant)

    print('\nEDA run successfully!\n')
