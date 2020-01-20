import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import datetime
import pymongo
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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
    return date_list

def words_by_author(word, author):
    docs = col.find_one({'Author': author, '$text': {'$search': word}}, {'_id': 0})

    date_list = {}
    for document in docs:
        date = document['Date'].date()
        if date not in date_list:
            date_list[date] = 1
        else:
            date_list[date] = date_list[date] + 1
    return date_list

def setup(ax):
    ax.autoscale(enable=True, axis='x', tight=True)

def find_first_occurence(author, word):
    document = col.find({"Author":author, '$text': {'$search': "ploopy"}}, {"_id": 0, "Date": 1}).sort('Date',pymongo.DESCENDING).limit(1)
    for doc in document:
        return doc['Date'].date()


if __name__ == '__main__':
    URL = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(URL)
    db = client.gc_data
    col = db.messages

    word = 'ploopy'
    dates = find_word(word)
    author = 'Babak'
    first = find_first_occurence(author, word)

    df = pd.DataFrame(list(dates.items()), columns=['Date', 'Mentions'])
    df.set_index(['Date'],inplace=True)
    ax = df.plot(kind='line', title=F'Amount of times we said \"{word}\" in the GC', figsize=(15,13))
    #  plt.plot(df['Date'], df['Mentions'])
    plt.xticks(rotation='vertical')
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    #  setup(ax)

    label = F'First time {author} says {word}'
    plt.annotate(label, (first,dates[first]),textcoords='offset points', xytext=(15,20),ha='center',arrowprops={'arrowstyle':'->'})
    plt.tick_params(axis='x', which='major', labelsize=10)

    for x, y in dates.items():
        plt.annotate(str(y),(x, y),textcoords='offset points', xytext=(-20,10),ha='center',arrowprops={'arrowstyle':'->'})
        plt.plot([x],[y],'o')

    plt.savefig('../www/plot.png',pdi=8000)


