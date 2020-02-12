from flask import Blueprint, request, make_response, jsonify
import bcrypt
import pymongo

# init blueprint
users = Blueprint('users', __name__)

# init pymongo client to users collection
URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.users

# method that creates a user with given params
def create_user(username, pwd):
    user = {'username': username,
            'pwd': bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())}
    return user


@users.route('/signup', methods=['POST'])
def register_user():
    # parse args from request
    try:
        username = request.args.get('username')
        pwd = request.args.get('pwd')
    except Exception as e:
        print('exception:', e)
        return make_response(jsonify({'Missing': 'Invalid or missing input'}), 400)
    # check if user exists
    duplicate = (col.find_one({'username' : username}) is not None)
    if (not duplicate):
        # make user
        user = create_user(username, pwd)
        col.insert_one(user)
        return make_response(jsonify({'created': True}), 200)
    else:
        return make_response(jsonify({'created': False, 'duplicate': True}), 400)


@users.route('/login', methods=['GET'])
def login_user():
    # parse args from request
    try:
        username = request.args.get('username')
        pwd = request.args.get('pwd')
    except Exception as e:
        print('exception:', e)
        return make_response({'Error': 'Invalid or missing input'}, 400)
    # lookup user in db and compare hashes
    user = col.find_one({'username': username}, {'_id': 0, 'pwd': 1})
    # return 400 if user doesnt exist
    if (user is None):
        return make_response({'Error': 'User not found'}, 404)
    # hash pwd and compare
    match = bcrypt.checkpw(pwd.encode('utf-8'), user['pwd'])

    if match:
        return make_response({'login_successful': True},200)
    else:
        return make_response({'login_successful': False},400)
