# -*- coding: utf-8 -*-

"""
@author: Paolo Campigotto
"""

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import seaborn as sns

from sklearn import metrics, tree
from sklearn.utils.multiclass import unique_labels


def plot_confusion_matrix_for_scikit_classifier(
    classifier,
    X_test_np_a,
    y_test_np_a,
    class_names=None,
    xticks_rotation='horizontal',  # 'vertical', 'horizontal', float
    part_of_fn_describing_matrix='',
    output_folder='../data/output/'
):
    #
    # classifier must be a Scikit trained classifier! E.g., after creating the
    # classifier object, its fit() method had been invoked.
    #
    # class_names = None  # list of labels to index the confusion matrix. This
    # may be used to reorder or select a subset of labels. If None is given,
    # those that appear at least once in y_true or y_pred are used in sorted
    # order.
    # To get the labels:
    #      class_names = sklearn.utils.multiclass.unique_labels(y_true)
    # To use only the labels that appear in the data:
    #      class_names = sklearn.utils.multiclass.unique_labels(y_true, y_pred)
    #
    # xticks_rotation can be 'horizontal', 'vertical' or float
    #

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

    if part_of_fn_describing_matrix != '':
        if not part_of_fn_describing_matrix.startswith('_for_'):
            part_of_fn_describing_matrix = '_for_' + \
                                           part_of_fn_describing_matrix
    file_path = output_folder + title.replace(' ', '_') + \
        part_of_fn_describing_matrix + '.png'
    plt.savefig(file_path, bbox_inches='tight', dpi=200)

    return file_path


def plot_confusion_matrix(y_true, y_pred, output_folder,
                          xticks_rotation='horizontal',
                          cmap=plt.cm.Blues,
                          part_of_fn_describing_matrix=''):
    """
    Print and plot the confusion matrix

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
        sns.heatmap(cm, ax=ax, annot=True, cbar=True, fmt=fmt, cmap=cmap)
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
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                     rotation_mode="anchor")

        fig.tight_layout()

        file_path = _save_plotted_cm(part_of_fn_describing_matrix, title,
                                     output_folder)
        plt.close(fig)
        print('\n' + title + ' saved in file ' + file_path)


def compute_confusion_matrix(y_true, y_pred, normalize):

    # only use the labels that appear in the data
    labels_list = list(unique_labels(list(y_true) + list(y_pred)))
    # or u can also use np.unique()
    cm = metrics.confusion_matrix(y_true, y_pred, labels_list)
    # Pass the labels list to the confusion_matrix function in order to
    # index the confusion matrix based on the order of labels in the list.
    # Using labels_list ensures that the confusion matrix matches the ticks in
    # the figure plotting it.
    #
    # From Scikit documentation:
    #       labels: array-like of shape (n_classes), default=None
    #               List of labels to index the matrix.
    #               This may be used to reorder or select a subset of
    #               labels. If None is given, those that appear at least
    #               once in y_true or y_pred are used in sorted order.
    #

    if normalize:
        # cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        # cm = np.round(cm, 2)
        cm_sum = np.sum(cm, axis=1, keepdims=True)
        cm = np.round(cm / cm_sum.astype(float), 2)
        # cm_perc = cm * 100

    cm_df = pd.DataFrame(cm, index=labels_list, columns=labels_list)
    # print(cm_df)

    return cm_df, labels_list


def scatterplot(x, y, working_folder='../data/working/', hue=None,
                part_of_fn_describing_data=''):

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

    fig = plt.figure()
    tree.plot_tree(dec_tree)
    file_path = folder + 'Learned_decision_tree_attack_model.png'
    plt.savefig(file_path, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print('\nLearned decision-tree attack-model saved in file ' + file_path)
