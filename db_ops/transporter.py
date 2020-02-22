import os
import json
import datetime
import pymongo
from pymongo import TEXT
import dateutil.parser
from bson import ObjectId

def write_to_db(file_pathname, user_id):
    # set instance vars for DB
    URL = 'mongodb://localhost:27017' # TODO: setup authentication for db
    client = pymongo.MongoClient(URL)
    db = client.gc_data
    print('userid for collection: ', user_id)
    col_name = 'b' + user_id
    col = db[col_name]

    # returns date object from string
    def getDatetimeFromISO(s):
        d = dateutil.parser.parse(s)
        return d
    # open json file and write them to db
    with open(file_pathname, 'r') as f:
        messages = json.load(f)

    for message in messages:
        message['Date'] = getDatetimeFromISO(message['Date'])
    # store message in db and save id
    col.insert_many(messages)
    try:
        col.create_index([('Body', TEXT)], default_language='english')
        # if all has gone well, delete file
        os.remove(file_pathname)
    except Exception as e:
        print('cannot create index')
        print(e)
