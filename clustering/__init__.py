from pprint import pprint

from sklearn.cluster import DBSCAN
import pandas as pd

from ObpApi.ObpApi import ObpApi
from ObpApi.api_credentials import *
from test_users import TEST_USERS


def get_api():
    return ObpApi(
        host='https://op.openbankproject.com',
        version='2.1.0',
        direct_login_url='/my/logins/direct',
        oauth_url='/oauth',
        oauth_callback_url='http://localhost',
        consumer_key=OBP_CONSUMER_KEY,
        consumer_secret=OBP_CONSUMER_SECRET)


def get_all_transaction_data(users, obp_api):
    # Get all TEST_USERS transactions from public & private accounts
    #  - Produces transactions for 77 accounts
    transactions = []
    for user in users:
        login_success = obp_api.login_direct(user['username'],
                                             user['password'])
        if not login_success:
            continue
        accounts = obp_api.get_accounts_at_all_banks()['accounts']
        for acc in accounts:
            t = obp_api.get_transactions(bank_id=acc['bank_id'],
                                         account=acc['id'])
            if t:
                transactions.append(t)
    return transactions


def get_transaction_amount(transaction):
    if transaction['details']['value']['currency'].strip().upper() == 'EUR':
        return transaction['details']['value']['amount']
    else:
        raise(Exception("Unknown currency: %s" %
                        transaction['details']['value']['currency']))


def get_transaction_description(transaction):
    descr = transaction['details']['description']
    if descr and descr is not None:
        return descr
    else:
        return ''


def user_transactions_to_data_matrix(user_transactions):
    df_all = pd.DataFrame()
    for transaction in user_transactions:
        row_transaction = pd.DataFrame({
            'amount': get_transaction_amount(transaction),
            'description': get_transaction_description(transaction),
            'counterparty_id': transaction['counterparty']['id'],
        }, index=[transaction['account']['id']])
        df_all = df_all.append([row_transaction], ignore_index=False)


def cluster_transactions(user_transactions):
    data_matrix = user_transactions_to_data_matrix(user_transactions)


if __name__ == '__main__':
    obp_api = get_api()
    users_transactions = get_all_transaction_data(users=TEST_USERS,
                                                  obp_api=obp_api)
    cluster_transactions(user_transactions=users_transactions[0])

