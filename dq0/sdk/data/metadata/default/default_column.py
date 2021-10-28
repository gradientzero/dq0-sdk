from dq0.sdk.data.metadata.attribute.attribute_boolean import AttributeBoolean
from dq0.sdk.data.metadata.attribute.attribute_float import AttributeFloat
from dq0.sdk.data.metadata.attribute.attribute_int import AttributeInt
from dq0.sdk.data.metadata.attribute.attribute_string import AttributeString
from dq0.sdk.data.metadata.attribute.attribute import Attribute


class DefaultColumn:
    @staticmethod
    def defaultColumnBooleanAttributes():
        return [
            AttributeString(key='data_type_name', value='boolean'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='synthesizable', value=False),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
        ]

    @staticmethod
    def defaultColumnDatetimeAttributes():
        return [
            AttributeString(key='data_type_name', value='datetime'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='synthesizable', value=False),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
        ]

    @staticmethod
    def defaultColumnFloatAttributes():
        return [
            AttributeString(key='data_type_name', value='float'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='use_auto_bounds', value=False),
            AttributeFloat(key='auto_bounds_prob', value=0.9),
            AttributeBoolean(key='discrete', value=False),
            AttributeFloat(key='min_step', value=1.0),
            AttributeBoolean(key='synthesizable', value=True),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
            AttributeBoolean(key='bounded', value=False),
            AttributeFloat(key='auto_lower', value=0.0),
            AttributeFloat(key='auto_upper', value=0.0),
            AttributeFloat(key='lower', value=0.0),
            AttributeFloat(key='upper', value=0.0),
        ]

    @staticmethod
    def defaultColumnIntAttributes():
        return [
            AttributeString(key='data_type_name', value='int'),
            AttributeBoolean(key='selectable', value=False),
            AttributeBoolean(key='use_auto_bounds', value=False),
            AttributeFloat(key='auto_bounds_prob', value=0.9),
            AttributeBoolean(key='discrete', value=False),
            AttributeInt(key='min_step', value=1),
            AttributeBoolean(key='synthesizable', value=True),
            AttributeBoolean(key='is_feature', value=False),
            AttributeBoolean(key='is_target', value=False),
            AttributeBoolean(key='private_id', value=False),
            AttributeBoolean(key='bounded', value=False),
            AttributeInt(key='auto_lower', value=0),
            AttributeInt(key='auto_upper', value=0),
            AttributeInt(key='lower', value=0),
            AttributeInt(key='upper', value=0),
        ]

    @staticmethod
    def defaultColumnStringAttributes(cardinality=0):
        return [
            AttributeString('data_type_name', value='string'),
            AttributeBoolean('selectable', value=False),
            AttributeInt('cardinality', value=0),
            AttributeBoolean('synthesizable', value=cardinality != 0),
            AttributeBoolean('is_feature', value=False),
            AttributeBoolean('is_target', value=False),
            AttributeBoolean('private_id', value=False),
        ]

    @staticmethod
    def getDefaultAttributesFor(data_type_name, cardinality=0):
        if data_type_name == 'boolean':
            return DefaultColumn.defaultColumnBooleanAttributes()
        if data_type_name == 'datetime':
            return DefaultColumn.defaultColumnDatetimeAttributes()
        if data_type_name == 'float':
            return DefaultColumn.defaultColumnFloatAttributes()
        if data_type_name == 'int':
            return DefaultColumn.defaultColumnIntAttributes()
        if data_type_name == 'string':
            return DefaultColumn.defaultColumnStringAttributes(cardinality=cardinality)
        return []

    @staticmethod
    def mergeDefaultAttributesWith(column_attributes_list):
        if not isinstance(column_attributes_list, list):
            raise Exception("connector_attribute_list is not of list type")
        data_type_name = None
        cardinality = 0
        for tmp_attribute in column_attributes_list if column_attributes_list is not None else []:
            if tmp_attribute is None:
                raise Exception("found None attribute in list")
            if not isinstance(tmp_attribute, Attribute):
                raise Exception("found list element that is not of type Attribute")
            if tmp_attribute.key == 'data_type_name':
                data_type_name = tmp_attribute.value
            elif tmp_attribute.key == 'cardinality':
                cardinality = tmp_attribute.value
        return Attribute.merge_many_with_many(list_a=DefaultColumn.getDefaultAttributesFor(data_type_name=data_type_name, cardinality=cardinality), list_b=column_attributes_list, overwrite=True)
