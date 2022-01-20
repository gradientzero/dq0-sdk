import json

from dq0.sdk.data.metadata.specification.json_schema.metadata import Metadata


def test_metadata_validate():
    json_raw = Metadata.json_schema()
    print("Metadata json schema:\n" f"{json_raw}")

    json_data = json.loads(json_raw)
    # print json schema
    print("Metadata json schema:\n" f"{json_data}")


if __name__ == "__main__":
    test_metadata_validate()
