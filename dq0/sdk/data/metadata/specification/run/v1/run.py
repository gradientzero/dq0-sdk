from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.specification.json_schema.node import Node as JsonSchemaNode
from dq0.sdk.data.metadata.specification.json_schema.run.attribute import Attribute as JsonSchemaRunAttribute
from dq0.sdk.data.metadata.specification.json_schema.run.attributes_group import AttributesGroup as JsonSchemaRunAttributesGroup
from dq0.sdk.data.metadata.specification.run.v1.sql import Sql
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Run:
    @staticmethod
    def apply_defaults(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=None, allowed_permissions=None)
        applied_attributes = Run.apply_defaults_to_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.analyst_node(role_uuids=role_uuids) if node.get_permissions() is None else node.get_permissions().copy()
        return Node(type_name=node.get_type_name(), attributes=applied_attributes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            applied_attribute.set_default_permissions(default_permissions=analyst_attribute)
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(node, role_uuids=None):
        Node.check(node=node, allowed_type_names=[NodeType.TYPE_NAME_RUN], allowed_permissions=DefaultPermissions.analyst_attribute(role_uuids=role_uuids))
        Run.verify_attributes(attributes=node.get_attributes(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        analyst_attribute = DefaultPermissions.analyst_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'data': ([AttributeType.TYPE_NAME_LIST], analyst_attribute),
            'sql': ([AttributeType.TYPE_NAME_LIST], analyst_attribute),
        }, required_keys={'data'})
        data_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'data'] \
            if attributes is not None else []
        if 0 < len(data_attributes):
            Attribute.check_list(attribute_list=data_attributes[0].get_value(), check_data={
                'description': ([AttributeType.TYPE_NAME_STRING], analyst_attribute),
                'name': ([AttributeType.TYPE_NAME_STRING], analyst_attribute),
                'type_name': ([AttributeType.TYPE_NAME_STRING], analyst_attribute),
            }, required_keys={'name', 'type_name'})
        sql_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'sql'] \
            if attributes is not None else []
        if 0 < len(sql_attributes):
            Sql.verify(attribute=sql_attributes[0], role_uuids=role_uuids)

    @staticmethod
    def json_schema():
        run_sql = Run.sql_json_schema().replace('\n', "\n    ")
        return f"""{{
  "oneOf": [
    {run_sql}
  ]
}}"""

    @staticmethod
    def sql_json_schema():
        return JsonSchemaNode.json_schema(
            NodeType.TYPE_NAME_RUN,
            attributes_groups=[
                JsonSchemaRunAttributesGroup.data(
                    attributes=[
                        JsonSchemaRunAttribute.description(
                            node_type_name=NodeType.TYPE_NAME_RUN
                        ),
                        JsonSchemaRunAttribute.name(
                            node_type_name=NodeType.TYPE_NAME_RUN
                        ),
                        JsonSchemaRunAttribute.run_type_name(
                            node_type_name=NodeType.TYPE_NAME_RUN,
                            additional_value="\"const\": \"sql\""
                        )
                    ]
                ),
                Sql.json_schema()
            ],
            attributes_groups_additional_contains=JsonSchemaAttributesGroup.json_schema(
                key='sql',
                group_name="sql",
                description="This item ensures, that the 'sql' attributes group is present."
            ),
            attributes_groups_additional_description="Requires 'sql' attributes group.",
        )
