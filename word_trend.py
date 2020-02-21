import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pymongo
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# global vars
URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data


#
def measure_relevance(date_list):
    # populate a list with every day from the first message to the most recent one
    # TODO: parse first and last message dates instead of hardcoding it!!
    m_date = datetime.datetime(2015, 7, 6, 23, 59, 59)
    last = datetime.datetime(2020, 1, 18, 23, 59, 59)
    delta = (last - m_date).days
    master_dates = {}
    # populate dictionary with dates and default values of 0
    for num in range(1, delta + 1):
        master_dates[m_date] = 0
        m_date = m_date + datetime.timedelta(days=1)

    # map the amount of times word was said on a day to the date dictionary
    for date, mentions in date_list.items():
        new_date = datetime.datetime.combine(date, datetime.time(23,59,59))
        master_dates[new_date] = mentions
    # returns dict with keys=every day in span, and values=amount of times word was said on date
    return master_dates

# db method that finds amount of times word was said and maps it to a dictionary with dates
def find_word(word):
    # using $text index, finds every time word was said and it's date
    docs = col.find({'$text': {'$search': word}}, {'_id': 0, 'Date': 1})
    date_list = {}
    # iterates through the messages and maps the times a word was said to a single date
    for document in docs:
        date = document['Date'].date()
        if date not in date_list:
            date_list[date] = 1
        else:
            date_list[date] = date_list[date] + 1
    # calls measure_relevance method to update the date_list with ALL the dates, and returns it
    date_list = measure_relevance(date_list)
    return date_list

# takes in a string (word), and a boolean (raw), and generates the plot
def main_func(word, raw, user_id):
    # initialize mongo instance and set global collection variables
    col = db.user_id
    # set size of plot initially
    fig = plt.figure(figsize=[10,6])
    # dates => dictionary with all days in chat history and how many times word was mentioned on that date
    dates = find_word(word)

    # creates pd.DataFrame to plot with labels (instead of dict)
    df = pd.DataFrame(list(dates.items()), columns=['Date', 'Mentions'])
    df = df.sort_values(by='Date', ascending=True)

    # setup DataFrame so it can be modeled by Numpy polyfit
    y = df.loc[:,'Mentions']
    x = np.linspace(0,1,len(df.loc[:, 'Mentions']))
    # polynomial degrees > 10 give weird results, 8 is default
    poly_deg = 8
    coeffs = np.polyfit(x, y * 10, poly_deg)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x)
    # plot np.polyfit here and label it
    plt.plot(df.loc[:,'Date'], y_hat, label='Line of best fit')

    # if raw data was requested, plot the original DataFrame as well
    if raw:
        label_df = F'Times {word} was mentioned'
        plt.plot(df['Date'], df['Mentions'], label=label_df)

    # setup the plot to look nicer
    plt.legend(loc='upper right')
    plt.suptitle('Relevance of ' + word +' over time')
    # XXX maybe autoscale should be off?
    plt.autoscale(enable=True, axis='both')
    plt.xlabel('Time')
    plt.ylabel('Mentions')

    # save to png with set dpi, and close plt
    fig_pathname = 'frontend/imgs/' + user_id +'.png'
    fig.savefig(fig_pathname,pdi=5000)
    plt.close()
