# -*- coding: utf-8 -*-
"""
Settings for the hello scripts.

You most likely need to edit a few of them, e.g. API_HOST and the OAuth
credentials.
"""

# Get the OAuth credentials prior from the API, e.g.
# https://apisandbox.openbankproject.com/consumer-registration

OBP_APPLICATION_TYPE = 'Web'
OBP_APPLICATION_NAME = 'Ultimate.ai'
OBP_DEVELOPER_EMAIL = 'reetu@ultimate.ai'
OBP_APP_DESCRIPTION = 'MVP for Ultrahack 2016'
OBP_API_HOST = 'https://op.openbankproject.com'
OBP_API_VERSION = '2.1.0'
OBP_API_BASE_URL = '{host}/obp/v{version}'.format(host=OBP_API_HOST, version=OBP_API_VERSION)
OBP_OAUTH_ENDPOINT = 'https://op.openbankproject.com/oauth/initiate'
OBP_OAUTH_CALLBACK_URL = 'http://localhost'
OBP_DIRECT_LOGIN_ENDPOINT = 'https://op.openbankproject.com/my/logins/direct'
