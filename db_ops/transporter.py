import os
import json
import datetime
import pymongo
import dateutil.parser
from bson import ObjectId

async def write_to_db(file_pathname, user_id):
    # call Go method to write json file
    command = 'go run main'
    subprocess.run(

    # set instance vars for DB
    URL = 'mongodb://localhost:27017' # TODO: setup authentication for db
    client = pymongo.MongoClient(URL)
    # TODO: update to support multiple users
    db = client.gc_data
    col = db.messages
    # this array of messages will be equivalent to an entire gc file
    message_list = []

    # returns date object from string
    def getDatetimeFromISO(s):
        d = dateutil.parser.parse(s)
        return d
    # open json file and write them to db
    with open(file_pathname, 'r') as f:
        messages = json.load(f)
    for message in messages:
        message['Date'] = getDatetimeFromISO(message['Date'])
        # now add to message list
        message_list.append(message)
    # store message in db and save id
    insert = col.insert_one(message_list)
    file_id = insert.inserted_id
    # store the id of this gc file on the user's document
    try:
        db.users.update({'_id': ObjectId(user_id)}, {'$set': {'gc_id': file_id}})
    except Exception as e:
        print(e)
