from datetime import datetime
import seaborn as sns

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from api_credentials import *

from ObpApi import ObpApi
from test_users import TEST_USERS


def price_fmt(x):
    return '{:1.2f} €'.format(x)

matplotlib.use('Gtk3Agg')

years = mdates.YearLocator()
months = mdates.MonthLocator()
days = mdates.DayLocator()
days_fmt = mdates.DateFormatter('%d.%m')

user = TEST_USERS[15]

obp_api = ObpApi(
    host='https://op.openbankproject.com',
    version='2.1.0',
    direct_login_url='/my/logins/direct',
    oauth_url='/oauth',
    oauth_callback_url='http://localhost',
    consumer_key=OBP_CONSUMER_KEY,
    consumer_secret=OBP_CONSUMER_SECRET
)
login_success = obp_api.login_direct(user['username'], user['password'])
accounts = obp_api.get_all_private_accounts()
transactions = obp_api.get_transactions(accounts[0]['bank_id'], accounts[0]['id'], view='owner')
dates = []
amounts = []
balances = []
for transaction in transactions:
    dates.append(transaction['details']['completed'])
    amounts.append(transaction['details']['value']['amount'])
    balances.append(transaction['details']['new_balance']['amount'])
datemin = datetime.strptime(min(dates), '%Y-%m-%dT%H:%M:%SZ')
# datemax = datetime.strptime(sorted(dates, reverse=True)[3], '%Y-%m-%dT%H:%M:%SZ')
datemax = datetime.strptime(max(dates), '%Y-%m-%dT%H:%M:%SZ')
print(datemin)
print(datemax)
dates = mdates.datestr2num(dates)


fig, ax = plt.subplots()
amount_plot = ax.plot(dates, amounts)
balance_plot = ax.plot(dates, balances)

ax.xaxis.set_major_locator(days)
ax.set_xlim(datemin, datemax)
ax.xaxis.set_major_formatter(days_fmt)

ax.format_ydata = price_fmt
ax.grid(True)

ax.legend(['Amount', 'Balances'])

fig.autofmt_xdate()

plt.setp([amount_plot, balance_plot], marker='o')
plt.show()
