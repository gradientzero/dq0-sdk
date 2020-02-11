# -*- coding: utf-8 -*-
"""
Example of transfer learning for image classification
using a pretrained feature_vector model from
tensorflow hub, namely, MobileNet stripped of classifier layer.

Note: the download of the data for this example can take several minutes
but it only does it once

"""

import os

from dq0sdk.data.google_flowers.flower_source import FlowerSource
from dq0sdk.models.tf.tf_hub_image_classification import TFHubImageClassification


if __name__ == '__main__':
    # data paths.
    path = 'dq0sdk/data/google_flowers/data/'
    path_train = os.path.join(os.getcwd(), path, 'train')
    path_test = os.path.join(os.getcwd(), path, 'test')

    # DataSources expect only one path parameter,
    # so concatenate the paths in split them inside.
    paths = '{};{}'.format(path_train, path_test)
    print(paths)

    dc = FlowerSource(paths)
    

    # tf_hub_url = 'https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4'
    # # tf_hub_url = 'https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/4'
    # im_clf = TFHubImageClassification(tf_hub_url)

    # test_generator, test_steps = im_clf.setup_data(augmentation=True)
    # im_clf.setup_model()
    # im_clf.fit_dp(epochs=2)

    # # evaluate
    # loss_te, acc_te, mse_te = im_clf.evaluate(x=test_generator, steps=test_steps)
    # print('Test  Acc: %.2f %%' % (100 * acc_te))
