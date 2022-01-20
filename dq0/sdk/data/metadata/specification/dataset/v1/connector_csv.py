from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.specification.json_schema.attribute import Attribute as JsonSchemaAttribute
from dq0.sdk.data.metadata.specification.json_schema.attributes_group import AttributesGroup as JsonSchemaAttributesGroup
from dq0.sdk.data.metadata.structure.attribute.attribute import Attribute
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class ConnectorCSV:
    @staticmethod
    def apply_defaults(attribute, role_uuids=None):
        Attribute.check(attribute=attribute, check_data=None)
        applied_attributes = ConnectorCSV.apply_defaults_to_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)
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
        ConnectorCSV.verify_attributes(attributes=attribute.get_value(), role_uuids=role_uuids)

    @staticmethod
    def verify_attributes(attributes, role_uuids=None):
        shared_attribute = DefaultPermissions.shared_attribute(role_uuids=role_uuids)
        Attribute.check_list(attribute_list=attributes, check_data={
            'decimal': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'header_columns': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'header_row': ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_LIST], shared_attribute),
            'index_col': ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_LIST, AttributeType.TYPE_NAME_STRING], shared_attribute),
            'na_values': ([AttributeType.TYPE_NAME_LIST], shared_attribute),
            'sep': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'skipinitialspace': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
            'type_name': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'uri': ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            'use_original_header': ([AttributeType.TYPE_NAME_BOOLEAN], shared_attribute),
        }, required_keys={'type_name'})
        type_name_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'type_name'] if attributes is not None else []
        if type_name_attributes[0].get_value() != 'csv':
            raise Exception(f"csv connector type_name value {type_name_attributes[0].get_value()} does not match 'csv'")
        header_columns_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'header_columns'] \
            if attributes is not None else []
        if 0 < len(header_columns_attributes):
            Attribute.check_list(attribute_list=header_columns_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
        header_row_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'header_row'] if attributes is not None else []
        if 0 < len(header_row_attributes) and header_row_attributes[0].get_type_name() == AttributeType.TYPE_NAME_LIST:
            Attribute.check_list(attribute_list=header_row_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_INT], shared_attribute),
            })
        index_col_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'index_col'] if attributes is not None else []
        if 0 < len(index_col_attributes) and index_col_attributes[0].get_type_name() == AttributeType.TYPE_NAME_LIST:
            Attribute.check_list(attribute_list=index_col_attributes[0].get_value(), check_data={
                None: ([AttributeType.TYPE_NAME_INT, AttributeType.TYPE_NAME_STRING], shared_attribute),
            })
            if 0 < len(index_col_attributes[0].get_value()):
                Attribute.check_list(attribute_list=index_col_attributes[0].get_value(), check_data={
                    None: ([index_col_attributes[0].get_value()[0].get_type_name()], shared_attribute),
                })
        na_value_attributes = [tmp_attribute for tmp_attribute in attributes if tmp_attribute.get_key() == 'na_values'] if attributes is not None else []
        if 0 < len(na_value_attributes):
            Attribute.check_list(attribute_list=na_value_attributes[0].get_value(), check_data=None)
            for tmp_attribute in na_value_attributes[0].get_value():
                if tmp_attribute.get_key() is None:
                    raise Exception("na_values may not have none keys")

    @staticmethod
    def json_schema():
        return JsonSchemaAttributesGroup.json_schema(
            key='connector',
            group_name='connector csv',
            description="The 'connector csv' attributes group.",
            additional_description="Requires 'type_name' attribute.",
            contains=JsonSchemaAttribute.json_schema(
                key='type_name', attribute_name="type name", description="This item ensures that the 'type_name' attribute is present.",
                type_name=AttributeType.TYPE_NAME_STRING),
            attributes=[
                JsonSchemaAttribute.json_schema(
                    key='decimal',
                    attribute_name='decimal',
                    description="The 'decimal' attribute specifies the decimal separator used in the CSV file.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.no_key_list(
                    key='header_columns',
                    attribute_name="header columns",
                    description="The 'header columns' attribute specifies a list of columns names present in the CSV file.",
                    item_attribute_name="header column",
                    item_description="A single 'header column' item in the 'header columns' list of column names.",
                    item_type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='header_row',
                    attribute_name="header row",
                    description="The 'header row' attribute identifies a single row index or a list of indexes for rows that contain header information. "
                        "This is the single row index version.",
                    type_name=AttributeType.TYPE_NAME_INT,
                    additional_value="\"minimum\": 0"
                ),
                JsonSchemaAttribute.no_key_list(
                    key='header_row',
                    attribute_name="header row",
                    description="The 'header row' attribute identifies a single row index or a list of indexes for rows that contain header information. "
                                "This is the row index list version.",
                    item_attribute_name="header row index",
                    item_description="A single 'header row index' item in the 'header row' list of row indexes.",
                    item_type_name=AttributeType.TYPE_NAME_INT,
                    item_additional_value="\"minimum\": 0"
                ),
                JsonSchemaAttribute.json_schema(
                    key='index_col',
                    attribute_name="index col",
                    description="The 'index col' attribute identifies a single column index/name or a list of column indexes/names for columns that contain "
                                "indexes. This is the single column index version.",
                    type_name=AttributeType.TYPE_NAME_INT,
                    additional_value="\"minimum\": 0"
                ),
                JsonSchemaAttribute.json_schema(
                    key='index_col',
                    attribute_name='index col',
                    description="The 'index col' attribute identifies a single column index/name or a list of column indexes/names for columns that contain "
                                "indexes. This is the single column name version.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.no_key_list(
                    key='index_col',
                    attribute_name="index col",
                    description="The 'index col' attribute identifies a single column index/name or a list of column indexes/names for columns that contain "
                                "indexes. This is the column index list version.",
                    item_attribute_name="index col index",
                    item_description="A single 'index col index' item in the 'index col' list of column indexes.",
                    item_type_name=AttributeType.TYPE_NAME_INT,
                    item_additional_value="\"minimum\": 0"
                ),
                JsonSchemaAttribute.no_key_list(
                    key='index_col',
                    attribute_name="index col",
                    description="The 'index col' attribute identifies a single column index/name or a list of column indexes/names for columns that contain "
                                "indexes. This is the column name list version.",
                    item_attribute_name="index col index",
                    item_description="A single 'index col index' item in the 'index col' list of column names.",
                    item_type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.any_key_value_list(
                    key='na_values',
                    attribute_name="na values",
                    description="The 'na values' attribute consists of a list of attributes that define na values for specific columns in the CSV file.",
                    item_attribute_name='na value',
                    item_description="A single 'na value' for a specific column."
                ),
                JsonSchemaAttribute.json_schema(
                    key='sep',
                    attribute_name='sep',
                    description="The 'sep' attribute specifies the field delimiter used in the CSV file.",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='skipinitialspace',
                    attribute_name="skip initial space",
                    description="The 'skip initial space' attribute specifies whether to skip space after the field delimiter 'sep'.",
                    type_name=AttributeType.TYPE_NAME_BOOLEAN
                ),
                JsonSchemaAttribute.json_schema(
                    key='type_name',
                    attribute_name="type name",
                    description="The 'type name' attribute specifies the type of connector. In this case it is a 'csv' connector.",
                    type_name=AttributeType.TYPE_NAME_STRING,
                    additional_value="\"const\": \"csv\""
                ),
                JsonSchemaAttribute.json_schema(
                    key='uri',
                    attribute_name='uri',
                    description="The 'uri' attribute specifies the URI pointing to the CSV file (e.g. a filepath).",
                    type_name=AttributeType.TYPE_NAME_STRING
                ),
                JsonSchemaAttribute.json_schema(
                    key='use_original_header',
                    attribute_name="use original header",
                    description="The 'use original header' attribute specifies whether to use the original header inside the CSV file.",
                    type_name=AttributeType.TYPE_NAME_BOOLEAN
                )
            ])
