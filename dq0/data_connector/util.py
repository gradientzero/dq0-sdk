# =============================================================================
# =                                 Utils                                     =
# =============================================================================

import os
import shutil
import sys
import configparser
import random
import pickle

import numpy as np
import pandas as pd

#
# sys.exit("some error message") is a quick way to exit a program when an error
# occurs. It results in an exit code of 1 and the error message in written
# in sys.stderr. sys.exit() is equivalent to passing zero,
# and any other object is printed to sys.stderr.
#


def print_dataset_info(df_dataset, s_title):

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
    grouped_cols_dict = df_dataset.columns.to_series().groupby(df_dataset.dtypes).groups
    for key, value in grouped_cols_dict.items():
        print('\t' + str(key) + ':')
        for f in value:
            print('\t\t' + f)


def print_summary_stats(ts, percentiles, s_col):

    print('\n\nStats for', s_col, 'group: ')
    print('num null values:', ts.isnull().sum())
    print(ts.describe(percentiles=percentiles))
    print("\n\n")


def pretty_print_strings_list(l_strings, s_list_name=None):

    if len(l_strings) > 0:
        _print_feats(l_strings, s_list_name)
    else:
        if s_list_name is not None:
            print('\n\tNo ' + s_list_name)


def _print_feats(l_column_names, s_title):
    # print column names one per line
    print("\n\t\t".join((['\t' + s_title + ': '] + l_column_names)))


def print_full_df(df_dataset):
    #
    # Print whole dataframe. By default, just reduced output is printed
    #
    pd.set_option('display.max_rows', len(df_dataset))
    print(df_dataset)
    pd.reset_option('display.max_rows')


def missing_values_table(df):
    #
    # generate per feature stats about missing values
    # to preview the missing values and the % of missing values in each column
    #
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    return mis_val_table_ren_columns


def case_insensitive_str_comparison(string1, string2):
    if string1.lower() == string2.lower():
        res = True
    else:
        res = False

    return res


def str_to_bool(s):
    if s.lower() in ("yes", "true", "t", "1"):
        return True
    elif s.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError  # evil ValueError that doesn't tell you what the
        # wrong value was


def string_contains_numeric_value(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def redirect_stdout_stderr_streams_to_file(log_file):

    # redirect stdout and stderr to file
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    log_file_stream = open(log_file, mode='w')
    sys.stdout = log_file_stream
    sys.stderr = log_file_stream

    return log_file_stream, orig_stdout, orig_stderr


def restore_stdout_stderr_streams(file_stream, orig_stdout, orig_stderr):

    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    file_stream.close()


def get_fn(file_path):
    base = os.path.basename(file_path)
    just_fn, ext = os.path.splitext(base)

    return just_fn, ext


def empty_folder(path_folder_tbr):
    if os.path.exists(path_folder_tbr):
        shutil.rmtree(path_folder_tbr)
    os.makedirs(path_folder_tbr)


def move_files(l_path_files, s_dest_folder):

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
        sys.exit('\n\nCannot move file ' + s_path_file + ' into folder ' +
                 s_dest_folder + '! ', e)


def list_subfloders(path='./', s_prefix=None):
    #
    # Subfolder name starts with given s_prefix ('_starting_with_certain_
    # name_prefix')
    #

    if s_prefix is None:
        l_sf = [d for d in os.listdir(path) if os.path.isdir(d)]
    else:
        l_sf = [d for d in os.listdir(path) if os.path.isdir(d) and
                d.startswith(s_prefix)]

    return l_sf


def print_human_readable_elapsed_time_value(elapsed_cpu_time_sec, s_tmp):

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
        print(s_tmp + ' {:.2f}'.format(elapsed_cpu_time) + ' ' + time_measure)
    else:
        print(s_tmp + ' ' + time_measure)


def dump_model(model, path='./data/output', name='model.pickle'):
    with open(os.path.join(path, name), 'wb') as f:
        pickle.dump(model, f)


def load_model_from_file(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
