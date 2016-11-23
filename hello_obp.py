#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script says hello to the OpenBankProject API

Configure settings.py to suit your needs.
"""

from pprint import pprint

from oauth_dance import get_api
from settings import OBP_API_BASE_URL


def say_hello():
    """Says hello to the API"""
    api = get_api()
    response = api.get(OBP_API_BASE_URL)
    status_code = response.status_code
    print('Status code: {}'.format(status_code))
    if status_code == 200:
        print('Success JSON:')
        pprint(response.json())
    else:
        print(response.text)


if __name__ == '__main__':
    say_hello()
