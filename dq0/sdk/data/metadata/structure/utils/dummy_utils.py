from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.structure.metadata import Metadata


class DummyUtils:
    @staticmethod
    def dummy_meta_database_for_csv(filepath):
        yaml_content = f'''meta_dataset:
  format: 'simple'
  node:
    dataset:
      attributes:
        'data':
          'name': 'dummy_ds'
        'differential_privacy':
          'privacy_level': 0
      child_nodes:
        database:
          attributes:
            'connector':
              'type_name': 'csv'
              'uri': '{filepath}'
            'data':
              'name': 'dummy_db'
  specification: 'dataset_v1'
'''
        return Interface(metadata=Metadata.from_yaml(yaml_content=yaml_content)).dataset().database()
