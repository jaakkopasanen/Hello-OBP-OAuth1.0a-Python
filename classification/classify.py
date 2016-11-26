from sklearn.preprocessing import StandardScaler
import numpy as np
from classification import features
import keras
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Dense, Activation

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


def train(X_train, Y_train):
    """Train model"""
    model = Sequential()
    # Stacking layers is as easy as .add():

    model.add(Dense(output_dim=64, input_dim=X_train.shape[1]))
    model.add(Activation("relu"))
    model.add(Dense(output_dim=2))
    model.add(Activation("softmax"))

    # Once your model looks good, configure its learning process with .compile():
    model.compile(loss='categorical_crossentropy', optimizer='sgd',
                  metrics=['accuracy'])

    # If you need to, you can further configure your optimizer. A core principle of Keras is to make things reasonably simple, while allowing the user to be fully in control when they need to (the ultimate control being the easy extensibility of the source code).
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

    # You can now iterate on your training data in batches:
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)

    return model


def test(model, X_test, Y_test):
    """Test model """
    # Evaluate your performance in one line:
    loss_and_metrics = model.evaluate(X_test, Y_test, batch_size=32)
    print("Loss and metrics: {}".format(loss_and_metrics))

    # Or generate predictions on new data:
    classes = model.predict_classes(X_test, batch_size=32)
    proba = model.predict_proba(X_test, batch_size=32)

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





