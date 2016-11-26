import calendar

import numpy as np
from dateutil.relativedelta import relativedelta
import datetime
from TransactionManager import TransactionManager
from datetime_utils import time_spread

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


def create_monthly_transactions(first_transaction_time, end_of_occurrences,
                         description, transaction_type, amount,
                         this_account_id,
                         other_account_id):
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


if __name__ == '__main__':
    # generate monthly payments of 500€ over two year period
    start_time = datetime.datetime(2015, 11, 1, 16, 55, 0)
    end_time = start_time + relativedelta(years=1, days=1)
    create_monthly_transactions(start_time, end_time, description="desc",
                         transaction_type=1, amount=-500,
                         this_account_id='10101',
                         other_account_id='101')
    tm.save('./tm.json')
