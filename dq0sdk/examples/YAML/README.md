# Configuring dq0 Neural Networks using YAML config
## Getting started:
Setting up your tf.Keras model via a yaml is currently limited to 
```Sequential``` models and follows the [tf.Keras](https://www.tensorflow.org/api_docs/python/tf/keras) ```to_yaml()``` and 
```model_from_yaml()``` conventions with the exception of using a yaml_string (this is taken care of internally).

We are using [PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

1. Create a yaml config file:
```yaml
MODEL:
  GRAPH:
    config:
      layers:
      - class_name: Dense
        config:
          activation: tanh
          batch_input_shape: !!python/tuple
          - null
          - 108 # number of features
          trainable: true
          units: 10
      - class_name: Dense
        config:
          activation: tanh
          trainable: true
          units: 10
      - class_name: Dense
        config:
          activation: tanh
          trainable: true
          units: 2 # number of classes
  OPTIMIZER:
    learning_rate: 0.3
  DP_OPTIMIZER:
    learning_rate: 0.3
    noise_multiplier: 1.3
    l2_norm_clip: 1.5
    num_microbatches: 1
  LOSS:
    class_name: SparseCategoricalCrossentropy
    from_logits: True
  METRICS:
    - accuracy
    - mse
FIT:
  epochs: 10
```

Usage:
```python
if __name__ == "__main__":
    class MyNN_yaml(dq0.models.tf.NeuralNetworkYaml):
        def setup_data():
            # do something
            pass

    yaml_path = 'dq0sdk/examples/YAML/yaml_config_adult.yaml'
    myModel = MyNN_yaml(yaml_path)
    myModel.setup_data()
    myModel.setup_model()
    myModel.fit()
    myModel.save()
    ...
```

## YAML Config:
The yaml config schema is:
```yaml
MODEL:
  GRAPH:
    config:
      layers:
      - class_name: <tf Layers class> # input layer
        config:
          <layer parameters>: val
          batch_input_shape: !!python/tuple
          - null
          - <input shape dim 0>
          - ...
          - <input shape dim n>
      - class_name: <tf Layers class> # output layer
        config:
          <layer parameters>: val
          units: int # number of classes
  OPTIMIZER:
    optimizer: <class name>
    kwargs:
      learning_rate: float
      ...: val
  DP_OPTIMIZER:
    optimizer: <class name>
    kwargs: 
      learning_trate: float
      noise_multiplier: float
      l2_norm_clip: float
      ...: val
  LOSS:
    loss: <losses class name>
    kwargs:
      <optional loss para 1>: val
      ...
      <optional loss para n>: val
  METRICS:
    - list item 1
    - ...
    - list item n
FIT:
  epochs: int
```
where,
- ['tf Layers class'](https://www.tensorflow.org/api_docs/python/tf/keras/layers) is a layer class name
- ['tf privacy para'](https://github.com/tensorflow/privacy/blob/master/tutorials/walkthrough/walkthrough.md) for the DPGradientDescentGaussianOptimizer optimizer
- ['losses class name' and 'optional loss para'](https://www.tensorflow.org/api_docs/python/tf/keras/losses) is a tf Keras losses class name and its parameters, respectively

Layers can include a [tensorflow hub](https://www.tensorflow.org/hub) model:
```yaml
MODEL:
  GRAPH:
    config:
      layers:
      - class_name: KerasLayer
        config:
          batch_input_shape: !!python/tuple
          - null
          - 224
          - 224
          - 3
          dtype: float32
          handle: https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/3
          name: keras_layer
          trainable: false
```

TIPP! If you have an existing model you can simply generate the model config using:
```python
your_model_dict = your_model.to_yaml()
with open(yaml_path, 'w') as yaml_file:
          yaml_file.write(your_model_dict)
```
copy paste the config: into your yaml config

## Running the Adult example using a yaml config

Update/View config file:

dq0sdk/examples/yaml/adult/yaml_config_adult.yaml

Run:

$ python dq0sdk/examples/yaml/adult/run_adult_from_yaml.py


## Running the image classification example using a yaml config and tf hub
includes save/load with post evaluation to verify it works

Update/View config file:

dq0sdk/examples/yaml/adult/yaml_config_adult.yaml

Run:

$ python dq0sdk/examples/yaml/adult/run_adult_from_yaml.py

## Preconfigured tf_hub models

Run:

$ python dq0sdk/examples/tf_hub/im_clf.py