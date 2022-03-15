from dq0.sdk.data.metadata.interface.attributes_group import AttributesGroup
from dq0.sdk.data.metadata.interface.run.v1.run.attributes_run_sql_query_processor import AttributesRunSQLQueryProcessor
from dq0.sdk.data.metadata.interface.run.v1.run.attributes_run_sql_result_processor import AttributesRunSQLResultProcessor
from dq0.sdk.data.metadata.specification.default_permissions import DefaultPermissions
from dq0.sdk.data.metadata.structure.attribute.attribute_type import AttributeType


class AttributesRunSQL(AttributesGroup):
    def __init__(self, run, attribute_list=None):
        super().__init__(key='sql',
                         permissions=DefaultPermissions.analyst_attribute(role_uuids=run.get_role_uuids()),
                         entity=run,
                         attribute_list=attribute_list,
                         create_attributes_group_func=self.create_attributes_group)

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'query_processor':
            return AttributesRunSQLQueryProcessor(attributes_run_sql=self, attribute_list=attribute_list)
        elif key == 'result_processor':
            return AttributesRunSQLResultProcessor(attributes_run_sql=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    # query_string
    @property
    def query_string(self):
        return self.get_attribute_value(key='query_string')

    @query_string.setter
    def query_string(self, new_query_string):
        self.set_attribute_value(type_name=AttributeType.TYPE_NAME_STRING,
                                 key='query_string',
                                 value=new_query_string,
                                 permissions=DefaultPermissions.analyst_attribute(role_uuids=self.get_role_uuids()))

    @query_string.deleter
    def query_string(self):
        raise Exception("query_string may not be deleted")

    # query_processor
    @property
    def query_processor(self):
        return super().get_attribute_group(key='query_processor')

    @query_processor.setter
    def query_processor(self, _):
        raise Exception("query_processor attribute group may not be set")

    @query_processor.deleter
    def query_processor(self):
        super().get_attribute_group(key='query_processor').delete()

    # result_processor
    @property
    def result_processor(self):
        return super().get_attribute_group(key='result_processor')

    @result_processor.setter
    def result_processor(self, _):
        raise Exception("result_processor attribute group may not be set")

    @result_processor.deleter
    def result_processor(self):
        super().get_attribute_group(key='result_processor').delete()
