from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class ConnectorMySQL:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        applied_attributes = ConnectorMySQL.apply_defaults_to_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)
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
        ConnectorMySQL.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        owner_attribute = DefaultPermissions.owner_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'charset': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'host': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'password': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
            'port': ([AttributeType.TYPE_NAME_INT], owner_attribute),
            'type_name': ([AttributeType.TYPE_NAME_STRING], DefaultPermissions.shared_attribute(role_uuids=role_uuids)),
            'username': ([AttributeType.TYPE_NAME_STRING], owner_attribute),
        }, required_keys={'host', 'type_name'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].get_value() != 'mysql':
            raise Exception(f"mysql connector type_name value {type_name_attributes[0].get_value()} does not match 'mysql'")

    @staticmethod
    def json_schema():
        return JsonSchemaAttributesGroup.json_schema(
            key='connector',
            group_name='connector mysql',
            description="The 'connector mysql' attributes group.",
            additional_description="Requires 'host' and 'type_name' attributes.",
            contains=[
                JsonSchemaAttribute.json_schema(
                    key='host', attribute_name="host", description="This item ensures that the 'host' attribute is present.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='type_name', attribute_name="type name", description="This item ensures that the 'type_name' attribute is present.",
                    type_name=AttributeType.TYPE_NAME_STRING
                )
            ],
            attributes=[
                JsonSchemaAttribute.json_schema(
                    key='charset',
                    attribute_name='charset',
                    description="The 'charset' attribute specifies the charset for the client connection.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='host',
                    attribute_name='host',
                    description="The 'host' attribute specifies the hostname of the server running the mysql database.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='password',
                    attribute_name='password',
                    description="The 'password' attribute specifies the password to log into the mysql server.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='port',
                    attribute_name='port',
                    description="The 'port' attribute specifies the port number, where to connect to the mysql server.",
                    type_name=AttributeType.TYPE_NAME_INT,
                    additional_value=""""minimum": 1,
"maximum": 65535"""
                ),
                JsonSchemaAttribute.json_schema(
                    key='type_name',
                    attribute_name="type name",
                    description="The 'type name' attribute specifies the type of connector. In this case it is a 'mysql' connector.",
                    type_name=AttributeType.TYPE_NAME_STRING,
                    additional_value="\"const\": \"mysql\""
                ),
                JsonSchemaAttribute.json_schema(
                    key='username',
                    attribute_name='username',
                    description="The 'username' attribute specifies the username to log into the mysql server.",
                    type_name=AttributeType.TYPE_NAME_STRING
                )
            ])
