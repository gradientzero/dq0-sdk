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
from dq0sdk.models.tf.neural_network_tfhub_image_classification import NeuralNetworkTFHubImageClassification


if __name__ == '__main__':
    # INPUTS
    # data paths.
    path = 'dq0sdk/data/google_flowers/'
    path_train = os.path.join(os.getcwd(), path, 'train')
    path_test = os.path.join(os.getcwd(), path, 'test')

    # DataSources expect only one path parameter,
    # so concatenate the paths in split them inside.
    paths = '{};{}'.format(path_train, path_test)

    # tensorflowhub model
    tf_hub_url = 'https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4'  # These are actually version 3 because of model not stored error
    # tf_hub_url = 'https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/4'

    # model path
    model_path = 'notebooks/saved_model/model_name.h5'

    # CODE
    # init data source
    dc = FlowerSource(paths)

    # init model
    im_clf = NeuralNetworkTFHubImageClassification('notebooks/saved_model/', tf_hub_url)

    # attache data source to model
    im_clf.attach_data_source(dc)

    # run setup data, setup model, fit and evaluate
    im_clf.dp_epochs = 2
    im_clf.run_all(augment=True)
