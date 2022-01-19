import json

from dq0.sdk.data.metadata.specification.json.metadata_schema import MetadataSchema


def test_metadata_validate():
    json_raw = MetadataSchema.json_schema()
    print("Metadata json schema:\n" f"{json_raw}")

    json_data = json.loads(json_raw)
    # print json schema
    print("Metadata json schema:\n" f"{json_data}")


if __name__ == "__main__":
    test_metadata_validate()
