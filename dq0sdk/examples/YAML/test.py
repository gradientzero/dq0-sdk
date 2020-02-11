# from tensorflow_privacy.privacy.optimizers import dp_optimizer

from dq0sdk.utils.utils import YamlConfig

yaml_config = YamlConfig('dq0sdk/examples/YAML/test.yaml')
yaml_dict = yaml_config.yaml_dict

optimizer = yaml_dict['DP_OPTIMIZER']['optimizer'](**yaml_dict['DP_OPTIMIZER']['kwargs'])
print(optimizer._learning_rate)

# print(yaml_dict)

