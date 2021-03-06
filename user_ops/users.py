from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
import bcrypt
import pymongo

# init blueprint
users = Blueprint('users', __name__)

# init pymongo client to users collection
URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.users

# validation reqs
USERNAME_MIN_LENGTH = 6
PASSWORD_MIN_LENGTH = 8

# method that creates a user with given params
def create_user(username, pwd):
    user = {'username': username,
            'pwd': bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())}
    return user


@users.route('/signup', methods=['POST'])
def register_user():
    # parse args from request and verify that input is safe
    try:
        username = request.args.get('username')
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Invalid or missing username'}), 400)
    try:
        assert(username.isalnum())
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Username should only contain letters and numbers'}), 400)
    try:
        assert(len(username) >= USERNAME_MIN_LENGTH)
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Username too short (Minimum ' + str(USERNAME_MIN_LENGTH) + ' characters)'}), 400)
    try:
        pwd = request.args.get('pwd')
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Invalid or missing password'}), 400)
    try:
        assert(len(pwd) >= PASSWORD_MIN_LENGTH)
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Password too short (Minimum ' + str(PASSWORD_MIN_LENGTH) + ' characters)'}), 400)
    # check if user exists
    duplicate = (col.find_one({'username' : username}) is not None)
    if (not duplicate):
        # make user
        user = create_user(username, pwd)
        insert = col.insert_one(user)
        user_id = str(insert.inserted_id)
        return make_response(jsonify({'created': True, 'id': user_id}), 200)
    else:
        return make_response(jsonify({'created': False, 'error': 'Username already in use'}), 400)


@users.route('/login', methods=['GET'])
def login_user():
    # parse args from request
    try:
        username = request.args.get('username')
        pwd = request.args.get('pwd')
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'error': 'Invalid or missing input'}), 400)
    # lookup user in db and compare hashes
    user = col.find_one({'username': username}, {'_id': 1, 'pwd': 1})
    # return 400 if user doesnt exist
    if (user is None):
        return make_response(jsonify({'error': 'User not found'}), 404)
    # hash pwd and compare
    match = bcrypt.checkpw(pwd.encode('utf-8'), user['pwd'])

    if match:
        redirect = False
        # get user id to return
        user_id = str(user['_id'])
        # check if they have a collection on file, if not, send to upload page
        names = db.collection_names()
        if (('b' + user_id) not in names):
            redirect = True

        return make_response(jsonify({'success': True, 'id': user_id, 'redirect': redirect}),200)
    else:
        return make_response(jsonify({'success': False, 'error': 'Incorrect password'}),400)
