# -*- coding: utf-8 -*-
"""
Example of transfer learning for image classification
using a pretrained feature_vector model from
tensorflow hub, namely, MobileNet stripped of classifier layer.

Note: the download of the data for this example can take several minutes
but it only does it once

@author: Craig Lincoln <cl@gradient0.com>
"""
import logging

# import os
from dq0sdk.data.google_flowers.get_im_clf_data import get_im_clf_example_data
from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml

import tensorflow as tf

tf.random.set_seed(0)

logger = logging.getLogger()


if __name__ == '__main__':
    # Need to download the data. This can take several minutes depending on your connection speed.
    get_im_clf_example_data()

    yaml_path = 'dq0sdk/examples/yaml/im_clf/yaml_config_image.yaml'
    im_clf = NeuralNetworkYaml(yaml_path)
    yaml_dict = im_clf.yaml_dict
    print(yaml_dict)

    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        # **yaml_dict['PREPROCESSING']['train_datagen'],
    )

    development_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        # **yaml_dict['PREPROCESSING']['development_datagen'],
    )

    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        **yaml_dict['PREPROCESSING']['base_datagen'],
        # **yaml_dict['PREPROCESSING']['test_datagen'],
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

    # Get number of batches per epoch
    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps = development_generator.samples // development_generator.batch_size
    test_steps = test_generator.samples // test_generator.batch_size

    # Create instance of NNFromYaml
    # im_clf = NeuralNetworkYaml(yaml_path)
    im_clf.setup_model()
    # Fit model
    im_clf.fit(x=train_generator,
               steps_per_epoch=steps_per_epoch,
               validation_data=development_generator,
               validation_steps=validation_steps,
               )

    # evaluate
    loss_tr, acc_tr, mse_tr = im_clf.evaluate(x=train_generator, steps=steps_per_epoch)
    loss_te, acc_te, mse_te = im_clf.evaluate(x=test_generator, steps=test_steps)
    print('Train  Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))

    # # Save and load model
    # im_clf.save('mobilenetv3','0.1')
    # im_clf.load('mobilenetv3','0.1')
    # # evaluate
    # print('Model reloaded from file')
    # # loss_tr, acc_tr, mse_tr = im_clf.evaluate(x=train_generator,steps = steps_per_epoch)
    # loss_te, acc_te, mse_te = im_clf.evaluate(x=test_generator,steps = test_steps)
    # # print('Train  Acc: %.2f %%' % (100 * acc_tr))
    # print('Test  Acc: %.2f %%' % (100 * acc_te))

    # DP Version
    im_clf_dp = NeuralNetworkYaml(yaml_path)
    im_clf_dp.setup_model()
    im_clf_dp.fit_dp(x=train_generator,
                     steps_per_epoch=steps_per_epoch,
                     validation_data=development_generator,
                     validation_steps=validation_steps,
                     )
    # evaluate
    loss_tr, acc_tr, mse_tr = im_clf_dp.evaluate(x=train_generator, steps=steps_per_epoch)
    loss_te, acc_te, mse_te = im_clf_dp.evaluate(x=test_generator, steps=test_steps)
    print('Train DP  Acc: %.2f %%' % (100 * acc_tr))
    print('Test DP  Acc: %.2f %%' % (100 * acc_te))

    # Save and load model
    im_clf.save('mobilenetv3_dp', '0.1')
    im_clf.load('mobilenetv3_dp', '0.1')
    # evaluate
    print('Model reloaded from file')
    # loss_tr, acc_tr, mse_tr = im_clf_dp.evaluate(x=train_generator,steps = steps_per_epoch)
    loss_te, acc_te, mse_te = im_clf_dp.evaluate(x=test_generator, steps=test_steps)
    # print('Train DP  Acc: %.2f %%' % (100 * acc_tr))
    print('Test DP Acc: %.2f %%' % (100 * acc_te))
