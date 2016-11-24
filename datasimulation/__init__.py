from datetime import datetime

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def get_random_hour_of_day(n_hours=1000, visualize=False):
    transactions_per_hour = np.array([
        # Taken from BI348Chapter02Finished.xlsx, sheet: Time Histogram
        # Created from 26524 Boomerang Inc online sales transactions
        # https://people.highline.edu/mgirvin/excelisfun.htm
        # https://www.youtube.com/watch?v=3YeoX1Cl7Og
        219, 234, 1579, 1813, 1773, 984, 226, 211, 213, 341, 966, 4062, 4174,
        1962, 337, 318, 975, 2025, 2094, 934, 333, 249, 246, 256])
    hour_probas = np.round(
        transactions_per_hour.astype(float) / transactions_per_hour.sum(),
        decimals=3)
    if visualize:
        ax = plt.figure().add_subplot(111)
        ax.bar(range(len(hour_probas)), hour_probas)
        ax.set_xlim((0, len(hour_probas)))
        ax.set_xticks(range(len(hour_probas)))
        ax.set_ylabel('Probability of transaction')
        ax.set_xlabel('Hour')
        plt.show()
    return np.random.choice(
        a=len(transactions_per_hour), size=n_hours,
        # p = The probabilities associated with each entry in a
        p=hour_probas)


def get_random_weekday(n_days=1000, visualize=False):
    sales_per_weekday = np.array([
        # Taken from http://g3cfo.com/little-fun-simple-flash-report/
        # Created from restaurant sales
        10237, 8365, 9018, 9547, 13313, 19055, 17660])
    weekday_probas = np.round(
        sales_per_weekday.astype(float) / sales_per_weekday.sum(), decimals=3)
    if visualize:
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)
        ax = fig.add_subplot(111)
        ax.bar(range(len(weekday_probas)), weekday_probas)
        ax.set_xlim((0, len(weekday_probas)))
        ax.set_xticks(range(len(weekday_probas)))
        ax.set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                            'Friday', 'Saturday', 'Sunday'],
                           rotation=45, ha='left')
        ax.set_ylabel('Probability of transaction')
        ax.set_xlabel('Day of week')
        plt.show()
    return np.random.choice(
        a=len(sales_per_weekday), size=n_days,
        # p = The probabilities associated with each entry in a
        p=weekday_probas)


def simulate(n_persons=100,
             start_time=datetime(year=2010, month=01, day=01),
             end_time=datetime(year=2016, month=01, day=01)):
    random_hours = get_random_hour_of_day(n_hours=n_persons)
    random_weekdays = get_random_weekday(n_days=n_persons)

    # For debugging purposes, plot the sampled data
    for sampled_data in [random_hours, random_weekdays]:
        ax = plt.figure().add_subplot(111)
        _, unique_counts = np.unique(sampled_data, return_counts=True)
        ax.bar(range(len(unique_counts)), unique_counts)
        plt.show()
