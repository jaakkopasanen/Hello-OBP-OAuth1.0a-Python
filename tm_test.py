from ObpApi.ObpApi import ObpApi
from datasimulation.TransactionManager import TransactionManager
from ObpApi.api_credentials import *
from test_users import TEST_USERS

tm = TransactionManager()

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
login_success = obp_api.login_direct(user['username'], user['password'])
accounts = obp_api.get_all_private_accounts()
this_account = accounts[-2]
that_account = accounts[-3]

