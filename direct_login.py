# -*- coding: utf-8 -*-

# Note: in order to use this example, you need to have at least one account

import sys
import requests
from pprint import pprint

from settings import *
from test_users import TEST_USERS
from api_credentials import OBP_CONSUMER_KEY


# Helper function to merge headers
def merge(x, y):
    z = x.copy()
    z.update(y)
    return z

# Our account's bank
our_bank = 'obp-bankx-n'

# User account
user = TEST_USERS[0]
# user = None
if user is None:
    _username = input('username')
    _password = input('password')
    user = {
        'user_name': _username,
        'password': _password,
        'email': _username
    }

login_header = {
    'Authorization': 'DirectLogin username="{un}",password="{pw}",consumer_key="{ck}"'.format(
        un=user['user_name'],
        pw=user['password'],
        ck=OBP_CONSUMER_KEY
    )
}

# Login and receive authorized token
print('Login as {login_header} to {login_endpoint}'.format(
    login_header=login_header,
    login_endpoint=OBP_DIRECT_LOGIN_ENDPOINT)
)
response = requests.get(OBP_DIRECT_LOGIN_ENDPOINT, headers=login_header)

if response.status_code != 200:
    print('error: could not login')
    sys.exit(0)

# Login OK - create authorization headers
token = response.json()['token']
print('Received token: {0}'.format(token))

# Prepare headers
directlogin = {'Authorization': 'DirectLogin token={token}'.format(token=token)}
content_json = {'content-type': 'application/json'}
limit = {'obp_limit': '25'}

# Send hello message
response = requests.get(OBP_API_BASE_URL, headers=directlogin)

if response.status_code == 200:
    print('Success JSON:')
    pprint(response.json())
else:
    print(response.text)
