import numpy as np
import dateutil.parser

def get_transaction_weekday(transaction):
    date_string = transaction['details']['completed']
    return dateutil.parser.parse(date_string).weekday()


def create_cluster_features(transactions):
    feats = []
    # mean and std of transaction amount

    print([t['details']['value']['amount'] for t in transactions])

    mean = np.array([t['details']['value']['amount'] for t in transactions]).mean()
    feats.append(mean)
    std = np.array([t['details']['value']['amount'] for t in transactions]).std()
    feats.append(std)

    # percentage of weekdays and weekend days
    days = [get_transaction_weekday(t) for t in transactions]
    weekends = np.array(days) > 4
    weekdays = np.array(days) <= 4
    weekends_ratio = weekends.sum() / weekends.shape[0]
    weekdays_ratio = weekdays.sum() / weekdays.shape[0]
    print(weekdays_ratio)
    print(weekends_ratio)

if __name__ == '__main__':
    from pprint import pprint
    from ObpApi.api_credentials import *
    from ObpApi.ObpApi import ObpApi
    from test_users import TEST_USERS

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
    login_success = obp_api.login_direct(user['username'], user['password'])
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
                                            accounts[0]['id'], view='owner')
    print(transactions)
    create_cluster_features(transactions)
