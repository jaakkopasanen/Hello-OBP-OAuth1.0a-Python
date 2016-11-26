import calendar

import numpy as np
from dateutil.relativedelta import relativedelta
import datetime
from TransactionManager import TransactionManager
from datetime_utils import time_spread
import random

enable_debugging = True

tm = TransactionManager()


def debug(message):
    if enable_debugging:
        print(message)


def add_months_to_datetime(source_date, months):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day, hour=source_date.hour,
                             second=source_date.second)


def create_monthly_transactions(first_transaction_time, end_of_occurrences, description, transaction_type, amount,
                                this_account_id, other_account_id):
    """ Generates monthly transactions

    Creates transaction timestamps by incrementing first_transaction_time
    by one month until end_of_occurrences is reached
    """

    if first_transaction_time > end_of_occurrences:
        raise ValueError("End time should be later than start time")

    # manager = TransactionManager()

    # increment current_time by one month until end time (end_of_occurrences)
    # has been reached
    current_time = first_transaction_time
    while current_time < end_of_occurrences:
        current_time = add_months_to_datetime(current_time, 1)
        current_time = time_spread(current_time, 1, -2, 2)
        debug("Monthly occurrence time: {}".format(current_time))
        tm.create_transaction(current_time, description, transaction_type, amount, this_account_id, other_account_id)


def create_daily_transaction(prob, day, hour, minute, hour_spread, description, this_account_id, other_account_id):
    if random.random() < 1 - prob:
        debug('Skipped {}'.format(description))
        return 0
    completed = day.replace(hour=hour, minute=minute)
    completed = time_spread(completed, hour_spread)
    amount = 8 + random.random() * 2  # TODO
    tm.create_transaction(completed, description, '10218', amount, this_account_id, other_account_id)
    debug('{desc} created for {amount}'.format(desc=description, amount=amount))
    return amount


def create_transactions(params):
    # Generate monthly transactions
    for mt in params['monthly_transactions']:  # Create all monthly transactions
        t_parts = mt['time'].split(':')  # Split time
        t = params['start_time'].replace(day=mt['day'], hour=int(t_parts[0]), minute=int(t_parts[1]))  # Set time
        create_monthly_transactions(t, params['end_time'], description=mt['description'], transaction_type='2',
                                    amount=mt['amount'], this_account_id=params['this_account'],
                                    other_account_id=mt['other_account'])

    # Generate daily transactions
    d = params['start_time']
    day_spending = 0
    month_spending = 0
    while d < params['end_time']:
        day_spending = 0  # Reset day spending
        if d.day == 1:
            month_spending = 0  # Reset month spending at the beginning of month
        for dt in params['daily_transactions']:  # Create all daily transactions
            t_parts = dt['time'].split(':')  # Split time
            amount = create_daily_transaction(dt['prob'], d, int(t_parts[0]), int(t_parts[1]), dt['hour_spread'],
                                              dt['description'], params['this_account'],
                                              random.choice(dt['other_accounts']))
            day_spending += amount  # Increase day spending
        # next day
        month_spending += day_spending  # Add day spending total to month spending
        d = d + relativedelta(days=1)  # Next day


if __name__ == '__main__':

    users = [{
        'start_time': datetime.datetime(2015, 11, 1, 16, 55, 0),
        'end_time': datetime.datetime(2015, 11, 1, 16, 55, 0) + relativedelta(years=1, days=1),
        'this_account': '1',
        'monthly_transactions': [
            {'description': 'salary', 'day': 15, 'time': '10:00', 'amount': 2000, 'other_account': '21'},
            {'description': 'rent', 'day': 2, 'time': '18:14', 'amount': -500, 'other_account': '22'},
            {'description': 'public transportation', 'day': 8, 'time': '12:05', 'amount': -29.9, 'other_account': '23'},
            {'description': 'internet', 'day': 27, 'time': '20:01', 'amount': -15, 'other_account': '24'},
        ],
        'daily_transactions': [
            {'description': 'breakfast', 'prob': 0.1, 'time': '09:00', 'hour_spread': 0.2, 'other_accounts': ['25', '26']},
            {'description': 'lunch', 'prob': 0.8, 'time': '11:20', 'hour_spread': 0.2, 'other_accounts': ['27', '28', '29']}
        ]
    }]

    for user in users:
        create_transactions(user)

    tm.save('./tm.json')
