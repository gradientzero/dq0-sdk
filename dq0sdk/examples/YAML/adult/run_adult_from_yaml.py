import os

from dq0sdk.data.adult import AdultSource
from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml

# import numpy as np
import pandas as pd

import sklearn
import sklearn.preprocessing
# import matplotlib.pyplot as plt


class NeuralNetworkYamlAdult(NeuralNetworkYaml):
    def __init__(self, yaml_path):
        super().__init__(yaml_path)
        self.input_dim = None

    def setup_data(self, X_df, y_ts, quantitative_features_list, num_tr_instances):
        # Scale values to the range from 0 to 1; to be precessed by the neural network
        X_df[quantitative_features_list] = sklearn.preprocessing.minmax_scale(X_df[quantitative_features_list])

        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)  # test to label
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)

        X_train_df, X_test_df, y_train_ts, y_test_ts = preprocessing.train_test_split(X_df, y_bin, num_tr_instances)
        self.input_dim = X_train_df.shape[1]

        return X_train_df, X_test_df, y_train_ts, y_test_ts


if __name__ == '__main__':

    path = 'dq0sdk/data/adult/data/'
    path_test = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../../', path, 'adult.test')
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../../', path, 'adult.data')

    dc = AdultSource(path_test, path_train)
    train_data, data = dc.read()
    X_df, y_ts, num_tr_instances = dc.preprocess(approach_for_missing_feature='imputation',
                                                 # 'imputation', 'dropping',
                                                 imputation_method_for_cat_feats='unknown',
                                                 # 'unknown', 'most_common_cat'
                                                 imputation_method_for_quant_feats='median',  # 'median', 'mean'
                                                 features_to_drop_list=None
                                                 )

    yaml_path = 'dq0sdk/examples/yaml/adult/yaml_config_adult.yaml'
    model = NeuralNetworkYamlAdult(yaml_path=yaml_path)
    X_train_df, X_test_df, y_train_ts, y_test_ts = model.setup_data(X_df, y_ts, dc.quantitative_features_list,
                                                                    num_tr_instances)
    model.setup_model()
    model.fit(x=X_train_df, y=y_train_ts)
    # model.fit_dp(X_train=X_train_df, y_train=y_train_ts)
    loss_tr, acc_tr, mse_te = model.evaluate(x=X_train_df, y=y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(x=X_test_df, y=y_test_ts)
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))

    # DP Version
    model.fit_dp(x=X_train_df, y=y_train_ts)
    # model.fit_dp(X_train=X_train_df, y_train=y_train_ts)
    loss_tr, acc_tr, mse_te = model.evaluate(x=X_train_df, y=y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(x=X_test_df, y=y_test_ts)
    print('Train DP Acc: %.2f %%' % (100 * acc_tr))
    print('Test DP  Acc: %.2f %%' % (100 * acc_te))
