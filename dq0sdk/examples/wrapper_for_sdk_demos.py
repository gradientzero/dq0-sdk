
from dq0.runtime.runtime import Runtime


class SdkDemo:
    """
    Wrapper for DQ0-core trainer, to keep it transparent to SDK users.
    """

    def __init__(self, user_model):

        # setup model trainer
        self.trainer = Runtime._get_trainer_for_model(user_model, True)

        self.model_metrics = user_model.metrics

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

        if type(model_metrics) != list:
            model_metrics = [model_metrics]

        for metric in model_metrics:
            print('\t' + metric.replace('_', ' ') + ' on ' + dataset_type
                  + ' set: %.2f %%' % (100 * res[metric]))
