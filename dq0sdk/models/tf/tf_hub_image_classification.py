"""Child of TFHub for Image Classification"""
from dq0sdk.models.tf.tf_hub import TFHub
from dq0sdk.models.tf.tf_hub_models import hub_models_dict
from dq0sdk.utils.utils import YamlConfig

from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class TFHubImageClassification(TFHub):
    def __init__(self, tf_hub_url):
        super().__init__(tf_hub_url)
        yaml_path = hub_models_dict[tf_hub_url]
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict
        self.preprocessing = self.yaml_dict['PREPROCESSING']
        self.n_classes = None
        self.train_generator = None
        self.development_generator = None
        self.steps_per_epoch = None
        self.validation_steps = None

    def setup_data(self, augmentation=False, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        development_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        development_generator = development_datagen.flow_from_directory(
            self.preprocessing['train_data_dir'],
            **self.preprocessing['development_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        if augmentation:
            train_datagen = keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],
                **self.preprocessing['train_datagen'],)
        else:
            train_datagen = development_datagen
        train_generator = train_datagen.flow_from_directory(
            self.preprocessing['train_data_dir'],
            **self.preprocessing['train_dataflow'],
            **self.preprocessing['dataflow_kwargs'])

        test_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        test_generator = test_datagen.flow_from_directory(
            self.preprocessing['test_data_dir'],
            **self.preprocessing['test_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        # Get number of batches per epoch
        steps_per_epoch = train_generator.samples // train_generator.batch_size
        validation_steps = development_generator.samples // development_generator.batch_size
        test_steps = test_generator.samples // test_generator.batch_size

        self.n_classes = train_generator.num_classes
        self.train_generator = train_generator
        self.development_generator = development_generator
        self.steps_per_epoch = steps_per_epoch
        self.validation_steps = validation_steps

        return test_generator, test_steps

    def fit(self, epochs=None, **kwargs):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            epochs (int): number of epochs, default = from config
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
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
            **kwargs,
        )

    def fit_dp(self, epochs=None, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            epochs (int): number of epochs, default = from config
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
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
            **kwargs,
        )
