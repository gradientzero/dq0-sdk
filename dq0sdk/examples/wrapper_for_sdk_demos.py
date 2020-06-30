# -*- coding: utf-8 -*-
"""SDK Runtime helper

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.runtime.runtime import Runtime


class SdkDemo:
    """
    Wrapper for DQ0-core trainer, to keep it transparent to SDK users.
    """

    def __init__(self, user_model):

        # setup model trainer
        self.trainer = Runtime._get_trainer_for_model(user_model, True)

        if hasattr(user_model, 'metrics'):
            # user_model is a Tensorflow model
            self.model_metrics = user_model.metrics
        else:
            # user_model is a Scikit model
            self.model_metrics = None

    def fit_model(self):
        self.trainer.fit()

    def evaluate_model(self):
        print('\nModel performance:')
        res_tr = self.trainer.evaluate(test_data=False)
        SdkDemo._print_evaluation_res(res_tr, 'training', self.model_metrics)
        res_te = self.trainer.evaluate()
        SdkDemo._print_evaluation_res(res_te, 'test', self.model_metrics)

    @staticmethod
    def _print_evaluation_res(res, dataset_type, model_metrics):
        """
        Print the results of call of trainer.evaluate()

        Args:
            res (:obj:`dict`): Results returned by trainer.evaluate()
            dataset_type (:obj:`str`): string with two possible values:
            "training" or "test"
            model_metrics (:obj:`list`): list of metrics specified in user model

        """

        if model_metrics is None:
            # user_model is a Scikit model
            for metric in res.keys():
                print('\t' + metric.replace('_', ' ') + ' on ' + dataset_type + ''
                      ' set: %.2f %%' % (100 * res[metric]))

        else:
            # user_model is a Tensorflow model
            if type(model_metrics) != list:
                model_metrics = [model_metrics]

            for metric in model_metrics:
                print('\t' + metric.replace('_', ' ') + ' on ' + dataset_type + ''
                      ' set: %.2f %%' % (100 * res[fix_metric_names(metric)]))


def fix_metric_names(metric):
    """
    In Tensorflow there is a mismatch between the metric names that a user can
    specify and the metric names used internally.

    Args:
            metric (:obj:`str`): name given by user

    Returns:
        Metric name used internally by Tensorflow corresponding to the
        metric name specified by the user
    """

    if metric.lower() == 'accuracy':
        metric = 'acc'
    elif metric.lower() == 'mse':
        metric = 'mean_squared_error'

    return metric
