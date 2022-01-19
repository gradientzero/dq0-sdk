from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1 as DatasetSpecificationV1


def output_metadata(m_interface, request_uuids, step):
    step += 1
    print("-------------------------------------------------------------------------------------\n"
          f"Metadata after step {step}:" "\n"
          "----------------------\n"
          f"{m_interface.__str__(request_uuids=request_uuids)}" "\n"
          "-------------------------------------------------------------------------------------")
    return step


def test_metadata_build():
    step = 0

    # define uuids for rights management.
    # use None to set default role rights and perform requests in 'god mode'.
    role_uuids = None
    request_uuids = None

    # define specifications that you would like to be used in the new Metadata.
    specifications = {
        'dataset': DatasetSpecificationV1(role_uuids=role_uuids),
    }

    # STEP 1
    # define the empty Metadata.
    metadata = Metadata(nodes={}, specifications=specifications)

    # as usual, obtain the interface from the metadata.
    # role_uuids are used for default permissions on new meta elements.
    m_interface = Interface(metadata=metadata, role_uuids=role_uuids)

    # the metadata is empty
    assert len(metadata) == 0
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 2
    # get new dataset object
    m_dataset = m_interface.dataset(name='test_dataset')

    # at this point you may call create() on the dataset or write any attribute field to create it.
    # however, one may also continue without directly creating it.
    # creation will happen automatically once the first dependent element is created.

    # get new database and connector attribute group objects.
    connector = m_dataset.database(name='test_database').connector

    # the metadata is still empty, as no element has been created yet.
    assert len(metadata) == 0
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 3
    # set the first attribute on connector (must be type_name as other fields only work if this one is present).
    connector.type_name = 'csv'

    # setting the attribute field forced creation of all underlying meta elements.
    assert len(metadata) == 1
    assert len(metadata.get_node(root_key='dataset')) == 1
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 4
    # set the csv's uri=filepath and you have created a useful minimal metadata
    connector.uri = '../dq0-sdk/dq0/examples/census/_data/adult_with_rand_names.csv'

    # the final metadata
    assert metadata.get_node(root_key='dataset').get_child_node(index=0).get_attribute(key='connector').get_attribute(
        key='uri').get_value() == '../dq0-sdk/dq0/examples/census/_data/adult_with_rand_names.csv'
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 5
    # continue until the first column
    m_column = m_dataset.database().schema(name='test_schema').table(name='test_table').column(name='test_column_a')

    # observe that database can be called without arguments, which is equivalent to calling with index=0 and which
    # works here, because database already exists. all other elements must be called by their new name.

    # there are no changes yet, as you have not created the column yet.
    assert len(metadata.get_node(root_key='dataset').get_child_node(index=0)) == 0
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 6
    # similar to connector depending on its type_name, many attribute groups of column depend on its data_type_name.
    # thus, you should set it early on.
    m_column.data.data_type_name = 'int'

    # again, setting the attribute forced creation.
    assert len(metadata.get_node(root_key='dataset').get_child_node(index=0)) == 1
    assert len(metadata.get_node(root_key='dataset').get_child_node(index=0).get_child_node(index=0)) == 1
    assert len(metadata.get_node(root_key='dataset').get_child_node(index=0).get_child_node(index=0).get_child_node(index=0)) == 1
    column = metadata.get_node(root_key='dataset').get_child_node(index=0).get_child_node(index=0).get_child_node(index=0).get_child_node(index=0)
    assert column.get_attribute(key='data').get_attribute(key='name').get_value() == 'test_column_a'
    assert column.get_attribute(key='data').get_attribute(key='data_type_name').get_value() == 'int'
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 7
    # Try changing connector type (this action is not allowed, as other connector fields depend on the type)
    try:
        connector.type_name = 'postgresql'
    except Exception as e:
        print("Step 7: Trying to set 'connector.type_name' to 'postgresql'\n"
              f"        correctly raised Exception '{e}'."
              "\n        One may delete the whole connector, though.")

    # however, one may delete the whole connector. [del only works if called with the accessor of the parent,
    # i.e., 'del m_database.connector' works, just 'del connector' does not work.]
    del m_dataset.database().connector

    # the connector is gone.
    assert metadata.get_node(root_key='dataset').get_child_node(index=0).get_attribute(key='connector') is None
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 8
    # create a different connector. The same 'connector' object continues to work, however, it is empty after
    # we deleted the previous connector.
    connector.type_name = 'postgresql'

    # the new connector appears.
    assert metadata.get_node(root_key='dataset').get_child_node(index=0).get_attribute(key='connector').get_attribute(
        key='type_name').get_value() == 'postgresql'
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 9
    # set the remaining attributes, to make it a useful connector.
    connector.host = 'postgresql1.dq0.io'
    connector.port = 5432
    connector.username = 'db_user'
    connector.password = 'super_secret_dp_password_that_noone_may_ever_even_imagine'

    # again, a useful final metadata.
    assert metadata.get_node(root_key='dataset').get_child_node(index=0).get_attribute(key='connector').get_attribute(
        key='password').get_value() == 'super_secret_dp_password_that_noone_may_ever_even_imagine'
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # finish test
    print("\nTEST SUCCESSFUL!")


if __name__ == "__main__":
    test_metadata_build()
