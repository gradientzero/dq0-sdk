"""Child of TFHub for Image Classification"""
from dq0sdk.models.tf.tf_hub import TFHub
from dq0sdk.models.tf.tf_hub_models import hub_models_dict
from dq0sdk.utils.utils import YamlConfig

from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class TFHubImageClassification(TFHub):
    def __init__(self, model_path=None, tf_hub_url=None):
        super().__init__(model_path, tf_hub_url)
        yaml_path = hub_models_dict[tf_hub_url]
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict
        self.preprocessing = self.yaml_dict['PREPROCESSING']
        self.n_classes = None
        self.train_generator = None
        self.development_generator = None
        self.steps_per_epoch = None
        self.validation_steps = None
        self.test_generator = None
        self.test_steps = None

    def setup_data(self, augmentation=False):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            augmentation (bool): applies image augmenttion to training data
        """
        self.path_train = list(self.data_sources.values())[0].path_train
        self.path_test = list(self.data_sources.values())[0].path_test

        development_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        development_generator = development_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['development_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        if augmentation:
            train_datagen = keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],
                **self.preprocessing['train_datagen'],)
        else:
            train_datagen = development_datagen
        train_generator = train_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['train_dataflow'],
            **self.preprocessing['dataflow_kwargs'])

        test_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        test_generator = test_datagen.flow_from_directory(
            self.path_test,
            **self.preprocessing['test_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        # Get number of batches per epoch
        steps_per_epoch = train_generator.samples // train_generator.batch_size
        validation_steps = development_generator.samples // development_generator.batch_size
        test_steps = test_generator.samples // test_generator.batch_size

        self.n_classes = train_generator.num_classes
        self.train_generator = train_generator
        self.development_generator = development_generator
        self.test_generator = test_generator
        self.steps_per_epoch = steps_per_epoch
        self.validation_steps = validation_steps
        self.test_steps = test_steps

    def fit(self, epochs=None):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            epochs (int): number of epochs, default = from config
        """
        if epochs:
            self.epochs = epochs

        optimizer = keras.optimizers.SGD(
            **self.yaml_dict['OPTIMIZER'])
        self.model.compile(optimizer=optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=self.train_generator,
            steps_per_epoch=self.steps_per_epoch,
            validation_data=self.development_generator,
            validation_steps=self.validation_steps,
            epochs=self.epochs,
        )

    def fit_dp(self, epochs=None):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            epochs (int): number of epochs, default = from config
        """
        if epochs:
            self.epochs = epochs

        optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
            **self.yaml_dict['DP_OPTIMIZER'])
        self.model.compile(optimizer=optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=self.train_generator,
            steps_per_epoch=self.steps_per_epoch,
            validation_data=self.development_generator,
            validation_steps=self.validation_steps,
            epochs=self.epochs,
        )

    def evaluate(self):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Returns:
            metrics: to be defined!

        """
        evaluation = self.model.evaluate(x = self.test_generator,
                                         steps = self.test_steps)
        return evaluation

    def run_all(self, augmentation=False, epochs=None):
        """Runs experiment
        
        Does all the setup data, model, fit and evaluate

        """
        # setup data
        self.setup_data(augmentation=augmentation)

        # setup model
        self.setup_model()

        # fit
        self.fit_dp(epochs=epochs)

        # evaluate
        loss_te, acc_te, mse_te = self.evaluate()
        print('Test  Acc: %.2f %%' % (100 * acc_te))

    
