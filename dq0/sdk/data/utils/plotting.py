# -*- coding: utf-8 -*-
"""Helper functions for plotting data analysis results.

Copyright 2020, Gradient Zero
All rights reserved
"""
import logging
import warnings

from dq0.sdk.data.utils import util

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import seaborn as sns

from sklearn import metrics, tree
from sklearn.utils.multiclass import unique_labels


logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("pyplot").setLevel(logging.WARNING)
logging.getLogger("seaborn").setLevel(logging.WARNING)


def plot_confusion_matrix_for_scikit_classifier(
    classifier,
    X_test_np_a,
    y_test_np_a,
    class_names=None,
    xticks_rotation='horizontal',  # 'vertical', 'horizontal', float
    part_of_fn_describing_matrix='',
    output_folder='../data/output/'
):
    """Plots a confusion matrix for the scikit classifier.

    Args:
        classifier: a Scikit trained classifier! E.g., after creating the
            classifier object, its fit() method had been invoked.
        X_test_np_a (:obj:`numpy.ndarray`): X test data
        y_test_np_a (:obj:`numpy.ndarray`): y test data
        class_names (:obj:`list`): optional list of labels to index the confusion matrix.
            This may be used to reorder or select a subset of labels. If None is given,
            those that appear at least once in y_true or y_pred are used in sorted order.
            To get the labels:
                class_names = sklearn.utils.multiclass.unique_labels(y_true)
            To use only the labels that appear in the data:
                class_names = sklearn.utils.multiclass.unique_labels(y_true, y_pred)
        xticks_rotation: can be 'horizontal', 'vertical' or float
        part_of_fn_describing_matrix (:obj:`str`): function description for matrix.
        output_folder (:obj:`str`): Path to the output folder for the matrix png image.
    """
    titles_options = [('Confusion matrix', None),
                      ('Normalized confusion matrix', 'true')]
    for title, normalize in titles_options:

        fig = plt.figure()
        disp = metrics.plot_confusion_matrix(classifier, X_test_np_a,
                                             y_test_np_a,
                                             display_labels=class_names,
                                             cmap=plt.cm.Blues,
                                             normalize=normalize,
                                             xticks_rotation=xticks_rotation
                                             # 'vertical', 'horizontal', float
                                             )
        disp.ax_.set_title(title)
        plt.tight_layout()

        file_path = _save_plotted_cm(part_of_fn_describing_matrix, title,
                                     output_folder)
        plt.close(fig)
        print('\n' + title + ' saved in file ' + file_path)


def _save_plotted_cm(part_of_fn_describing_matrix, title, output_folder):
    """Saves the confusion matrix as PNG image.

    Args:
        part_of_fn_describing_matrix (:obj:`str`): File part description
        title (:obj:`str`): Title of the matrix
        output_folder (:obj:`str`): Path to the output folder for the matrix
            png image.
    """
    if part_of_fn_describing_matrix != '':
        if not part_of_fn_describing_matrix.startswith('_for_'):
            part_of_fn_describing_matrix = '_for_' + \
                                           part_of_fn_describing_matrix
    file_path = output_folder + title.replace(' ', '_') + \
        part_of_fn_describing_matrix + '.png'
    plt.savefig(file_path, bbox_inches='tight', dpi=200)

    return file_path


def plot_confusion_matrix(y_true,
                          y_pred,
                          output_folder,
                          xticks_rotation='horizontal',
                          cmap=plt.cm.Blues,
                          part_of_fn_describing_matrix=''):
    """Print and plot the confusion matrix.

    Args:
        y_true (:obj:`numpy.ndarray`): target y values.
        y_pred (:obj:`numpy.ndarray`): predicted y values.
        output_folder (:obj:`str`): Path to the output folder for the matrix png image.
        xticks_rotation: can be 'horizontal', 'vertical' or float
        cmap: Matplotlib color map.
        part_of_fn_describing_matrix (:obj:`str`): function description for matrix.
    """
    titles_options = [('Confusion matrix', None),
                      ('Normalized confusion matrix', 'true')]
    for title, normalize in titles_options:

        cm, labels_list = compute_confusion_matrix(y_true, y_pred, normalize)
        # print(cm)

        if normalize:
            fmt = '.2f'
        else:
            fmt = 'd'

        fig, ax = plt.subplots()
        # cmap='Greens'
        if len(labels_list) > 10:
            annot_kws = {'size': 6}  # reduce font size to avoid cluttering
            xticks_rotation = '45'  # must be a string due to below call of
            # "lower()"
        else:
            annot_kws = None
        sns.heatmap(cm, ax=ax, annot=True, cbar=True, fmt=fmt, cmap=cmap,
                    annot_kws=annot_kws)
        # annot=True to annotate cells
        # cbar=True to show vertical bar acting as a color legend
        # annot_kws = {"size": 16})# font size
        # sns.set(font_scale=1.4)#for label size
        #

        # labels, title and ticks
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('Actual labels')
        ax.set_title(title)
        ax.xaxis.set_ticklabels(labels_list)
        ax.yaxis.set_ticklabels(labels_list)

        ax.grid(False)

        # rotate the tick labels and set their alignment
        if xticks_rotation.lower() != 'horizontal'.lower():
            for c_ax in [ax.get_xticklabels(), ax.get_yticklabels()]:
                plt.setp(c_ax, rotation=45, ha="right", rotation_mode="anchor")

        fig.tight_layout()

        file_path = _save_plotted_cm(part_of_fn_describing_matrix, title,
                                     output_folder)
        plt.close(fig)
        print('\n' + title + ' saved in file ' + file_path)


def compute_confusion_matrix(y_true, y_pred, normalize):
    """Computes the confusion matrix.

    Pass the labels list to the confusion_matrix function in order to
    index the confusion matrix based on the order of labels in the list.
    Using labels_list ensures that the confusion matrix matches the ticks in
    the figure plotting it.

    From Scikit documentation:
        labels: array-like of shape (n_classes), default=None
        List of labels to index the matrix.
        This may be used to reorder or select a subset of
        labels. If None is given, those that appear at least
        once in y_true or y_pred are used in sorted order.

    Args:
        y_true (:obj:`numpy.ndarray`): target y values.
        y_pred (:obj:`numpy.ndarray`): predicted y values.
        normalize (bool): True to normalize the matrix.
    """
    # Only use the labels that appear in the data:
    labels_list = list(unique_labels(list(y_true) + list(y_pred)))

    # Or u can also use np.unique()
    cm = metrics.confusion_matrix(y_true, y_pred, labels_list)

    if normalize:
        # cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        # cm = np.round(cm, 2)
        cm_sum = np.sum(cm, axis=1, keepdims=True)
        cm = np.round(cm / cm_sum.astype(float), 2)
        # cm_perc = cm * 100

    cm_df = pd.DataFrame(cm, index=labels_list, columns=labels_list)
    # print(cm_df)

    return cm_df, labels_list


def scatterplot(x,
                y,
                working_folder='../data/working/',
                hue=None,
                part_of_fn_describing_data=''):
    """Plots a scatterplot graph with seaborn.

    Args:
        x: names of x variables in data or vector data
        y: names of y variables in data or vector data
        working_folder (:obj:`str`): working directory
        hue: Grouping variable that will produce points with different colors
        part_of_fn_describing_data (:obj:`str`): function description for plot.
    """
    fig = plt.figure()
    sns.set(style="white")
    sns.scatterplot(x=x,
                    y=y,
                    hue=hue,
                    alpha=.5,
                    palette="muted"
                    )
    plt.tight_layout()

    file_name = 'Scatterplot'
    if part_of_fn_describing_data != '':
        file_name += '_of_' + part_of_fn_describing_data.replace(' ', '_')

    file_path = working_folder + file_name + '.png'
    plt.savefig(file_path, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print('\n' + file_name.replace('_', ' ') + ' saved in file ' + file_path)


def plot_decision_tree(dec_tree, folder):
    """Plot scikit-learn decision tree.

    Args:
        dec_tree: The decision tree to plot.
        folder (:obj:`str`): Folder to save the figure to.
    """
    fig = plt.figure()
    tree.plot_tree(dec_tree)
    file_path = folder + 'Learned_decision_tree_attack_model.png'
    plt.savefig(file_path, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print('\nLearned decision-tree attack-model saved in file ' + file_path)


def _debug_cm_plot():
    """Helper funtion to test the plotting utils."""
    import random

    num_preds = 50000
    l1 = [random.randint(0, 20) for i in range(num_preds)]
    l2 = [random.randint(0, 20) for i in range(num_preds)]
    plot_confusion_matrix(l1, l2, './')


def add_shared_axis_labels(fig, x_label, y_label, font_size=15):
    """
    Add label to x and y axes shared by the subplots in the figure
    referred to by the input "fig" handle.

    Input "fig" handle is assumed to be generated by, e.g:
        fig, ax = plt.subplots(nrows=...,
                               ncols=...,
                               sharex=True,
                               sharey=True
                               )

    Args:
        fig: multi-plots figure handle
        x_label: string with label for shared x-axis
        y_label: string with label for shared y-axis
        font_size: size of font for axes labels
    """

    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False,
                    left=False, right=False)

    plt.ylabel(y_label, fontsize=font_size)
    plt.xlabel(x_label, fontsize=font_size)


def get_param_configuration_for_publication_quality_plot():
    """
    Set matplotlib.pyplot parameters for publication-quality plot

    Returns:
        linewidth, markersize, figsize, fontsize
    """

    linewidth = 3
    markersize = 7
    figsize = (8, 4)

    fontsize = {'axes_label': 15,
                'major_axes_tick:': 13,
                'minor_axes_tick:': 12,
                'legend': 13
                }

    #
    # Together with size, controlling the output image resolution gives you
    # control over the quality of the final product.
    #
    # fig.savefig("image_filename.png", dpi=150)
    #
    # You can specify the dpi, dots per inch, in the call to savefig().
    # For printing and most screens, 150 is pretty good, 300 is clear,
    # and 600 is spectacular. 1200 or higher can come in handy if you want
    # to be able to do a lot of zooming in, but your image can start to get
    # very big on disk at that resolution.
    dpi = 300

    return linewidth, markersize, figsize, fontsize, dpi


def select_bar_colors(bar_heights, evenly_spaced_interval=False):
    """
    Define a color for each bar in a bar-plot.

    Args:
        bar_heights (np.ndarray): list of heights of the bars. Order
            matters: bar_heights[0] refers to the height of the leftmost bar.
        evenly_spaced_interval (bool): Boolean flag. If False, bar coloring
            based on height of bins. If true, bar coloring by order of the
            bins: the selected colors are equally spaced in the color map.
            The latter option may be useful if the bins are ordered by their
            height and the color map is sequential or diverging.

    Returns:
        list of colors
    """

    # color_map = plt.cm.get_cmap('GnBu')
    color_map = plt.cm.get_cmap('RdYlBu_r')
    # to get a color, call the colormap with a value between 0 and 1
    if evenly_spaced_interval:
        # coloring by order of the bins (useful if bins are ordered,
        # e.g., from highest to lowest)
        selected_colors = np.linspace(0, 1, len(bar_heights))
    else:
        # coloring by height of the bins
        # scale bar heights into [0, 1]
        selected_colors = (bar_heights - bar_heights.min()) / \
                          (bar_heights.max() - bar_heights.min())

    # colormap maps numbers to colors in a 1-D array of (e.g., RGB) colors.
    bar_colors = [color_map(x) for x in selected_colors]

    return bar_colors


def plot_bars(bar_heights, **kwargs):  # noqa: C901
    """
    Generate a bar plot.

    Args:
        bar_heights (list): heights of the bars.
        **kwargs:

    Returns:

    """

    bar_locations = kwargs.get('bar_locations', None)
    bar_width = kwargs.get('bar_width', 1.0)
    bar_labels = kwargs.get('bar_labels', None)
    bar_colors = kwargs.get('bar_colors', None)
    x_label = kwargs.get('x_label', None)
    y_label = kwargs.get('y_label', None)
    tick_label_length_threshold_for_rotation = kwargs.get(
        'tick_label_length_threshold_for_rotation', None)
    x_labels_rotation_degr = kwargs.get('x_labels_rotation_degr', 45)
    x_lim = kwargs.get('x_lim', None)
    y_lim = kwargs.get('y_lim', None)
    log_y_scale = kwargs.get('log_y_scale', False)
    graph_title = kwargs.get('graph_title', None)
    show_legend = kwargs.get('show_legend', False)

    num_bars = len(bar_heights)
    show_bar_heights = False if num_bars > 20 else kwargs.get(
        'show_bar_heights', False)  # if too many bars, forced to False to
    # avoid cluttering

    threshold = kwargs.get('threshold', None)
    remove_grid = kwargs.get('remove_grid', True)
    file_with_fig = kwargs.get('file_with_fig', None)

    linewidth, markersize, figsize, fontsize, dpi = \
        get_param_configuration_for_publication_quality_plot()
    # set opacity. If set to None, colors are NOT transparent at all.
    color_transparency_level = kwargs.get('color_transparency_level', .4)

    plt.style.use('seaborn-darkgrid')

    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=figsize)
    ax = fig.gca()

    if bar_locations is None and bar_width == 1.0:
        bar_locations = np.arange(num_bars)

    tmp = bar_width
    bar_width *= 0.9  # avoid overlapping edges

    # set a margin to avoid that right (left) edge of last (first) bar
    # overlaps with figure edge
    bar_edge_to_fig_edge_margin = tmp - bar_width

    # alignment of the bars to the x coordinates: bars are centered on the
    # "bar_locations" values
    rects = ax.bar(
        bar_locations,
        bar_heights,
        width=bar_width,
        # label='',
        color=bar_colors,
        linewidth=linewidth,
        linestyle='-',
        alpha=color_transparency_level
    )

    if threshold is not None:
        # plot horizontal line y = threshold value
        plt.axhline(y=threshold,
                    linestyle='--', color='k',
                    linewidth=linewidth - 2,
                    label='decision threshold',
                    alpha=color_transparency_level)
        show_legend = True

    if x_lim is not None:
        ax.set_xlim(x_lim)
    else:
        xlb = bar_locations[0] - bar_width * .5 - bar_edge_to_fig_edge_margin
        xub = bar_locations[-1] + bar_width * .5 + bar_edge_to_fig_edge_margin
        ax.set_xlim(xlb, xub)
    if y_lim is not None:
        ax.set_ylim(y_lim)

    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=fontsize['axes_label'])
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=fontsize['axes_label'])
    if log_y_scale:
        plt.yscale('log')

    plt.tick_params(axis='both', which='major', labelsize=fontsize[
        'major_axes_tick:'])
    plt.tick_params(axis='both', which='minor', labelsize=fontsize[
        'minor_axes_tick:'])
    ax.set_xticks(bar_locations)
    if bar_labels is not None:

        rotation = None
        if tick_label_length_threshold_for_rotation is not None:
            max_length = max([len(x) for x in bar_labels])
            if max_length >= tick_label_length_threshold_for_rotation:
                rotation = x_labels_rotation_degr

        ax.set_xticklabels(bar_labels, rotation=rotation)

    if show_legend:
        # handles with labels to put in legend must have been defined above
        # (by, e.g., setting "label=..." in each plot command)
        #
        # loc='upper right', loc='upper center'
        #
        ax.legend(loc='best', ncol=2, fontsize=fontsize['legend'])

    if remove_grid:
        plt.grid(None)  # remove grid

    if graph_title is not None:
        plt.title(graph_title, fontsize=fontsize['legend'])

    if show_bar_heights:
        _autolabel(rects, ax, fontsize=fontsize['major_axes_tick:'])

    # clean up whitespace padding
    plt.tight_layout()

    if file_with_fig is not None:
        fig.savefig(file_with_fig, dpi=dpi)
    else:
        plt.show()

    # do not leave fig in RAM...
    plt.close(fig)
    # return fig


def _autolabel(rects, ax, **kwargs):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    Args:
        rects: heights of the bar
        ax: Matplotlib Axes object where labels will be generated.
    """

    fontsize = kwargs.get('fontsize', None)
    number_decimals = kwargs.get('number_decimals', 2)

    for rect in rects:
        height = rect.get_height()

        height_str = util.format_float_lower_than_1(
            round(height, number_decimals)
        )

        ax.annotate(height_str,  # '{}'.format(height)
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=fontsize)


def plot_hist(bin_edges, bin_heights, **kwargs):
    """
    Plot a histogram. By default, the bins are coloured based on their heights.
    Coloring is based on a diverging colormap where highest bins are given
    reddish colors, while lower bins are given bluish colors.

    Args:
        bin_edges (list): edges of the bins. List lengths is number of bins
            plus one.
        bin_heights (list): heights of the bins.
        **kwargs:

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
        get_param_configuration_for_publication_quality_plot()

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

    plt.tick_params(axis='both', which='major', labelsize=fontsize[
        'major_axes_tick:'])
    plt.tick_params(axis='both', which='minor', labelsize=fontsize[
        'minor_axes_tick:'])

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


def visualize_categorical_distribution(series, output_folder, **kwargs):
    """
    Show the proportion of observations in each category using bars. Basically,
    it visualizes the discrete distribution of the data and the resulting
    plot can be interpreted as an histogram across a categorical, instead of
    quantitative, variable.


    Args:
        series (pandas.Series): categorical (aka discrete) data to be
            visualized.
        output_folder: path to folder where the generated figure will be
            saved.
    """

    fn_suffix = kwargs.get('fn_suffix', '')

    counts_se = series.value_counts(normalize=True)
    bar_heights = counts_se.values
    bar_labels = counts_se.index.values.tolist()
    bar_colors = select_bar_colors(bar_heights)

    if len(bar_heights) > 6:
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
        graph_title='distribution of ' + series.name,
        file_with_fig=output_folder + series.name + fn_suffix + '.png'
    )


def visualize_continuous_distribution(series, output_folder, **kwargs):
    """
    Generate univariate histogram showing the data distribution.
    Histogram bars show the proportions of observations falling in each
    bin.

    Args:
        series (pandas.Series): quantitative data to be visualized.
        output_folder: path to folder where the generated figure will be
            saved.
    """

    fn_suffix = kwargs.get('fn_suffix', '')
    binning = kwargs.get('binning', 10)  # 'auto'
    graph_title = kwargs.get('graph_title', 'distribution of ' + series.name)

    vals = series.values
    bool_mask = np.isnan(vals)
    num_nans = sum(bool_mask)
    if num_nans > 0:
        wrn_str = 'feature ' + series.name + ' has ' + str(num_nans) +\
                  ' NaN values ignored when computing the histogram!'
        warnings.warn(wrn_str)

    # drop Nan values. Otherwise the range parameter of the histogram is
    # not finite.
    vals = vals[np.logical_not(bool_mask)]

    bin_heights, bin_edges = np.histogram(vals, bins=binning, density=False)

    # normalize s.t. the sum of heights is one
    bin_heights = bin_heights / bin_heights.sum()

    plot_hist(bin_edges, bin_heights,
              x_label=series.name,
              y_label='proportion',
              y_lim=(0, 1),
              color_transparency_level=.8,
              graph_title=graph_title,
              file_with_fig=output_folder + series.name + fn_suffix + '.png')


if __name__ == '__main__':
    _debug_cm_plot()
