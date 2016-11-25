# -*- coding: utf-8 -*-

import requests
from copy import copy


class ObpApi:
    def __init__(self, host='https://op.openbankproject.com', version='2.1.0',
                 direct_login_url='/my/logins/direct', oauth_url='/oauth',
                 oauth_callback_url='http://localhost', consumer_key='', consumer_secret=''):
        self.host = host
        self.version = version
        self.base_url = '{host}/obp/v{version}'.format(host=self.host, version=self.version)
        self.direct_login_url = '{host}{url}'.format(host=self.host, url=direct_login_url)
        self.oauth_url = '{host}{url}'.format(host=host, url=oauth_url)
        self.oauth_callback_url = oauth_callback_url

        assert consumer_key, 'No consumer key provided'
        assert consumer_secret, 'No consumer secret provided'
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.auth_method = None
        self._direct_login = {}
        self._oauth = None

    def login_direct(self, username, password):
        """Performs a direct login."""

        # Authorization header
        auth = 'DirectLogin username="{un}",password="{pw}",consumer_key="{ck}"'.format(
            un=username,
            pw=password,
            ck=self.consumer_key
        )
        headers = {'Authorization': auth}

        # Do the login request
        res = requests.get(self.direct_login_url, headers=headers)

        # Handle response
        if res.status_code == 200:
            # Login success
            token = res.json()['token']
            # Save authorization details
            self._direct_login = {'Authorization': 'DirectLogin token={token}'.format(token=token)}
            self.auth_method = 'direct'
            return True

        # Login failed
        return False

    def initiate_oauth(self):
        """Initiates the OAuth authorisation returns an API session object."""

        from requests_oauthlib import OAuth1Session

        request_token_url = '{}/initiate'.format(self.oauth_url)
        authorization_url = '{}/authorize'.format(self.oauth_url)
        access_token_url = '{}/token'.format(self.oauth_url)

        # initiate Oauth by fetching request token
        api = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret,
                            callback_uri=self.oauth_callback_url)
        api.fetch_request_token(request_token_url)

        # ask user to visit authorization URL and paste response
        authorization_url = api.authorization_url(authorization_url)
        print('Please visit this URL and authenticate/authorise:')
        print(authorization_url)
        redirect_response = input('Paste the full redirect URL here: ')

        # parse authorization response (contains callback_uri) and access token
        api.parse_authorization_response(redirect_response)
        api.fetch_access_token(access_token_url)
        self._oauth = api
        self.auth_method = 'oauth'

    def _request(self, url, method='GET', headers=None, json_data=None):
        """Creates HTTP request to API endpoint."""

        if self.auth_method == 'direct':
            # Add direct login authentication headers
            if headers is not None:
                # Merge custom headers with direct login headers
                all_headers = copy(self._direct_login)
                all_headers.update(headers)
            else:
                all_headers = self._direct_login
            # HTTP method functions from requests module
            methods = {
                'GET': requests.get,
                'POST': requests.post,
                'PUT': requests.put,
                'DELETE': requests.delete
            }
        elif self.auth_method == 'oauth':
            # Custom headers only
            all_headers = headers
            # HTTP method functions from oauth
            methods = {
                'GET': self._oauth.get,
                'POST': self._oauth.post,
                'PUT': self._oauth.put,
                'DELETE': self._oauth.delete
            }
        else:
            # Invalid authentication method
            raise ValueError('Invalid auth method: {}'.format(self.auth_method))

        method = methods[method]
        if all_headers:
            if json_data:
                res = method(self.base_url + url, headers=all_headers, json=json_data)
            else:
                res = method(self.base_url + url, headers=all_headers)
        else:
            if json_data:
                res = method(self.base_url + url, json=json_data)
            else:
                res = method(self.base_url + url)

        return res

    def hello(self, quiet=False):
        """Tests API endpoint."""

        # HTTP GET with direct login authorization
        res = self._request('')
        if not quiet:
            print('API response {}'.format(res.status_code))  # Print response
        if res.status_code == 200:
            return True
        else:
            return False

    def import_data(self, data):
        """Dumps users, accounts banks etc. into this sandbox environment"""

        res = self._request('/sandbox/data-import', method='POST', json_data=data)
        return res

    # Banks
    # ----------------------------------------------------------------------------------------------
    def get_banks(self):
        """Retrieves basic info for all the banks supported by the host server"""

        res = self._request('/banks')
        return res.json()['banks']

    def get_bank(self, bank_id):
        """Retrieves basic info about a bank"""
        url = '/banks/{}'.format(bank_id)
        res = self._request(url)
        return res.json()

    # Users
    # ----------------------------------------------------------------------------------------------
    def get_consumers(self):
        """Retrieves all consumers

        CanGetConsumers entitlement required
        """

        res = self._request('/management/consumers')
        return res.json()

    def get_consumer(self, consumer_id):
        """Retrieves a consumer by consumer ID

        CanGetConsumers entitlement required
        """

        url = '/management/consumers/{}'.format(consumer_id)
        res = self._request(url)
        return res.json()

    def get_customers_for_current_user(self):
        """Retrieves infos for all customer objects of current user"""

        res = self._request('/users/current/customers')
        return res.json()['customers']

    def get_current_user(self):
        """Retrieves info about current user"""

        res = self._request('/users/current')
        return res.json()

    def get_users(self):
        """Retrieves all users

        CanGetAnyUser entitlement required
        """

        res = self._request('/users')
        return res.json()

    def get_entitlements(self, user_id, bank_id=None):
        """Retrieves entitlements for user in a bank

        CanGetEntitlementsForAnyUserAtOneBank or
        CanGetEntitlementsForAnyUserAtAnyBank entitlements required
        """

        if bank_id is not None:
            url = '/banks/{bank}/users/{user}/entitlements'.format(bank=bank_id, user=user_id)
        else:
            url = '/users/{}/entitlements'.format(user_id)
        res = self._request(url)
        return res.json()

    # Accounts
    # ----------------------------------------------------------------------------------------------
    def get_account(self, bank_id, account_id, view):
        """Retrieves info for a bank account redacted by a view"""

        url = '/banks/{bank}/accounts/{account}/{view}/account'.format(
            bank=bank_id, account=account_id, view=view)
        res = self._request(url)
        return res.json()

    def get_all_private_accounts(self):
        """Retrieves all private accounts for current user"""

        url = '/my/accounts'
        res = self._request(url)
        return res.json()

    # Views
    # ----------------------------------------------------------------------------------------------
    def get_views(self, bank_id, account_id):
        """Retrieves views for given account_id in given bank_id"""

        url = '/banks/{bank}/accounts/{account}/views'.format(bank=bank_id, account=account_id)
        res = self._request(url)
        return res.json()['views']

    # Transactions
    # ----------------------------------------------------------------------------------------------
    def get_transactions(self, bank_id, account, view=None, sort_by=None, sort_direction=None,
                         limit=None, offset=None, from_date=None, to_date=None):
        """Retrieves transactions for given account in given bank_id"""

        if view is not None:
            url = '/banks/{bank}/accounts/{account}/{view}/transactions'.format(
                bank=bank_id, account=account, view=view)
        else:
            url = '/my/banks/{bank}/accounts/{account}/transactions'.format(
                bank=bank_id, account=account)

        headers = {}
        if sort_by is not None:
            headers['obp_sort_by'] = sort_by
        if sort_direction is not None:
            headers['obp_sort_direction'] = sort_direction
        if limit is not None:
            headers['obp_limit'] = str(limit)
        if offset is not None:
            headers['obp_offset'] = str(offset)
        if from_date is not None:
            headers['obp_from_date'] = from_date
        if to_date is not None:
            headers['obp_to_date'] = to_date
        res = self._request(url, headers=headers)
        return res.json()['transactions']
