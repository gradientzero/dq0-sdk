# -*- coding: utf-8 -*-
"""
Example of transfer learning for image classification
using a pretrained feature_vector model from
tensorflow hub, namely, MobileNet stripped of classifier layer.

Note: the download of the data for this example can take several minutes
but it only does it once

"""
from dq0sdk.data.google_flowers.get_im_clf_data import get_im_clf_example_data
from dq0sdk.models.tf.tf_hub_image_classification import TFHubImageClassification


if __name__ == '__main__':
    # Need to download the data. This can take several minutes depending on your connection speed.
    get_im_clf_example_data()

    tf_hub_url = 'https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4'
    # tf_hub_url = 'https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/4'
    im_clf = TFHubImageClassification(tf_hub_url)

    test_generator, test_steps = im_clf.setup_data(augmentation=True)
    im_clf.setup_model()
    im_clf.fit_dp(epochs=2)

    # evaluate
    loss_te, acc_te, mse_te = im_clf.evaluate(x=test_generator, steps=test_steps)
    print('Test  Acc: %.2f %%' % (100 * acc_te))
