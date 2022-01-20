from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.specification.dataset.v1.specification_v1 import SpecificationV1 as DatasetSpecificationV1
from dq0.sdk.data.metadata.structure.metadata import Metadata


def output_metadata(m_interface, request_uuids, step):
    step += 1
    print("-------------------------------------------------------------------------------------\n"
          f"Metadata after step {step}:" "\n"
          "----------------------\n"
          f"{m_interface.__str__(request_uuids=request_uuids)}" "\n"
          "-------------------------------------------------------------------------------------")
    return step


def show_metadata_build():
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
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 3
    # set the first attribute on connector (must be type_name as other fields only work if this one is present).
    connector.type_name = 'csv'

    # setting the attribute field forced creation of all underlying meta elements.
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 4
    # set the csv's uri=filepath and you have created a useful minimal metadata
    connector.uri = '../dq0-sdk/dq0/examples/census/_data/adult_with_rand_names.csv'

    # the final metadata
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    connector_dict = connector.to_dict(request_uuids=None)

    print(f"Connector dict: {connector_dict}")

    # STEP 5
    # continue until the first column
    m_column = m_dataset.database().schema(name='test_schema').table(name='test_table').column(name='test_column_a')

    # observe that database can be called without arguments, which is equivalent to calling with index=0 and which
    # works here, because database already exists. all other elements must be called by their new name.

    # there are no changes yet, as you have not created the column yet.
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)

    # STEP 6
    # similar to connector depending on its type_name, many attribute groups of column depend on its data_type_name.
    # thus, you should set it early on.
    m_column.data.data_type_name = 'int'

    # again, setting the attribute forced creation.
    step = output_metadata(m_interface=m_interface, request_uuids=request_uuids, step=step)


if __name__ == "__main__":
    show_metadata_build()
