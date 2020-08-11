# -*- coding: utf-8 -*-
"""Helper functions for plotting data analysis results.

Copyright 2020, Gradient Zero
All rights reserved
"""
import logging

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import seaborn as sns

from sklearn import metrics, tree
from sklearn.utils.multiclass import unique_labels


logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("pyplot").setLevel(logging.WARNING)
logging.getLogger("seaborn").setLevel(logging.WARNING)

def plot_confusion_matrix_for_scikit_classifier(classifier,
                                                X_test_np_a,
                                                y_test_np_a,
                                                class_names=None,
                                                xticks_rotation='horizontal',  # 'vertical', 'horizontal', float
                                                part_of_fn_describing_matrix='',
                                                output_folder='../data/output/'):
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
        output_folder (:obj:`str`): Path to the output folder for the matrix png image.
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


if __name__ == '__main__':
    _debug_cm_plot()
