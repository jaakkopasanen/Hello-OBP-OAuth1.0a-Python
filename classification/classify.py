from sklearn.preprocessing import StandardScaler
import numpy as np
from classification import features
import keras
from keras.models import Sequential, model_from_json
from keras.optimizers import SGD
from keras.layers import Dense, Activation
from datetime import datetime

from ObpApi.api_credentials import *
from ObpApi.ObpApi import ObpApi
from test_users import TEST_USERS

def get_test_data():
    """Only for testing purposes"""
    user = TEST_USERS[10]
    obp_api = ObpApi(
        host='https://op.openbankproject.com',
        version='2.1.0',
        direct_login_url='/my/logins/direct',
        oauth_url='/oauth',
        oauth_callback_url='http://localhost',
        consumer_key=OBP_CONSUMER_KEY,
        consumer_secret=OBP_CONSUMER_SECRET
    )
    login_success = obp_api.login_direct(user['username'],
                                         user['password'])
    # login_success = obp_api.initiate_oauth()
    # obp_api.hello()
    accounts = obp_api.get_all_private_accounts()
    # for acc in accounts:
    #     account = obp_api.get_account(acc['bank_id'], acc['id'], 'owner')
    #     print('{currency} {amount} @ {iban}'.format(
    #         currency=account['balance']['currency'],
    #         amount=account['balance']['amount'],
    #         iban=account['IBAN'])
    #     )
    #
    transactions = obp_api.get_transactions(accounts[0]['bank_id'],
                                            accounts[0]['id'],
                                            view='owner')
    return transactions


def save_model(_model):
    json_string = _model.to_json()
    date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    open('model_architecture.json', 'w').write(
        json_string)
    _model.save_weights('model_weights.h5')


def load_model(path_to_architecture, path_to_weights, optimizer):
    _model = model_from_json(open(path_to_architecture).read())
    _model.load_weights(path_to_weights)
    print("Compiling the neural network...")
    _model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer)
    return _model


def train(X_train, Y_train):
    """Train model"""

    model = Sequential()
    # Stacking layers is as easy as .add():

    model.add(Dense(output_dim=64, input_dim=X_train.shape[1]))
    model.add(Activation("relu"))
    model.add(Dense(output_dim=Y_train.shape[1]))
    model.add(Activation("softmax"))

    # Once your model looks good, configure its learning process with .compile():
    model.compile(loss='categorical_crossentropy', optimizer='sgd',
                  metrics=['accuracy'])

    # You can now iterate on your training data in batches:
    model.fit(X_train, Y_train, nb_epoch=1000, batch_size=17)

    save_model(model)


def test(model, X_test, Y_test):
    """Test model """
    # Evaluate your performance in one line:
    loss_and_metrics = model.evaluate(X_test, Y_test, batch_size=17)
    print("Loss and metrics: {}".format(loss_and_metrics))

    # Or generate predictions on new data:
    classes = model.predict_classes(X_test, batch_size=17)
    proba = model.predict_proba(X_test, batch_size=17)

    return classes, proba


if __name__ == '__main__':
    # get data
    # cluster
    transactions = get_test_data()
    X_train = np.array([features.create_cluster_features([t]) for t in transactions])

    Y_train = np.zeros((13,1))
    Y_train[0:5] = 1
    Y_train = np.hstack((Y_train, 1 - Y_train))

    X_train =  StandardScaler().fit_transform(X_train)
    # print(X_train)

    model = train(X_train, Y_train)





