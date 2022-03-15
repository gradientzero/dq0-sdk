from dq0.sdk.data.metadata.specification.dataset.v1.dataset import Dataset
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.run.v1.run import Run


class Metadata:
    @staticmethod
    def json_schema():
        attribute_permissions = DefaultPermissions.json_schema_attribute_permissions().replace('\n', "\n    ")
        node_permissions = DefaultPermissions.json_schema_node_permissions().replace('\n', "\n    ")
        dataset = Dataset.json_schema().replace('\n', "\n        ")
        run = Run.json_schema().replace('\n', "\n        ")
        return f"""{{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dq0.io/metadata.schema.json",
  "$defs": {{
    "attribute_permissions": {attribute_permissions},
    "node_permissions": {node_permissions}
  }},
  "description": "A DQ0 metadata object",
  "type": "object",
  "properties": {{
    "meta_dataset": {{
      "description": "The dataset root node in the metadata.",
      "type": "object",
      "properties": {{
        "format": {{
          "description": "The format of the dataset metadata.",
          "type": "string",
          "const": "full"
        }},
        "node": {dataset},
        "specification": {{
          "description": "The specification to validate the dataset metadata against.",
          "type": "string",
          "const": "dataset_v1"
        }}
      }},
      "required": [ "format", "specification" ],
      "additionalProperties": false
    }},
    "meta_run": {{
      "description": "The run root node in the metadata.",
      "type": "object",
      "properties": {{
        "format": {{
          "description": "The format of the run metadata.",
          "type": "string",
          "const": "full"
        }},
        "node": {run},
        "specification": {{
          "description": "The specification to validate the run metadata against.",
          "type": "string",
          "const": "run_v1"
        }}
      }},
      "required": [ "format", "specification" ],
      "additionalProperties": false
    }}
  }},
  "additionalProperties": false
}}"""
