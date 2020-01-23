import pandas as pd
import operator
import calendar
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import pymongo
import scipy
from scipy.interpolate import UnivariateSpline
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages

def measure_relevance(date_list):
    # get the list of total messages
    m_date = datetime.datetime(2015, 7, 6, 23, 59, 59)
    last = datetime.datetime(2020, 1, 18, 23, 59, 59)
    delta = (last - m_date).days
    master_dates = {}
    for num in range(1, delta + 1):
        master_dates[m_date] = 0
        m_date = m_date + datetime.timedelta(days=1)

    for date, mentions in date_list.items():
        new_date = datetime.datetime.combine(date, datetime.time(23,59,59))
        prev = new_date - datetime.timedelta(days=1)
        next_d = new_date + datetime.timedelta(days=1)
        # get total messages said that day
        #  relevance = col.find({'Date': {'$gt': prev, '$lt': next_d}}).count()
        master_dates[new_date] = mentions #(mentions / relevance) * 100
    return master_dates

def calculate_relevance(date_list, mention_count):
    for key, value in date_list.items():
        date_list[key] = (value / mention_count) * 100
    return date_list

# lookup word
def find_word(word):
    docs = col.find({'$text': {'$search': word}}, {'_id': 0, 'Date': 1})
    date_list = {}
    for document in docs:
        date = document['Date'].date()
        if date not in date_list:
            date_list[date] = 1
        else:
            date_list[date] = date_list[date] + 1
    keys = list(date_list.keys())
    vals = list(date_list.values())
    mention_count = len(vals)
    date_list = measure_relevance(date_list)
    #  date_list = calculate_relevance(date_list, mention_count)
    return date_list

def toTimestamp(d):
    return calendar.timegm(d.timetuple())

def main_func(word1):
    fig = plt.figure(figsize=[10,6])

    dates = find_word(word1)

    df1 = pd.DataFrame(list(dates.items()), columns=['Date', 'Mentions'])
    df1 = df1.sort_values(by='Date', ascending=True)

    y = df1.loc[:,'Mentions']
    x = np.linspace(0,1,len(df1.loc[:, 'Mentions']))
    poly_deg = 8

    coeffs = np.polyfit(x, y * 10, poly_deg)

    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x)
    plt.plot(df1.loc[:,'Date'], y_hat, label='Line of best fit')


    plt.legend(loc='upper right')
    plt.suptitle('Relevance of ' + word1 +' over time')
    plt.autoscale(enable=True, axis='both')
    plt.xlabel('Time')
    plt.ylabel('Relevance (mentions/total messages)')

    fig.savefig('www/plot.png',pdi=8000)


