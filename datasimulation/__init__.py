from datetime import datetime
from collections import OrderedDict

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Commodity:
    def __init__(self):
        pass
    food = "Food & non-alcoholic drinks"
    alcohol_tobacco = "Alcoholic drinks, tobacco & narcotics"
    clothing = "Clothing & footwear"
    housing = "Housing (net), fuel & power"
    household = "Household goods & services"
    health = "Health"
    transport = "Transport"
    communication = "Communication"
    recreation_culture = "Recreation & culture"
    education = "Education"
    restaurants_hotels = "Restaurants & hotels"
    misc_goods = "Miscellaneous goods & services"
    other = "Other expenditure items"

COMMODITIES = [Commodity.food, Commodity.alcohol_tobacco, Commodity.clothing,
               Commodity.housing, Commodity.household, Commodity.health,
               Commodity.transport, Commodity.communication,
               Commodity.recreation_culture, Commodity.education,
               Commodity.restaurants_hotels, Commodity.misc_goods,
               Commodity.other]


class AgeGroup:
    def __init__(self, name, commodity_probas):
        self.name = name
        self.commodity_probas = commodity_probas


class AgeGroups:
    def __init__(self):
        pass
    # Data source:
    # http://tinyurl.com/hyot8qu
    # http://tinyurl.com/jjz6x36
    # Data description: Table A10 - Household expenditure as a percentage of
    # total expenditure by age of household reference person, 2012
    # Note: The one who prepared the data has rounded percentages to integers,
    # which leads to a situation where the sum of percentages won't sum up to
    # 100. We can fix this by dividing the array by the sum of elements
    # in the array.
    less_than_30 = AgeGroup(name="Less than 30",
                            commodity_probas=OrderedDict(zip(COMMODITIES, [
                                9, 2, 5, 24, 5, 0, 12, 3, 10, 3, 9, 7, 11])))
    from_30_to_49 = AgeGroup(name="30 to 49",
                             commodity_probas=OrderedDict(zip(COMMODITIES, [
                                 11, 2, 5, 13, 5, 1, 13, 3, 12, 2, 8, 8, 16])))
    from_50_to_64 = AgeGroup(name="50 to 64",
                             commodity_probas=OrderedDict(zip(COMMODITIES, [
                                 12, 3, 5, 11, 6, 1, 14, 3, 13, 1, 9, 8, 13])))
    from_65_to_74 = AgeGroup(name="65 to 74",
                             commodity_probas=OrderedDict(zip(COMMODITIES, [
                                 14, 3, 4, 12, 6, 2, 13, 3, 16, 1, 8, 8, 11])))
    more_than_75 = AgeGroup(name="75 or over",
                            commodity_probas=OrderedDict(zip(COMMODITIES, [
                                15, 2, 3, 16, 7, 4, 9, 3, 11, 0, 7, 9, 12])))

    @staticmethod
    def get_all_age_groups():
        all_vars = []
        for _, var in vars(AgeGroups).items():
            if isinstance(var, AgeGroup):
                all_vars.append(var)
        return all_vars


def visualize_spending_per_age_group():
    # Put the data to Pandas DataFrame
    age_groups_df = pd.DataFrame()
    for g in AgeGroups.get_all_age_groups():
        probas = np.array(list(g.commodity_probas.values()))
        age_groups_df[g.name] = probas/probas.sum() * 100.0
    # Sort the columns in right order
    age_groups_df = age_groups_df[[
        AgeGroups.less_than_30.name, AgeGroups.from_30_to_49.name,
        AgeGroups.from_50_to_64.name, AgeGroups.from_65_to_74.name,
        AgeGroups.more_than_75.name]]
    # Visualize
    age_groups_df = age_groups_df.transpose()
    ax = age_groups_df.plot.bar(
        stacked=True, legend='reverse',
        colormap='Spectral', rot=0, figsize=(10, 7))
    ax.set_ylim((0, 100))
    ax.set_ylabel("Proportion (%)", fontsize=10)
    ax.set_xlabel("Age group", fontsize=10)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], COMMODITIES[::-1], title='Commodities',
              loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.7)
    # plt.savefig('spending_per_age_group.png')


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
             start_time=datetime(year=2010, month=1, day=1),
             end_time=datetime(year=2016, month=1, day=1)):
    random_hours = get_random_hour_of_day(n_hours=n_persons)
    random_weekdays = get_random_weekday(n_days=n_persons)

    # For debugging purposes, plot the sampled data
    for sampled_data in [random_hours, random_weekdays]:
        ax = plt.figure().add_subplot(111)
        _, unique_counts = np.unique(sampled_data, return_counts=True)
        ax.bar(range(len(unique_counts)), unique_counts)
        plt.show()
