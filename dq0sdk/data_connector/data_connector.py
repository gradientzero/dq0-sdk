#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Wolfgang Gross <wg@gradient0.com>
"""
import pandas as pd
import os
import sklearn
from dq0sdk.data_connector import preprocessing, util


class Data_Connector_Adult:

    def __init__(self):
        pass

    #def read_data(self, path='data/adult/'):
    #    """DQ0 Data connector."""
    #    data_path = os.path.join(path,'adult.data')
    #    test_path = os.path.join(path,'adult.test')
    #    columns_names = ['age','workclass','fnlwgt','education','education-num','marital-status','occupation',
    #                'relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country']

    #    adult_data = pd.read_csv(data_path, names=columns_names + ['income'])
    #    adult_test = pd.read_csv(test_path, names=columns_names)
    #    adult_test = adult_test.drop(0, axis=0) # first line contains unvalid data

    #    self.adult_data = adult_data
    #    self.adult_test = adult_test

    #    return self.adult_data, self.adult_test

    def load_input_dataset(self, dataset_file_path, skiprows=None):
        #print('Load dataset from file "' + dataset_file_path + '" ')

        column_names_list = [
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

        # categorical_features_list = [
        #    'workclass',
        #    'fnlwgt',
        #    'education',
        #    'education-num',
        #    'marital-status',
        #    'occupation',
        #    'relationship',
        #    'race',
        #    'sex',
        #    'native-country'
        # ]

        target_feature = 'income'

        # List difference. Warning: in below operation, set does not preserve the
        # order. If order matters, use, e.g., list comprehension.
        # quantitative_features_list = list(set(column_names_list) -
        #                                  set(categorical_features_list) -
        #                                  set([target_feature]))

        # To speed up load of data in RAM and to optimize memory consumption. Not
        # really sensible effect if dataset size is limited.
        # columns_dtype_dict = {
        #                    'age': np.uint8,
        #                    'workclass': object,
        #                    'fnlwgt': np.uint32,
        #                    'education': object,
        #                    'education-num': np.uint8,
        #                    'marital-status': object,
        #                    'occupation': object,
        #                    'relationship': object,
        #                    'race': object,
        #                    'sex': object,
        #                    'capital-gain': np.uint32,
        #                    'capital-loss': np.uint32,
        #                    'hours-per-week': np.uint8,
        #                    'native-country': object,
        #                    'income': object
        #                    }

        # Let Python decide for column types, since they may be missing values.
        dataset_df = pd.read_csv(dataset_file_path,
                                 names=column_names_list,
                                 sep=',',
                                 # false_values=['f', 'false'],
                                 # true_values=['t', 'true'],
                                 # dtype=columns_dtype_dict,
                                 skiprows=skiprows,
                                 index_col=None,
                                 # comment='|',  # test dataset has comment in it
                                 # comment is in the first row only. Ignored by
                                 # setting parameter "skiprows"
                                 skipinitialspace=True,  # skip spaces after
                                 # delimiter
                                 na_values={
                                     'capital-gain': 99999,
                                     'capital-loss': 99999,
                                     'hours-per-week': 99,
                                     'workclass': '?',
                                     'native-country': '?',
                                     'occupation': '?'
                                 }
                                 # missing values in categorical features are
                                 # encoded via '?'.
                                 )

        categorical_features_list = [column for column in dataset_df.columns
                                     if column != target_feature and
                                     dataset_df[column].dtype == 'object']

        # List difference. Warning: in below operation, set does not preserve the
        # order. If order matters, use, e.g., list comprehension.
        quantitative_features_list = list(set(column_names_list) -
                                          set(categorical_features_list) -
                                          set([target_feature]))

        self.dataset_df = dataset_df

        return dataset_df, categorical_features_list, \
               quantitative_features_list, target_feature

    def read_data(self, input_folder):


        # csv file
        training_dataset_path = input_folder + 'adult.data'
        # csv file
        test_dataset_path = input_folder + 'adult.test'
        tr_dataset_df, _, _, _ = self.load_input_dataset(training_dataset_path)
        # Load test data skipping the bad row in the test data.
        test_dataset_df, categorical_features_list, \
        quantitative_features_list, target_feature = \
            self.load_input_dataset(test_dataset_path, skiprows=1)

        return tr_dataset_df, test_dataset_df, categorical_features_list, \
               quantitative_features_list, target_feature


    def preprocess_dataset(self, tr_dataset_df, test_dataset_df,
                           categorical_features_list, quantitative_features_list, target_feature,
                           approach_for_missing_feature='imputation',  # 'imputation', 'dropping',
                           imputation_method_for_cat_feats='unknown',  # 'unknown', 'most_common_cat'
                           imputation_method_for_quant_feats='median',  # 'median', 'mean'
                           features_to_drop_list=None):

        tr_dataset_df = preprocessing._handle_missing_data(tr_dataset_df, mode=approach_for_missing_feature,
                                                           imputation_method_for_cat_feats=imputation_method_for_cat_feats,
                                                           imputation_method_for_quant_feats=imputation_method_for_quant_feats,
                                                           categorical_features_list=categorical_features_list,
                                                           quantitative_features_list=quantitative_features_list)

        test_dataset_df = preprocessing._handle_missing_data(test_dataset_df,
                                               mode=approach_for_missing_feature,
                                               imputation_method_for_cat_feats=imputation_method_for_cat_feats,
                                               imputation_method_for_quant_feats=imputation_method_for_quant_feats,
                                               categorical_features_list=categorical_features_list,
                                               quantitative_features_list=quantitative_features_list)

        num_tr_instances, _ = tr_dataset_df.shape
        num_test_instances, _ = test_dataset_df.shape

        X_train_df = tr_dataset_df.drop(target_feature, axis=1)
        X_test_df = test_dataset_df.drop(target_feature, axis=1)

        # full dataset
        X_df = X_train_df.append(X_test_df)
        y_ts = tr_dataset_df[target_feature].append(test_dataset_df[target_feature])

        # cleanup (test) labels: strip trailing '.' (by visual inspection on
        # sampled data, it should appear only in the test labels. For safety,
        # parse training labels, too.)
        y_ts = y_ts.apply(lambda label: label.rstrip("."))

        # util.print_dataset_info(X_df, 'Raw full dataset without target_feature')

        if features_to_drop_list is not None:
            X_df.drop(features_to_drop_list, axis=1, inplace=True)
            util.pretty_print_strings_list(
                features_to_drop_list,
                '\nThe following uninformative features (given the remaining '
                'ones)  have been dropped:')

        print('\nConvert categorical features to numerical representations by '
              'one-hot encoding')
        # TODO: investigate whether ordinal features are present
        #
        # (Weak) assumption: for each categorical feature, its values in the
        # test set is already present in the training set.
        #
        X_df = pd.get_dummies(X_df, columns=categorical_features_list,
                              dummy_na=False)  # True => add a column to indicate
        # NaNs. False => NaNs are ignored.
        #
        # Rather than get_dummies, it would be better as follows ...
        # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # enc.fit(X_df[categorical_features_list])

        # print(X_df.head(10))  # debug

        return X_df, y_ts, num_tr_instances

