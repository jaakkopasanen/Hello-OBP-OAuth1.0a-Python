import json
from copy import copy


class TransactionManager:
    def __init__(self):
        self.accounts = {}
        self.n_transactions = 0;

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
        if type(completed) == str:
            d = completed
        else:
            d = completed.strftime('%Y-%m-%dT%H:%M:%SZ')
        details = {
            'completed': d,
            'description': description,
            'posted': d,
            'type': str(transaction_type),
            'value': {'amount': str(amount), 'currency': 'EUR'}
        }
        transaction = {
            'details': details,
            'id': 'ea3c6ee0-0147-48c9-b6e2-{}'.format(str(self.n_transactions).zfill(11)),
            'account': {'id': str(this_account_id)},
            'counterparty': {'id': str(other_account_id)}
        }
        if this_account_id in self.accounts:
            self.accounts[this_account_id].append(transaction)
        else:
            self.accounts[this_account_id] = [transaction]
        self.n_transactions += 1
        return transaction

    def save(self, path):
        """Writes transactions to a JSON file"""
        json_data = json.dumps(self.accounts, indent=4)
        with open(path, 'w+') as f:
            f.write(json_data)

    def load(self, path):
        """Loads transactions from a JSON file"""
        with open(path) as f:
            self.accounts = json.loads(f.read())
