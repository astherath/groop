import json
import datetime
import pymongo
import dateutil.parser

file_pathname = '../mains/message_test.json'

def write_to_db(file_pathname):
    # set instance vars for DB
    URL = 'mongodb://localhost:27017' # TODO: setup authentication for db
    client = pymongo.MongoClient(URL)
    # TODO: update to support multiple users
    db = client.gc_data
    col = db.messages

    # parse the json and add to the db
    def getDatetimeFromISO(s):
        d = dateutil.parser.parse(s)
        return d
    # open json file and write them to db
    with open(file_pathname, 'r') as f:
        messages = json.load(f)
    for message in messages:
        message['Date'] = getDatetimeFromISO(message['Date'])
    col.insert_many(messages)
