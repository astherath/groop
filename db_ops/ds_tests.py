import json
import datetime
import pymongo
import dateutil.parser

URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages


# lookup word
def find_word(word):
    docs = col.find({'$text': {'$search': word}}, {'_id': 0, 'Date': 1})
    print(F'amount of results for \"{word}\": {docs.count()}')

    for document in docs:
        print(F'date is: {document.date()}')

find_word('ploopy')

