# -*- coding: utf-8 -*-
"""
Adult dataset loading

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>
Copyright 2019, Gradient Zero
"""

import pandas as pd

from dq0sdk.data.source import Source
from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.utils import util


class AdultSource(Source):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def read(self):

        training_dataset_path = self.input_folder + 'adult.data'  # csv file
        test_dataset_path = self.input_folder + 'adult.test'  # csv file
        tr_dataset_df, _, _, _ = self._load_input_dataset(
            training_dataset_path)
        # Load test data skipping the bad row in the test data.
        test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature = \
            self._load_input_dataset(test_dataset_path, skiprows=1)

        return tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature

    def _load_input_dataset(self, dataset_file_path, skiprows=None):

        print('Load dataset from file "' + dataset_file_path + '" ')
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

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        # quantitative_features_list = list(set(column_names_list) -
        #                                  set(categorical_features_list) -
        #                                  set([target_feature]))

        # To speed up load of data in RAM and to optimize memory consumption.
        # Not really sensible effect if dataset size is limited.
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
                                 # comment='|',  # dataset has comment in it
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

        categorical_features_list = [
            column for column in dataset_df.columns
            if column != target_feature and dataset_df[column].dtype == 'object'
        ]

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        quantitative_features_list = list(
            set(column_names_list) - set(categorical_features_list) - set([
                target_feature])
        )

        return dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature

    def get_preprocessed_X_y_train_and_X_y_test(self):

        tr_dataset_df, test_dataset_df, categorical_features_list, \
            quantitative_features_list, target_feature = \
            self.read()

        util.print_dataset_info(tr_dataset_df, 'Raw training dataset')
        util.print_dataset_info(test_dataset_df, 'Raw test dataset')

        tr_dataset_df, quantitative_features_list, categorical_features_list = \
            self._keep_selected_quantitative_features_only(tr_dataset_df,
                                                           target_feature)

        test_dataset_df, quantitative_features_list, categorical_features_list = \
            self._keep_selected_quantitative_features_only(test_dataset_df,
                                                           target_feature)

        X_train_df, X_test_df, y_train_ts, y_test_ts = \
            self.preprocess(
                tr_dataset_df,
                test_dataset_df,
                categorical_features_list,
                quantitative_features_list,
                target_feature,
                approach_for_missing_feature='imputation',  # 'imputation',
                # 'dropping',
                imputation_method_for_cat_feats='unknown',  # 'unknown',
                # 'most_common_cat'
                imputation_method_for_quant_feats='median',  # 'median',
                # 'mean'
                features_to_drop_list=None  # ['fnlwgt', 'education-num']
            )

        return X_train_df, X_test_df, y_train_ts, y_test_ts, target_feature

    def _keep_selected_quantitative_features_only(self, dataset_df,
                                                  target_feature):

        selected_quantitative_feats_list = [
            'age',
            'education-num',
            'capital-gain',
            'capital-loss',
            'hours-per-week'
        ]

        dataset_df = dataset_df[selected_quantitative_feats_list + [
            target_feature]]

        categorical_features_list = []

        print('\nKeep only a subset of quantitative features. The '
              'following features survived the cut:')
        util.pretty_print_strings_list(selected_quantitative_feats_list,
                                       'quantitative features')
        util.pretty_print_strings_list(categorical_features_list,
                                       'categorical features')

        return dataset_df, selected_quantitative_feats_list, \
            categorical_features_list

    def preprocess(
        self, tr_dataset_df, test_dataset_df,
        categorical_features_list, quantitative_features_list, target_feature,
        approach_for_missing_feature='imputation',  # 'imputation', 'dropping',
        imputation_method_for_cat_feats='unknown',  # 'unknown',
                                                    # 'most_common_cat'
        imputation_method_for_quant_feats='median',  # 'median', 'mean'
        features_to_drop_list=None
    ):

        print('\n\n--------------------- Data preprocessing '
              '---------------------')
        # 1. impute missing values with data or remove missing values.
        #    According to the adult.names file, unknown values are encoded
        #    via the "?" string.
        # 2. drop uninformative features (given the remaining features)
        # 3. encode the categorical features as numeric data via one-hot
        #    encoding

        print('\nHandling training instances with missing values')
        tr_dataset_df = preprocessing.handle_missing_data(
            tr_dataset_df,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,
            categorical_features_list=categorical_features_list,
            quantitative_features_list=quantitative_features_list
        )

        print('\nHandling test instances with missing values')
        test_dataset_df = preprocessing.handle_missing_data(
            test_dataset_df,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,
            categorical_features_list=categorical_features_list,
            quantitative_features_list=quantitative_features_list
        )

        num_tr_instances, _ = tr_dataset_df.shape
        num_test_instances, _ = test_dataset_df.shape

        X_train_df = tr_dataset_df.drop(target_feature, axis=1)
        X_test_df = test_dataset_df.drop(target_feature, axis=1)

        # full dataset
        X_df = X_train_df.append(X_test_df)
        y_ts = tr_dataset_df[target_feature].append(
            test_dataset_df[target_feature])

        # cleanup labels: strip trailing '.'
        y_ts = y_ts.apply(lambda label: label.rstrip("."))

        util.print_dataset_info(X_df, 'Raw full dataset without target_feature'
                                )

        if features_to_drop_list is not None:
            X_df.drop(features_to_drop_list, axis=1, inplace=True)
            util.pretty_print_strings_list(
                features_to_drop_list,
                '\nThe following uninformative features (given the remaining '
                'ones)  have been dropped:')

        if categorical_features_list:
            print('\nConvert categorical features to numerical representations'
                  ' by one-hot encoding')
            #
            # (Weak) assumption: for each categorical feature, its values in
            # the test set is already present in the training set.
            #
            X_df = pd.get_dummies(X_df, columns=categorical_features_list,
                                  dummy_na=False)  # True => add a column to
            # indicate NaNs. False => NaNs are ignored.
            #
            # Rather than get_dummies, it would be better as follows ...
            # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
            # enc.fit(X_df[categorical_features_list])

            # print(X_df.head(10))  # debug

            util.pretty_print_strings_list(X_df.columns.tolist(),
                                           'After one-hot encoding categorical '
                                           'features, the features are')

        # X_train, X_test, y_train, y_test = model_selection.train_test_split(
        #   X, y, test_size=0.3, stratify=y)

        X_train_df, X_test_df, y_train_ts, y_test_ts = \
            preprocessing.train_test_split(X_df, y_ts, num_tr_instances)

        return X_train_df, X_test_df, y_train_ts, y_test_ts

    def save_preprocessed_tr_and_te_datasets(self, X_train_df, X_test_df,
                                             y_train_ts, y_test_ts,
                                             working_folder):

        pd.concat([X_train_df, y_train_ts], axis=1).to_csv(
            working_folder + 'preprocessed_training_data.csv', index=False)
        pd.concat([X_test_df, y_test_ts], axis=1).to_csv(
            working_folder + 'preprocessed_test_data.csv', index=False)

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        return {}
