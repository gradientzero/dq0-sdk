import cloudpickle

from dq0.examples.census.raw.model.user_model import UserModel
from dq0.sdk.data.metadata.structure.utils.dummy_utils import DummyUtils
from dq0.sdk.data.text.csv import CSV

if __name__ == '__main__':
    # init input data source
    filepath = '../dq0-sdk/dq0/examples/census/_data/adult_with_rand_names_w_header.csv'
    # filepath = '/Users/susdorf/Documents/Customers/gradient0/dq0-sdk/dq0/examples/census/_data/adult_with_rand_names_w_header_full.yaml'
    data_source = CSV(DummyUtils.dummy_meta_database_for_csv(filepath=filepath))
    # create model
    model = UserModel()
    # attach data set to model
    model.attach_data_source(data_source)
    # prepare data
    model.setup_data()
    # setup model
    model.setup_model()
    # fit the model
    model.fit()
    pickled = cloudpickle.dumps(model)
    print("--------")
    print(len(pickled))
    print("--------")
    loaded = cloudpickle.loads(pickled)
    # print(loaded(self=None, x=pd.DataFrame()))
    if model.uuid == loaded.uuid:
        print("TRUE:: uuid")
    else:
        raise Exception('uuid differ: {} with {}'.format(model.uuid, loaded.uuid))
    if model.data_source.uuid == loaded.data_source.uuid:
        print("TRUE:: data_source")
    else:
        raise Exception('data_source differ: {} with {}'.format(model.data_source, loaded.data_source))
    if model.model_type == loaded.model_type:
        print("TRUE:: model_type")
    else:
        raise Exception('model_type differ: {} with {}'.format(model.model_type, loaded.model_type))
    model_evaluate = model.evaluate()
    loaded_evaluate = loaded.evaluate()
    if model_evaluate == loaded_evaluate:
        print('eveluate equals')
    print("--------")
