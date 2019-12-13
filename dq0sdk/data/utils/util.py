# -*- coding: utf-8 -*-
"""DQ0 Data Utils.

Data util helper functions.

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle
import shutil
import sys
from logging.config import fileConfig

import numpy as np

import pandas as pd


fileConfig(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../../logging.conf'))
logger = logging.getLogger('dq0')


def print_dataset_info(df_dataset, s_title):
    """
    Prints dataset info.

    Args:
        df_dataset (df): The dataset to print
        s_title (str): The title to print
    """
    print("\n" + s_title + ". Technical info (RAM usage, etc.): ")
    df_dataset.info(memory_usage='deep')

    dims = df_dataset.shape
    print("\n", s_title, ": ")
    print("\t# of features: ", dims[1])
    print("\t# of rows: ", dims[0])
    if isinstance(df_dataset, pd.DataFrame):
        _print_feats(df_dataset.columns.values.tolist(), "features")
        print("\n\tfeatures type:")
        _print_dataframe_cols_grouped_by_type(df_dataset)

    print("\nSummary stats for numerical features:")
    print(df_dataset.describe(include=None))  # set to None for numeric
    # features only
    print("\nSummary stats for categorical features:")
    print(df_dataset.describe(include=[np.object, 'category']))


def _print_dataframe_cols_grouped_by_type(df_dataset):
    """
    Prints dataset columns grouped by type.

    Args:
        df_dataset (df): The dataset to print
    """
    grouped_cols_dict = df_dataset.columns.to_series().\
        groupby(df_dataset.dtypes).groups
    for key, value in grouped_cols_dict.items():
        print('\t' + str(key) + ':')
        for f in value:
            print('\t\t' + f)


def print_summary_stats(ts, percentiles, s_col):
    """
    Prints summary statistics

    Args:
        ts (df): test dataset to print
        percentiles: percentiles for df.describe
        s_col: column title
    """
    print('\n\nStats for', s_col, 'group: ')
    print('num null values:', ts.isnull().sum())
    print(ts.describe(percentiles=percentiles))
    print("\n\n")


def pretty_print_strings_list(l_strings, s_list_name=None):
    """
    Prints string list

    Args:
        l_strings (list): list of strings to print
        s_list_name (str): list title
    """
    if len(l_strings) > 0:
        _print_feats(l_strings, s_list_name)
    else:
        if s_list_name is not None:
            print('\n\tNo ' + s_list_name)


def _print_feats(l_column_names, s_title):
    """
    Print column names one per line.

    Args:
        l_column_names (list): list of column names to print
        s_title (str): title to print
    """
    print("\n\t\t".join((['\t' + s_title + ': '] + l_column_names)))


def print_full_df(df_dataset):
    """
    Print whole dataframe. By default, just reduced output is printed

    Args:
        df_dataset (df): dataframe to print
    """
    pd.set_option('display.max_rows', len(df_dataset))
    print(df_dataset)
    pd.reset_option('display.max_rows')


def missing_values_table(df):
    """
    Generate per feature stats about missing values
    to preview the missing values and the % of missing values in each column.

    Args:
        df: source dataframe

    Returns:
        table with missing columns
    """
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    return mis_val_table_ren_columns


def case_insensitive_str_comparison(string1, string2):
    """
    Compare strings case insensitive.

    Args:
        string1 (str): first string
        string2 (str): second string

    Returns:
        True if the strings are case insensitive equal
    """
    if string1.lower() == string2.lower():
        return True
    return False


def str_to_bool(s):
    """
    Custom cast string to bool

    Args:
        s (str): The string to convert

    Returns:
        bool: True or False

    Raises:
        ValueError: in case of unsuccesful cast.
    """
    if s.lower() in ("yes", "true", "t", "1"):
        return True
    elif s.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError


def string_contains_numeric_value(s):
    """
    Returns true if the string is a number.

    Args:
        s (str): The string to check for numbers.

    Returns:
        True if the string is convertible to float.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def redirect_stdout_stderr_streams_to_file(log_file):
    """
    Redirect stdout and stderr to file.

    Args:
        log_file (str): path to log file.

    Returns:
        log_file_stream: The log file handler
        orig_stdout: The original std out
        orig_stderr: The original std err
    """
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    log_file_stream = open(log_file, mode='w')
    sys.stdout = log_file_stream
    sys.stderr = log_file_stream

    return log_file_stream, orig_stdout, orig_stderr


def restore_stdout_stderr_streams(file_stream, orig_stdout, orig_stderr):
    """
    Reset std err and std out back to original values.

    Args:
        file_stream (file): log file to close
        orig_stdout: The original std out
        orig_stderr: The original std err
    """
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    file_stream.close()


def get_fn(file_path):
    """
    Returns the filename and extension for the given file path.

    Args:
        file_path (str): The file path to parse.

    Returns:
        just_fn (str): The filename
        ext (str): The file extension
    """
    base = os.path.basename(file_path)
    just_fn, ext = os.path.splitext(base)

    return just_fn, ext


def empty_folder(path_folder_tbr):
    """
    Deletes folder content.

    Args:
        path_folder_tbr (str): path to the folder to dump.
    """
    if os.path.exists(path_folder_tbr):
        shutil.rmtree(path_folder_tbr)
    os.makedirs(path_folder_tbr)


def move_files(l_path_files, s_dest_folder):
    """
    Move files to folder.

    Args:
        l_path_files (list): List of files to move.
        s_dest_folder (str): Path of destination directory.

    Returns:
        list: List of new file paths.
    """
    l_path_new_files = []
    try:
        for s_path_file in l_path_files:
            fn = os.path.basename(s_path_file)
            if not s_dest_folder.endswith('/'):
                s_dest_path_file = s_dest_folder + '/' + fn
            else:
                s_dest_path_file = s_dest_folder + fn
            if os.path.isfile(s_dest_path_file):
                os.remove(s_dest_path_file)
            os.rename(s_path_file, s_dest_path_file)
            l_path_new_files.append(s_dest_path_file)

        return l_path_new_files

    except Exception as e:
        sys.exit('\n\nCannot move file ' + s_path_file + ' into folder '
                 '' + s_dest_folder + '! ', e)


def list_subfloders(path='./', s_prefix=None):
    """
    List subfolders.

    Subfolder name starts with given s_prefix ('_starting_with_certain_
    name_prefix')

    Args:
        path (str): Path of the parent directory.
        s_prefix (str, optional): List only those files starting with s_prefix

    Returns:
        list: List of subdirectories.
    """
    if s_prefix is None:
        l_sf = [d for d in os.listdir(path) if os.path.isdir(d)]
    else:
        l_sf = [d for d in os.listdir(path)
                if os.path.isdir(d) and d.startswith(s_prefix)]

    return l_sf


def print_human_readable_elapsed_time_value(elapsed_cpu_time_sec, prefix):
    """
    Print elapsed cpu time in human readable format.

    Args:
        elapsed_cpu_time_sec (int): elapsed time in seconds.
        prefix (str): A prefix to print.
    """
    if elapsed_cpu_time_sec >= (60 * 60 * 24):
        elapsed_cpu_time = round(elapsed_cpu_time_sec / (60 * 60 * 24), 2)
        time_measure = 'day'
    elif elapsed_cpu_time_sec >= (60 * 60):
        elapsed_cpu_time = round(elapsed_cpu_time_sec / (60 * 60), 2)
        time_measure = 'hour'
    elif elapsed_cpu_time_sec >= 60:
        elapsed_cpu_time = round(elapsed_cpu_time_sec / 60.0)
        time_measure = 'minute'
    elif elapsed_cpu_time_sec >= 1:
        elapsed_cpu_time = round(elapsed_cpu_time_sec)
        time_measure = 'sec'
    elif elapsed_cpu_time_sec >= 1e-3:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e3)
        time_measure = 'millisec'
    elif elapsed_cpu_time_sec >= 1e-6:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e6)
        time_measure = 'microsec'
    elif elapsed_cpu_time_sec >= 1e-9:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e9)
        time_measure = 'nanosec'
    else:
        elapsed_cpu_time = elapsed_cpu_time_sec
        time_measure = 'less than one nanosec'

    if elapsed_cpu_time > 1:
        time_measure += 's'

    if time_measure != 'less than one nanosec':
        print(prefix + ' {:.2f}'.format(elapsed_cpu_time) + ' ' + time_measure)
    else:
        print(prefix + ' ' + time_measure)


def dump_model(model, path='./data/output', name='model.pickle'):
    """
    Dump a model with pickle to file.

    Args:
        model (obj): The model to dump
        path (str): directory to save to
        name (str): filename to save to
    """
    with open(os.path.join(path, name), 'wb') as f:
        pickle.dump(model, f)


def load_model_from_file(path):
    """
    Load pickled model from file.

    Args:
        path (str): Path to pickled model file

    Returns:
        unpickled model
    """
    with open(path, 'rb') as file:
        return pickle.load(file)
