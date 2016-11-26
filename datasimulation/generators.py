import calendar

import numpy as np
from dateutil.relativedelta import relativedelta
import datetime
from TransactionManager import TransactionManager
from datetime_utils import time_spread
import random
import json

enable_debugging = False

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


def create_daily_transaction(prob, day, hour, minute, hour_spread, description, amount, this_account_id, other_account_id):
    if random.random() < 1 - prob:
        debug('Skipped {}'.format(description))
        return 0
    completed = day.replace(hour=hour, minute=minute)
    completed = time_spread(completed, hour_spread)
    am = amount * (0.9 + 0.2*random.random())  # TODO
    tm.create_transaction(completed, description, '10218', am, this_account_id, other_account_id)
    debug('{desc} created for {amount}'.format(desc=description, amount=amount))
    return amount


def create_transactions(params):
    # Parse start time and end time
    start_time = datetime.datetime.strptime(params['start_time'], '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.datetime.strptime(params['end_time'], '%Y-%m-%dT%H:%M:%SZ')
    # Generate monthly transactions
    static_spendings = 0
    for mt in params['monthly_transactions']:  # Create all monthly transactions
        t_parts = mt['time'].split(':')  # Split time
        t = start_time.replace(day=mt['day'], hour=int(t_parts[0]), minute=int(t_parts[1]))  # Set time
        create_monthly_transactions(t, end_time, description=mt['description'], transaction_type='2',
                                    amount=mt['amount'], this_account_id=params['this_account'],
                                    other_account_id=mt['other_account'])
        static_spendings += mt['amount']
    print('Static spendings are {} €'.format(static_spendings))

    # Generate daily transactions
    d = start_time
    day_spending = 0
    month_spending = 0
    while d < end_time:

        # print('Spent {} € yesterday'.format(day_spending))
        day_spending = 0  # Reset day spending
        if d.day == 1:
            print('Spent {} € last month'.format(month_spending + static_spendings))
            month_spending = 0  # Reset month spending at the beginning of month

        for dt in params['daily_transactions']:  # Create all daily transactions
            t_parts = dt['time'].split(':')  # Split time
            amount = create_daily_transaction(dt['prob'], d, int(t_parts[0]), int(t_parts[1]), dt['hour_spread'],
                                              dt['description'], dt['amount'], params['this_account'],
                                              random.choice(dt['other_accounts']))
            day_spending += amount  # Increase day spending

        # next day
        month_spending += day_spending  # Add day spending total to month spending
        d = d + relativedelta(days=1)  # Next day


if __name__ == '__main__':

    with open('./simulated_users.json') as f:
        users = json.loads(f.read())

    for user in users:
        create_transactions(user)

    tm.save('./tm.json')
