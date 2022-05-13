from dq0.sdk.data.metadata.interface.entity import Entity
from dq0.sdk.data.metadata.interface.run.v1.run.attributes_run_data import AttributesRunData
from dq0.sdk.data.metadata.interface.run.v1.run.attributes_run_logging import AttributesRunLogging
from dq0.sdk.data.metadata.interface.run.v1.run.attributes_run_sql import AttributesRunSQL
from dq0.sdk.data.metadata.structure.attribute.attribute_list import AttributeList
from dq0.sdk.data.metadata.structure.node.node import Node
from dq0.sdk.data.metadata.structure.node.node_type import NodeType


class Run(Entity):
    @staticmethod
    def check_type_name(type_name):
        if type_name not in ['sql']:
            raise Exception(f"unknown type_name {type_name}")

    def __init__(self, name, parent, permissions=None, data_permissions=None, name_permissions=None, role_uuids=None, node=None):
        super().__init__(name=name, type_name=NodeType.TYPE_NAME_RUN, parent=parent,
                         permissions=permissions, data_permissions=data_permissions, name_permissions=name_permissions,
                         create_attributes_group_func=self.create_attributes_group, role_uuids=role_uuids, node=node)

    def get_type_name(self):
        data_attribute = self.get_node().get_attribute(key='data') if isinstance(self.get_node(), Node) else None
        type_name_attribute = data_attribute.get_attribute(key='type_name') if isinstance(data_attribute, AttributeList) else None
        type_name = type_name_attribute.get_value() if type_name_attribute is not None else None
        if type_name is not None:
            Run.check_type_name(type_name=type_name)
        return type_name

    def create_attributes_group(self, key, attribute_list=None):
        if key == 'data':
            return AttributesRunData(run=self, attribute_list=attribute_list)
        elif key == 'logging':
            return AttributesRunLogging(run=self, attribute_list=attribute_list)
        elif key == 'sql':
            if self.get_type_name() is None:
                raise Exception("cannot access sql without type_name being set")
            if self.get_type_name() != 'sql':
                raise Exception("attribute group sql not allowed for non sql run")
            return AttributesRunSQL(run=self, attribute_list=attribute_list)
        else:
            raise Exception(f"key {key} is invalid")

    # data
    @property
    def data(self):
        return super().get_attribute_group(key='data')

    @data.setter
    def data(self, _):
        raise Exception("data attribute group may not be set")

    @data.deleter
    def data(self):
        super().get_attribute_group(key='data').delete()

    # logging
    @property
    def logging(self):
        return super().get_attribute_group(key='logging')

    @logging.setter
    def logging(self, _):
        raise Exception("logging attribute group may not be set")

    @logging.deleter
    def logging(self):
        super().get_attribute_group(key='logging').delete()

    # sql
    @property
    def sql(self):
        return super().get_attribute_group(key='sql')

    @sql.setter
    def sql(self, _):
        raise Exception("sql attribute group may not be set")

    @sql.deleter
    def sql(self):
        super().get_attribute_group(key='sql').delete()
