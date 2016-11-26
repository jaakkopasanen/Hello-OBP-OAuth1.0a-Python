from ObpApi.ObpApi import ObpApi
from datasimulation.TransactionManager import TransactionManager
from ObpApi.api_credentials import *
from test_users import TEST_USERS

from pprint import pprint
import seaborn as sns
import matplotlib.pyplot as plt


obp_api = ObpApi(
    host='https://op.openbankproject.com',
    version='2.1.0',
    direct_login_url='/my/logins/direct',
    oauth_url='/oauth',
    oauth_callback_url='http://localhost',
    consumer_key=OBP_CONSUMER_KEY,
    consumer_secret=OBP_CONSUMER_SECRET)

# Get all TEST_USERS transactions from public & private accounts
#  - Produces transactions for 77 accounts
transactions = []
for user in TEST_USERS:
    login_success = obp_api.login_direct(user['username'], user['password'])
    accounts = obp_api.get_accounts_at_all_banks()['accounts']
    for acc in accounts:
        t = obp_api.get_transactions(bank_id=acc['bank_id'],
                                     account=acc['id'])
        if t:
            transactions.append(t)

# Get amount of each transaction
all_acc_all_trans_amounts = []
for tt in transactions:
    acc_trans_amounts = []
    for t in tt:
        acc_trans_amounts.append(t['details']['value']['amount'])
    all_acc_all_trans_amounts.append(acc_trans_amounts)
    print(len(acc_trans_amounts))

# Visualize number of transactions per account
ax = plt.figure().add_subplot(111)
ax.bar(range(len(all_acc_all_trans_amounts)),
       [len(i) for i in all_acc_all_trans_amounts])
ax.set_title('Number of transactions per account (public + private)')
ax.set_xlabel('Account')
ax.set_ylabel('Nr of transactions')
plt.savefig('nr_of_transactions_per_account.png')

# Visualize transaction amounts for each account
fig = plt.figure(figsize=(8, 12))
for i, person in enumerate(all_acc_all_trans_amounts, start=1):
    ax = fig.add_subplot(12, 7, i)
    ax.plot(range(len(person)), person)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
plt.tight_layout()
plt.savefig('transactions_per_account.png')
