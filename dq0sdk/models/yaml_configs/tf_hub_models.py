"""Curated list of hub models"""

hub_models_dict = {
    'https://tfhub.dev/google/imagenet/mobilenet_v2_100_96/feature_vector/4': {
        'yaml_path': 'dq0sdk/models/yaml_configs/mobilenet_v2_100_96_feature_vecotr_V4.yaml',
        'task': 'im_clf'},
    'https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4': {
        'yaml_path': 'dq0sdk/models/yaml_configs/mobilenet_v2_100_224_feature_vecotr_V4.yaml',
        'task': 'im_clf'},
    'https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/4': {
        'yaml_path': 'dq0sdk/models/yaml_configs/resnet50_v2_224_feature_vector_V4.yaml',
        'task': 'im_clf'},
    'https://tfhub.dev/google/albert_base/3': {
        'yaml_path': 'dq0sdk/models/yaml_configs/allbert_base_128_embeddings_V3.yaml',
        'task': 'text_clf'},
}
