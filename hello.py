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
#obp_api.initiate_oauth()
obp_api.hello()
