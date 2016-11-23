from pprint import pprint
from api_credentials import *
from ObpApi import ObpApi
from test_users import TEST_USERS

user = TEST_USERS[0]

obp_api = ObpApi(
    host='https://op.openbankproject.com',
    version='2.1.0',
    direct_login_url='/my/logins/direct',
    oauth_url='/oauth',
    oauth_callback_url='http://localhost',
    consumer_key=OBP_CONSUMER_KEY,
    consumer_secret=OBP_CONSUMER_SECRET
)

obp_api.login_direct(user['username'], user['password'])
# obp_api.initiate_oauth()
accounts = obp_api.get_all_private_accounts()
#for acc in accounts:
#    account = obp_api.get_account(acc['bank_id'], acc['id'], 'owner')
#    print('{currency} {amount} @ {iban}'.format(currency=account['balance']['currency'], amount=account['balance']['amount'], iban=account['IBAN']))

transactions = obp_api.get_transactions_core(accounts[0]['bank_id'], accounts[0]['id'], view='owner')
pprint(transactions[0])
