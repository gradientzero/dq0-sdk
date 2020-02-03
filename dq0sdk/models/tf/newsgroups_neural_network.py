
"""
Neural network Model class

Basic Tensorflow neural-network implementation using Keras.

Todo:
    * Protect Keras compile and fit functions

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>

Copyright 2019, Gradient Zero
"""

import warnings

from dq0sdk.data.utils import plotting
from dq0sdk.data.utils import util
from dq0sdk.models.model import Model

import numpy as np

import pandas as pd

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

import tensorflow as tf  # no GPU support for Mac. In any case,
# NVIDIA GPU card with CUDA is required.
# from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class NewsgroupsNeuralNetwork(Model):
    """
    Newsgroups Neural Network model implementation

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """

    def __init__(self, **kwargs):

        super().__init__()

        if 'saved_model_folder' in kwargs:
            self._saved_model_folder = kwargs['saved_model_folder']
        else:
            self._saved_model_folder = './data/output'
        self._model_type = kwargs['model_type']

        if 'DP_enabled' in kwargs:
            self.DP_enabled = kwargs['DP_enabled']
        else:
            self.DP_enabled = False

        if self.DP_enabled:
            self._model_type = 'DP-' + self._model_type
            self.DP_epsilon = kwargs['DP_epsilon']

        self._label_encoder = None
        self._setup_model(num_features=kwargs['num_features'],
                          num_classes=kwargs['num_classes'])

        if self.DP_enabled:
            raise NotImplementedError('\n\nDP-version of NN not ready '
                                      'yet. In particular, in TfPrivacy '
                                      'epsilon cannot be defined a-priori.'
                                      '\n\n')

    def _setup_model(self, **kwargs):
        """
        Setup model function

        Implementing child classes can use this method to define the
        Keras model.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """

        # TODO: below parameters set in Yaml file to be parsed by this
        # function
        self.learning_rate = 0.001  # 0.15
        self.epochs = 10  # 50 in ML-leaks paper
        self.verbose = 2
        self.metrics = ['accuracy']
        # TODO: grid search over parameters space

        # network topology. TODO: make it parametric!
        if self._model_type.startswith('DP-'):
            network_type = self._model_type[3:]
        else:
            network_type = self._model_type
        if util.case_insensitive_str_comparison(network_type, 'cnn'):
            print('Setting up a multilayer convolution neural network...')
            self._model = self._get_cnn_model(None, kwargs['num_classes'])
        elif util.case_insensitive_str_comparison(network_type, 'mlnn'):
            print('Setting up a multilayer neural network...')
            self._model = self._get_mlnn_model(kwargs['num_features'], kwargs[
                'num_classes'])
        elif util.case_insensitive_str_comparison(network_type, 'simple_nn'):
           print('Setting up a single-layer softmax network...')
           self._model = self._get_softmax_model(kwargs['num_features'],
                                                 kwargs['num_classes'])

    def _get_mlnn_model(self, n_in, n_out, which_model='ml-leaks_paper'):

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):
            # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py
            num_units_hidden_layer = 128
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(num_units_hidden_layer,
                                      activation='tanh'),
                tf.keras.layers.Dense(n_out, activation='softmax')]
            )
        else:
            model = tf.keras.Sequential([
                tf.keras.layers.Input(n_in),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(10, activation='tanh'),
                tf.keras.layers.Dense(n_out, activation='softmax')]
            )

        model.summary()
        return model

    def _get_softmax_model(self, n_in, n_out):

        # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py

        num_units_hidden_layer = 64
        model = tf.keras.Sequential([
            tf.keras.layers.Input(n_in),
            tf.keras.layers.Dense(num_units_hidden_layer,
                                  activation='tanh'),
            tf.keras.layers.Dense(n_out, activation='softmax')]
        )

        model.summary()
        return model

    def _get_cnn_model(self, n_in, n_out, which_model='tf_tutorial'):

        if util.case_insensitive_str_comparison(which_model, 'ml-leaks_paper'):

            # https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py

            model = tf.keras.Sequential()
            # create the convolutional base
            model.add(tf.keras.layers.Conv2D(32, (5, 5), activation='relu',
                      nput_shape=(32, 32, 3)))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu'))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

            # add Dense layers on top
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            model.add(tf.keras.layers.Dense(n_out, activation='softmax'))

        elif util.case_insensitive_str_comparison(which_model, 'tf_tutorial'):

            # https://www.tensorflow.org/tutorials/images/cnn

            model = tf.keras.Sequential()
            # create the convolutional base
            model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                      input_shape=(32, 32, 3)))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

            # add Dense layers on top
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(64, activation='relu'))
            model.add(tf.keras.layers.Dense(n_out, activation='softmax'))

        model.summary()
        return model

    def setup_model(self, **kwargs):
        # to inherit from abstract base class
        pass

    def setup_data(self, **kwargs):
        # to inherit from abstract base class
        pass

    def prepare(self, y_np_a, **kwargs):
        """
        Prepare data for model training (preprocess data). Called before
        model fit on every run.

        Args:
            y_np_a: Numpy array with the class labels
            kwargs (:obj:`dict`): dictionary of optional arguments
        """

        #
        # from sklearn import preprocessing
        # lb = preprocessing.LabelBinarizer()
        # lb.fit([1, 2, 6, 4, 2])
        # >>> LabelBinarizer()
        # lb.classes_
        # >>> array([1, 2, 4, 6])
        # lb.transform([1, 6])
        # >>> array([[1, 0, 0, 0],
        #     [0, 0, 0, 1]])
        #

        # if self._label_encoder is None:
        #     self._label_encoder = LabelBinarizer()
        #     y_encoded_np_a = self._label_encoder.fit_transform(y_np_a).flatten()
        # else:
        #     y_encoded_np_a = self._label_encoder.transform(y_np_a).flatten()
        #

        if y_np_a.ndim == 2:
            # make non-dimensional array (just to avoid Warnings by Sklearn)
            y_np_a = np.ravel(y_np_a)

        # LabelEncoder() encodes target labels with value between 0 and
        # n_classes - 1
        if self._label_encoder is None:
            # self._label_encoder is None => y contains train labels
            self._label_encoder = LabelEncoder()
            y_encoded_np_a = self._label_encoder.fit_transform(y_np_a)
        else:
            y_encoded_np_a = self._label_encoder.transform(y_np_a)

        return y_encoded_np_a

    def fit(self, **kwargs):
        """
        Model fit function

        It learns a model from training data.
        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """

        X_train_np_a, y_train_np_a = self._get_train_data_from_kwargs(kwargs)

        y_train_encoded_np_a = self.prepare(y_train_np_a)

        print('\n\n-------------------- ' + self._model_type + ' classifier '
              'learning ---------------------')
        if self.DP_enabled:
            print('DP epsilon set to', self.DP_epsilon)
        print('\nPercentage freq. of target labels in train dataset:')
        util.pretty_print_dict(
            util.get_percentage_freq_of_values(y_train_np_a)
        )

        if not self.DP_enabled:
            optimizer, loss, additional_fit_params_dict = \
                self._define_training_parameters()
        else:
            optimizer, loss, additional_fit_params_dict, X_train_np_a, \
                y_train_encoded_np_a = self._define_dp_training_parameters(
                    X_train_np_a, y_train_encoded_np_a)

        self._model.compile(optimizer=optimizer,
                            loss=loss,
                            metrics=self.metrics)

        self._print_training_params(optimizer, additional_fit_params_dict)

        self._model.fit(X_train_np_a,
                        y_train_encoded_np_a,
                        epochs=self.epochs,
                        verbose=self.verbose,
                        **additional_fit_params_dict)

        print('\nLearned a ' + self._model_type + ' model. ')

        # test on training set
        y_pred_np_a = self.predict(X_train_np_a)
        accuracy_score = metrics.accuracy_score(y_train_np_a, y_pred_np_a)
        print('\nModel accuracy on training data:', round(accuracy_score, 2))

        return accuracy_score

    def _get_train_data_from_kwargs(self, kwargs):

        if 'X_train_np_a' in kwargs:
            X_train_np_a = kwargs['X_train_np_a']
        elif 'X_train_df' in kwargs:
            X_train_np_a = kwargs['X_train_df'].values
        else:
            if isinstance(kwargs['X_train'], pd.DataFrame):
                X_train_np_a = kwargs['X_train'].values
            else:
                X_train_np_a = kwargs['X_train']

        if 'y_train_np_a' in kwargs:
            y_train_np_a = kwargs['y_train_np_a']
        elif 'y_train_ts' in kwargs:
            y_train_np_a = kwargs['y_train_ts'].values
        else:
            if isinstance(kwargs['y_train'], pd.Series):
                y_train_np_a = kwargs['y_train'].values
            else:
                y_train_np_a = kwargs['y_train']

        return X_train_np_a, y_train_np_a

    def _define_training_parameters(self):
        """
        Define parameters of the training procedure fitting a neural
        network to the training data.

        """

        # optimizer = dp_optimizer.GradientDescentOptimizer(
        #    learning_rate=self.learning_rate)
        # loss = tf.keras.losses.SparseCategoricalCrossentropy(
        # from_logits=True)
        # optimizer = 'adam'
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        loss = 'sparse_categorical_crossentropy'
        additional_fit_params_dict = {'batch_size': 100}

        return optimizer, loss, additional_fit_params_dict

    def _define_dp_training_parameters(self, X_train_np_a, y_train_np_a):
        """
        Define parameters of the differentially-private training of the
        neural network

        """

        num_microbatches = 250

        # TODO: make training robust for any number of
        # minibatches -> bug in optimize function
        num_minibatches = round(X_train_np_a.shape[0] / num_microbatches)
        X_train_np_a = X_train_np_a[:num_minibatches * num_microbatches]
        y_train_np_a = y_train_np_a[:num_minibatches * num_microbatches]

        # DPSGD Training
        optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
            l2_norm_clip=1.0,
            noise_multiplier=1.1,
            num_microbatches=num_microbatches,
            learning_rate=self.learning_rate)

        # Compute vector of per-example loss rather than
        # its mean over a minibatch.
        loss = 'sparse_categorical_crossentropy'
        # tf.keras.losses.SparseCategoricalCrossentropy(
        # from_logits=True,
        # reduction=tf.compat.v1.losses.Reduction.NONE)

        additional_fit_params_dict = {'batch_size': num_microbatches}

        return optimizer, loss, additional_fit_params_dict, X_train_np_a, \
            y_train_np_a

    def _print_training_params(self, optimizer, additional_fit_params_dict):

        print('\nTraining parameters:')
        print('\toptimization algorithm:', optimizer if isinstance(
            optimizer, str) else optimizer.get_config()['name'])
        print('\tepochs:', self.epochs)
        print('\tlearning_rate:', self.learning_rate)
        print('\tmetric: ', ', '.join(self.metrics))
        if 'batch_size' in additional_fit_params_dict:
            print('\tbatch_size:', additional_fit_params_dict['batch_size'])

    def fit_dp(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
        """
        raise RuntimeError('to fit a model with dp, crate an instance '
                           'of this class enabling DP and call the fit method')
        pass

    def get_classes(self):
        """
        Just a wrapper for sklearn attribute classes_
        According to the documentation of scikit-learn v. 0.22:
            "classes_ :  array, shape (n_classes,)
                         class labels known to the classifier"

        """
        return self._label_encoder.classes_

    def predict(self, X_test, **kwargs):
        """Generate class predictions for the input test samples.

        This method is final. Signature will be checked at runtime!
        Args:
            X_test_np_a: Numpy 2D array with test data
            kwargs (:obj:`dict`): dictionary of optional arguments.
        Returns:
            y_pred_np_a: Numpy array of the predicted classes, one per
            test example.
        """

        if isinstance(X_test, pd.DataFrame):
            X_test_np_a = X_test.values
        else:
            X_test_np_a = X_test

        class_probabilities_np_a = self._model.predict(X_test_np_a)

        # map the predicted class probabilities back to class labels
        if class_probabilities_np_a.shape[-1] > 1:
            y_pred_np_a = class_probabilities_np_a.argmax(axis=-1)  # argmax
            # over the last dimension
        else:
            y_pred_np_a = (class_probabilities_np_a > 0.5).astype('int32')

        # encoded labels back to multi-class labels
        y_pred_np_a = self._label_encoder.inverse_transform(y_pred_np_a)
        #  self._label_encoder.inverse_transform(y_pred_np_a, threshold=0)  #
        #  in the case of LabelBinarizer

        return y_pred_np_a

    def predict_proba(self, X_test, top_n_proba_only=3):
        """
        Mimic sklearn predict_proba() function.
        :param X_test_np_a: Numpy 2D array with test data
        :param top_n_proba_only: set to n to keep only the top-n class
                                 probabilities. If set to None is has no
                                 effect.
        :return: Pandas DataFrame posterior_class_probab_df with class
                 probabilities
        """
        if isinstance(X_test, pd.DataFrame):
            X_test_np_a = X_test.values
        else:
            X_test_np_a = X_test

        assert (top_n_proba_only is None) or (top_n_proba_only >= 2)

        probs_np_a = self._model.predict(X_test_np_a)

        if probs_np_a.min() < 0. or probs_np_a.max() > 1.:
            warnings.warn('Network returning invalid probability values. '
                          'The last layer might not normalize predictions '
                          'into probabilities (like softmax or sigmoid would).'
                          )
        # print(type(probs_np_a))

        probs_np_a, class_names = self._keep_top_n_class_probabilities_only(
            probs_np_a, top_n_proba_only)
        posterior_class_probab_df = pd.DataFrame(probs_np_a,
                                                 columns=class_names)

        return posterior_class_probab_df

    def _keep_top_n_class_probabilities_only(self, probs_np_a,
                                             top_n_proba_only):
        """

        :param probs_np_a:
        :param top_n_proba_only:
        :return: numpy.ndarray with top-n probabilities and class_names. If
        all the class probabilities are retained, class_names list contains
        the class names associated with the probabilities. Otherwise,
        class_list has the form ["top-1", "top-2", "top-3", ...]
        """

        num_proba = probs_np_a.shape[1]  # num. of classes of the
        # classification task
        if (top_n_proba_only is not None) and (top_n_proba_only < num_proba):
            print("\nKeep only the top-" + str(top_n_proba_only) + " probabilities")
            # minus sign to sort in descending order
            probs_np_a = - np.sort(- probs_np_a, axis=1)
            probs_np_a = probs_np_a[:, 0:top_n_proba_only]

            class_names = []
            for r in range(1, top_n_proba_only + 1):
                class_names.append("top_" + str(r))
        else:
            index = np.arange(0, probs_np_a.shape[1], 1)
            class_names = list(self._label_encoder.inverse_transform(index))
            # class_names = list(self.get_classes())

        return probs_np_a, class_names

    def evaluate(self, X_test, y_test, output_folder,
                 enable_plots=False,
                 classifier_description='',
                 verbose=False
                 ):
        """
        Test learnt classifier over a test set
        :param X_test_np_a: test instances
        :param y_test_np_a: learning signal
        :param output_folder:
        :param enable_plots: flag to generate a jpg file with the confusion
                             matrix
        :param classifier_description: name of file containing the confusion
                                       matrix (if enabled)
        :param verbose: self-explanatory
        :return: accuracy score over test set    print(X_train_np_a.shape)
        """

        print('\n\n--------------------- Testing learnt classifier '
              '---------------------')

        if isinstance(X_test, pd.DataFrame):
            X_test_np_a = X_test.values
        else:
            X_test_np_a = X_test

        if isinstance(y_test, pd.Series):
            y_test_np_a = y_test.values
        else:
            y_test_np_a = y_test

        y_pred_np_a = self.predict(X_test_np_a)

        print(
            '\nPercentage freq. of target labels in test dataset (baseline '
            'for classification performance):')
        util.pretty_print_dict(
            util.get_percentage_freq_of_values(y_test_np_a)
        )

        accuracy_score = metrics.accuracy_score(y_test_np_a, y_pred_np_a)
        print('\nModel accuracy on test data:', round(accuracy_score, 2))
        print('\n', metrics.classification_report(y_test_np_a, y_pred_np_a))

        if enable_plots:
            plotting.plot_confusion_matrix(
                y_test_np_a, y_pred_np_a, output_folder,
                part_of_fn_describing_matrix=classifier_description,
                xticks_rotation='horizontal')

        return accuracy_score

    def save(self, name, version='1.0'):
        """
        Save the model in binary format on local storage

        This method is final. Signature will be checked at runtime!
        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        self._model.save('{}/{}_{}.h5'.format(self._saved_model_folder, name,
                         version), include_optimizer=False)

    def load(self, name, version='1.0'):
        """
        Load the model from local storage

        This method is final. Signature will be checked at runtime!
        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """
        self._model = tf.keras.models.load_model('{}/{}_{}.h5'.format(
            self._saved_model_folder, name, version), compile=False)
