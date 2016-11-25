import calendar

import numpy as np
from dateutil.relativedelta import relativedelta
import datetime
from TransactionManager import TransactionManager

enable_debugging = True

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


def monthly_transactions(first_transaction_time, end_of_occurrences,
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
        debug("Monthly occurrence time: {}".format(current_time))
        # manager.create_transaction(monthly_occurrence_time,
        #                                       description,
        #                                       transaction_type,
        #                                       amount,
        #                                       this_account_id,
        #                                       other_account_id)


if __name__ == '__main__':
    # generate monthly payments of 500€ over two year period
    now = datetime.datetime.now()
    year_from_now = now - relativedelta(years=-1)
    year_ago = now - relativedelta(years=1)
    monthly_transactions(now, year_from_now, description="desc",
                         transaction_type=1, amount=-500,
                         this_account_id=10101,
                         other_account_id=101)
