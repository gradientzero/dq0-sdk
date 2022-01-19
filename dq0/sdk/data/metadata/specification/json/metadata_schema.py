from dq0.sdk.data.metadata.specification.dataset.v1.dataset import Dataset


class MetadataSchema:
    @staticmethod
    def json_schema():
        dataset_json_schema = Dataset.json_schema().replace('\n', "\n        ")
        return f"""{{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dq0.io/metadata.schema.json",
  "title": "Metadata",
  "description": "A DQ0 metadata object",
  "type": "object",
  "properties": {{
    "meta_dataset": {{
      "title": "Meta Dataset",
      "description": "The dataset root node in the metadata.",
      "type": "object",
      "properties": {{
        "format": {{
          "title": "Format",
          "description": "The format of the dataset metadata.",
          "type": "string",
          "const": "full"
        }},
        "node": {dataset_json_schema},
        "specification": {{
          "title": "Specification",
          "description": "The specification to validate the dataset metadata against.",
          "type": "string",
          "const": "dataset_v1"
        }}
      }},
      "required": [ "format", "specification" ],
      "additionalProperties": false
    }}
  }},
  "additionalProperties": false
}}"""
