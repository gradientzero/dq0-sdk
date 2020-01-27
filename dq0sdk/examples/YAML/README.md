# Running the Adult example using a yaml config

## Update/View config file
dq0sdk/examples/YAML/yaml_config_adult.yaml

## Run
$ python dq0sdk/examples/YAML/run_adult_from_yaml.py

## Example config file
```yaml
MODEL:
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
MODEL_PATH: notebooks/saved_model/
OPTIMIZER:
  learning_rate: 0.3
LOSS:
  class_name: SparseCategoricalCrossentropy
  from_logits: True
METRICS:
  - accuracy
  - mse
FIT:
  epochs: 10
```

## Example useage:
```python
if __name__ == "__main__":
    class MyNN_yaml(dq0.models.tf.NeuralNetwork):
        def setup_data():
            # do something
            pass

    yaml_path = 'dq0sdk/examples/YAML/yaml_config_adult.yaml'
    yaml_config = YamlConfig(yaml_path)
    
    myModel = MyNN_yaml(yaml_config)
    myModel.setup_data()
    myModel.setup_model()
    myModel.fit()
    myModel.save()
    
```
