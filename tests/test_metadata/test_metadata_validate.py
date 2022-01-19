from dq0.sdk.data.metadata.specification.json.metadata_schema import MetadataSchema


def test_metadata_validate():
    # print json schema
    print("Metadata json schema:\n" f"{MetadataSchema.json_schema()}")


if __name__ == "__main__":
    test_metadata_validate()
