from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Column:
    @staticmethod
    def data(data_type_name):
        return AttributesGroup.data(
            attributes=[
                Attribute.json_schema(
                    key='data_type_name',
                    attribute_name='data type name',
                    description="The 'data type name' attribute. Specifies the name of the data type "
                        f"for the '{NodeType.TYPE_NAME_COLUMN}'.",
                    type_name=AttributeType.TYPE_NAME_STRING,
                    additional_value=f"\"const\": \"{data_type_name}\""
                ),
                Attribute.description(node_type_name=NodeType.TYPE_NAME_COLUMN),
                Attribute.metadata_is_public(node_type_name=NodeType.TYPE_NAME_COLUMN),
                Attribute.name(node_type_name=NodeType.TYPE_NAME_COLUMN),
                Attribute.json_schema(
                    key='selectable',
                    attribute_name='selectable',
                    description="The 'selectable' attribute. Specifies whether a selection may happen "
                        f"for the '{NodeType.TYPE_NAME_COLUMN}'.",
                    type_name=AttributeType.TYPE_NAME_BOOLEAN
                )
            ],
            additional_contains=[
                Attribute.json_schema(
                    key='data_type_name',
                    attribute_name='data type name',
                    description="This item ensures that the 'data_type_name' attribute is present.",
                    type_name=AttributeType.TYPE_NAME_STRING
                )
            ],
            additional_description=" Requires a 'data_type_name' attribute."
        )

    @staticmethod
    def machine_learning():
        return AttributesGroup.machine_learning(
            attributes=[
                Attribute.json_schema(
                    key='is_feature',
                    attribute_name="is feature",
                    description=f"The 'is feature' attribute. Specifies whether this '{NodeType.TYPE_NAME_COLUMN}' is a feature.",
                    type_name=AttributeType.TYPE_NAME_BOOLEAN
                ),
                Attribute.json_schema(
                    key='is_target',
                    attribute_name="is target",
                    description=f"The 'is target' attribute. Specifies whether this '{NodeType.TYPE_NAME_COLUMN}' is a target.",
                    type_name=AttributeType.TYPE_NAME_BOOLEAN
                )
            ]
        )
