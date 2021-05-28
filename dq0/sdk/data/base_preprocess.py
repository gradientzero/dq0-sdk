from abc import abstractmethod
import pickle

class BasePreprocess(object):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self, x, y=None, train=False):
        """ Execute User defined preprocessing

        used by UserModel and predict to preprocess data

        Args:
            - x: raw input data
            - y: raw input data labels
            - train [bool]: store transformer parameters

        Return:
            - x [pd.DataFrame, np.ndarray]: model input
            - y [pd.Series, np.array]: labels
        """
        pass

    def predict(self, x):
        """ wrapper of run for mlflow """
        return self.run(x=x)

