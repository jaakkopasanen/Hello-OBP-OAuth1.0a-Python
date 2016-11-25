import json
from copy import copy


class TransactionManager:
    def __init__(self):
        self.accounts = {}
        self.transactions = {}

    def create_transaction(self, completed, description, transaction_type, amount, this_account_id, other_account_id):
        """Generates transaction as a dict as per ObpApi transaction

        Args:
            completed: ISO8601 date in UTC as a string. e.g. '2016-11-12T09:14:99Z'
            description: Transaction description
            transaction_type: Transaction type id as per Obp API
            amount: Transaction amount in Euros
            this_account_id: ID of this account
            other_account_id: ID of the other account

        Returns:
            Generated transaction
        """
        new_balance = self.accounts[this_account_id]['balance']['amount'] + amount
        details = {
            'completed': completed,
            'description': description,
            'new_balance': {'amount': new_balance, 'currency': 'EUR'},
            'posted': completed,
            'type': transaction_type,
            'value': {'amount': amount, 'currency': 'EUR'}
        }
        transaction = {
            'details': details,
            'id': 'ea3c6ee0-0147-48c9-b6e2-{}'.format(str(len(self.transactions)).zfill(11)),
            'metadata': {
                'comments': [],
                'images': [],
                'narrative': None,
                'tags': [],
                'where': None
            },
            'this_account': copy(self.accounts[this_account_id]),
            'other_account': copy(self.accounts[other_account_id])
        }
        self.transactions[transaction['id']] = transaction  # Save transaction
        self.accounts[this_account_id]['balance']['amount'] = new_balance  # Update balance
        return transaction

    def save(self, path):
        """Writes transactions and accounts to a JSON file"""
        json_data = json.dumps({
            'accounts': self.accounts,
            'transactions': self.transactions
        })
        with open(path) as f:
            f.write(json_data)

    def load(self, path):
        """Loads transactions and accounts from a JSON file"""
        with open(path) as f:
            data = json.loads(f.read())
            self.transactions = data['transactions']
            self.accounts = data['accounts']
