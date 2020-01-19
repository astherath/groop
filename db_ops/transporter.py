# goal of file:
    # move all the data from the json file into a mongodb
import json
import datetime
import pymongo
import dateutil.parser

URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages

json_filename = 'message_test.json'


# parse the json and add to the db
def getDatetimeFromISO(s):
    d = dateutil.parser.parse(s)
    return d

with open(json_filename, 'r') as f:
    messages = json.load(f)

for message in messages:
    message['Date'] = getDatetimeFromISO(message['Date'])

col.insert_many(messages)


