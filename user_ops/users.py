from flask import Blueprint, request, make_response
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
def create_user(username, pwd, email):
    user = {'username': username,
            'pwd': bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()),
            'email': email}
    return user


@users.route('/signup', methods=['POST'])
def register_user():
    # parse args from request
    try:
        username = request.args.get('username')
        pwd = request.args.get('pwd')
        email = request.args.get('email')
    except Exception as e:
        print('exception:', e)
        return make_response({'Error': 'Invalid or missing input'}, 400)
    # make user
    user = create_user(username, pwd, email)
    col.insert_one(user)
    return make_response({'User created': 'OK'}, 200)


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
    user = col.find_one({'useername': username}, {'_id': 0, 'pwd': 1})
    # hash pwd and compare
    match = bcrypt.checkpw(pwd.encode('utf-8'), user['pwd'])

    if match:
        return make_response(jsonify({'login_successful': True}),200)
    else:
        return make_response(jsonify({'login_successful': False}),400)
