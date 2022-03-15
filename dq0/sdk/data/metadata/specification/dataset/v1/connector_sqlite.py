from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class ConnectorSQLite:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        applied_attributes = ConnectorSQLite.apply_defaults_to_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)
        applied_permissions = DefaultPermissions.shared_attribute(role_uuids=role_uuids) \
            if attribute.get_permissions() is None else attribute.get_permissions().copy()
        return AttributeList(key=attribute.get_key(), value=applied_attributes, permissions=applied_permissions)

    @staticmethod
    def apply_defaults_to_attributes(attributes, role_uuids=None):
        Attribute.check_list(attribute_list=attributes, check_data=None)
        applied_attributes = [] if attributes is not None else None
        for attribute in attributes if attributes is not None else []:
            applied_attribute = attribute.copy()
            applied_attribute.set_default_permissions(default_permissions=DefaultPermissions.shared_attribute(role_uuids=role_uuids))
            applied_attributes.append(applied_attribute)
        return applied_attributes

    @staticmethod
    def verify(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data={
            'connector': ([AttributeType.TYPE_NAME_LIST], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
        })
        ConnectorSQLite.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'uri': ([AttributeType.TYPE_NAME_STRING], shared_attribute)
        }, required_keys={'type_name', 'uri'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].get_value() != 'sqlite':
            raise Exception(f"sqlite connector type_name value {type_name_attributes[0].get_value()} does not match 'sqlite'")

    @staticmethod
    def json_schema():
        return JsonSchemaAttributesGroup.json_schema(
            key='connector',
            group_name='connector sqlite',
            description="The 'connector sqlite' attributes group.",
            additional_description="Requires 'type_name' and 'uri' attributes.",
            contains=[
                JsonSchemaAttribute.json_schema(
                    key='type_name', attribute_name="type name", description="This item ensures that the 'type_name' attribute is present.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='uri', attribute_name="uri", description="This item ensures that the 'uri' attribute is present.",
                    type_name=AttributeType.TYPE_NAME_STRING
                )
            ],
            attributes=[
                JsonSchemaAttribute.json_schema(
                    key='type_name',
                    attribute_name="type name",
                    description="The 'type name' attribute specifies the type of connector. In this case it is a 'sqlite' connector.",
                    type_name=AttributeType.TYPE_NAME_STRING,
                    additional_value="\"const\": \"sqlite\""
                ),
                JsonSchemaAttribute.json_schema(
                    key='uri',
                    attribute_name='uri',
                    description="The 'uri' attribute specifies the URI pointing to the SQLite file (e.g. a filepath).",
                    type_name=AttributeType.TYPE_NAME_STRING
                )
            ])
