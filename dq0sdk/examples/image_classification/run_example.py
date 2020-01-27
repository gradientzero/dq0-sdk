# -*- coding: utf-8 -*-
"""Instructions to run

data source: https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz
1. download source and unpack to dq0sdk/data/google_flowers/flower_photos
2. run dq0sdk/data/google_flowers/split_train_test.py
3. make sure to install updated requirements.txt
4. should be good to go
"""
import os
import tensorflow as tf

from dq0sdk.models.tf.process_yaml_config import YamlConfig
from dq0sdk.models.tf.tf_hub import TFHub

if __name__=='__main__':
    yaml_path = 'dq0sdk/examples/image_classification/yaml_config_image.yaml'
    yaml_config = YamlConfig(yaml_path)
    yaml_dict = yaml_config.yaml_dict
    # print(yaml_dict)

    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        #**yaml_dict['PREPROCESSING']['train_datagen'],
        )

    development_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        #**yaml_dict['PREPROCESSING']['development_datagen'],
        )

    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        #**yaml_dict['PREPROCESSING']['test_datagen'],
        )

    train_generator = train_datagen.flow_from_directory(
        yaml_dict['PREPROCESSING']['train_data_dir'],
        **yaml_dict['PREPROCESSING']['train_dataflow'],
        **yaml_dict['PREPROCESSING']['base_dataflow']
        )

    development_generator = development_datagen.flow_from_directory(
        yaml_dict['PREPROCESSING']['train_data_dir'],
        **yaml_dict['PREPROCESSING']['development_dataflow'],
        **yaml_dict['PREPROCESSING']['base_dataflow'],
        )

    test_generator = test_datagen.flow_from_directory(
        yaml_dict['PREPROCESSING']['test_data_dir'],
        **yaml_dict['PREPROCESSING']['test_dataflow'],
        **yaml_dict['PREPROCESSING']['base_dataflow'],
        )

    # Create instaqnce of tfhub
    im_cls = TFHub(yaml_config)
    im_cls.setup_model()
    # Fit model
    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps = development_generator.samples // development_generator.batch_size
    im_cls.fit(x=train_generator,
            steps_per_epoch=steps_per_epoch,
            validation_data=development_generator,
            validation_steps=validation_steps,
            )
    # evaluate
    test_steps = test_generator.samples // test_generator.batch_size
    loss_te, acc_te, mse_te = im_cls.evaluate(x=test_generator,steps = test_steps)
    print('Test  Acc: %.2f %%' % (100 * acc_te))
    # Save and load model
    im_cls.save('mobilenetv3','0.1')
    im_cls2 = TFHub(yaml_config)
    im_cls2.load('mobilenetv3','0.1')
    # evaluate
    print('Model reloaded from file')
    test_steps = test_generator.samples // test_generator.batch_size
    loss_te, acc_te, mse_te = im_cls2.evaluate(x=test_generator,steps = test_steps)
    print('Test Acc: %.2f %%' % (100 * acc_te))

