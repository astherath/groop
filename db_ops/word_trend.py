import pandas as pd
import operator
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import datetime
import pymongo
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def measure_relevance(date_list):
    # get the list of total messages
    m_date = datetime.datetime(2015, 7, 6, 23, 59, 59)
    last = datetime.datetime(2020, 1, 18, 23, 59, 59)
    delta = (last - m_date).days
    print(F'master: {m_date}, last: {last}, delta: {delta}')
    master_dates = {}
    for num in range(1, delta + 1):
        master_dates[m_date] = 0
        m_date = m_date + datetime.timedelta(days=1)

    for date, mentions in date_list.items():
        new_date = date.replace(hour=23, minute=59, second=59)
        prev = new_date - datetime.timedelta(days=1)
        next_d = new_date + datetime.timedelta(days=1)
        # get total messages said that day
        relevance = col.find({'Date': {'$gt': prev, '$lt': next_d}}).count()
        master_dates[new_date] = (mentions / relevance) * 100
    return master_dates


# lookup word
def find_word(word):
    docs = col.find({'$text': {'$search': word}}, {'_id': 0, 'Date': 1})
    date_list = {}
    for document in docs:
        date = document['Date']
        if date not in date_list:
            date_list[date] = 1
        else:
            date_list[date] = date_list[date] + 1
    keys = list(date_list.keys())
    vals = list(date_list.values())
    max_val = max(vals)
    max_date = keys[vals.index(max_val)]
    print(F'max of list is {max_val} on date: {max_date}')
    date_list = measure_relevance(date_list)
    return date_list

if __name__ == '__main__':
    URL = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(URL)
    db = client.gc_data
    col = db.messages
    fig = plt.figure(figsize=[10,6])

    word1 = 'cringe'
    word2 = 'nigger'

    dates = find_word(word1)

    df1 = pd.DataFrame(list(dates.items()), columns=['Date', 'Mentions'])
    df1 = df1.sort_values(by='Date', ascending=True)

    #  dates = find_word(word2)
    #  df2 = pd.DataFrame(list(dates.items()), columns=['Date', 'Mentions'])
    #  df2 = df2.sort_values(by='Date', ascending=True)

    plt.plot(df1['Date'], df1['Mentions'], label=word1)
    #  plt.plot(df2['Date'], df2['Mentions'], label=word2)

    plt.legend(loc='upper right')
    plt.suptitle('Relevance of ' + word1 +' over time')
    plt.xlabel('Time')
    plt.ylabel('Relevance (mentions/total messages)')

    fig.savefig('../www/plot.png',pdi=8000)


