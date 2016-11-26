import numpy as np
import dateutil.parser

def get_transaction_weekday(transaction):
    print("Extracting weekday of transaction...")
    date_string = transaction['details']['posted']
    return dateutil.parser.parse(date_string).weekday()

def get_transaction_month(transaction):
    print("Extracting month of transaction...")
    date_string = transaction['details']['posted']
    return dateutil.parser.parse(date_string).month

def get_transaction_hour(transaction):
    print("Extracting hour of transaction...")
    date_string = transaction['details']['posted']
    return dateutil.parser.parse(date_string).hour

def get_transaction_balance(transaction):
    print("Extracting new balance of account after transaction...")
    return transaction['details']['new_balance']['amount']

def get_is_transaction_weekend(transaction):
    print("Determining whether transaction was made during weekend....")
    day_of_week = get_transaction_weekday(transaction)
    return day_of_week > 4



def create_cluster_features(transactions):
    print("Extracting features from cluster...")
    """
    Compute cluster features
    amount mean, amount std, hour average, hour std, month average,
    month std, day average, day std, percentage of weekdays,
    percentage of weekends
    """

    feats = []
    # amount statistics
    values = np.array([float(t['details']['value']['amount']) for t in transactions])
    mean = values.mean()
    std = values.std()
    print("Calculating mean of transaction amounts in cluster...")
    feats.append(mean)
    print("Calculating standard deviation of transaction amounts in cluster...")
    feats.append(std)

    # hour statistics
    hour_data = np.array([get_transaction_hour(t) for t in transactions])
    hour_average = hour_data.mean()
    hour_std = hour_data.std()
    print("Calculating average hour of transactions in cluster...")
    feats.append(hour_average)
    print("Calculating standard deviation of hour of transactions in cluster...")
    feats.append(hour_std)

    # month statistics
    month_data = np.array([get_transaction_month(t) for t in transactions])
    month_average = month_data.mean()
    month_std = month_data.std()
    print("Calculating average month of transactions in cluster...")
    feats.append(month_average)
    print("Calculating standard deviation of transaction month in cluster...")
    feats.append(month_std)

    # day statistics
    day_data = np.array([get_transaction_weekday(t) for t in transactions])
    day_average = day_data.mean()
    day_std = day_data.std()
    print("Calculating average transactions day in cluster...")
    feats.append(day_average)
    print("Calculating standard deviation of transaction day in cluster...")
    feats.append(day_std)

    # percentage of weekdays and weekend days
    weekends = day_data > 4
    weekdays = day_data <= 4
    weekends_ratio = weekends.sum() / weekends.shape[0]
    weekdays_ratio = weekdays.sum() / weekdays.shape[0]
    print("Calculating weekday/weekend ratio...")
    feats.append(weekdays_ratio)
    print("Calculating weekends/weekday ratio...")
    feats.append(weekends_ratio)

    n_descriptions = {}
    for transaction in transactions:
        if transaction['details']['description'] in n_descriptions:
            n_descriptions[transaction['details']['description']] += 1
        else:
            n_descriptions[transaction['details']['description']] = 1
    max_descr = None  # Description with most transactions
    for key, count in n_descriptions.items():
        if max_descr == None or count > n_descriptions[max_descr]:
            max_descr = key
    feats.append(max_descr)

    # new balances
    # new_balances = np.array([float(t['details']['new_balance']['amount']) for t in transactions])
    # new_balances_mean = new_balances.mean()
    # new_balances_std = new_balances.std()
    # feats.append(new_balances_mean)
    # feats.append(new_balances_std)

    # relative amounts
    # relative_amounts = values / new_balances
    # relative_amounts_average = relative_amounts.mean()
    # relative_amounts_std = relative_amounts.std()
    # feats.append(relative_amounts_average)
    # feats.append(relative_amounts_std)

    feats_names = ['amount_mean', 'amount_std', 'hours_mean', 'hours_std',
                   'month_mean', 'month_std', 'day_mean', 'day_std',
                   'weekdays_ratio', 'weekends_ratio']

    return np.array(feats), feats_names

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
    feats = create_cluster_features(transactions)
    print(feats)
